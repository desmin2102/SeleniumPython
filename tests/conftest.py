"""Pytest fixtures + hooks dùng chung cho toàn bộ test."""

import os
import re
import shutil

import pytest

from utils.driver_factory import create_driver
from utils.helpers import read_config, read_test_data
from utils.logger import _get_log_file, get_logger

SCREENSHOTS_DIR = "screenshots"
log = get_logger("conftest")


# ---------- CLI options ----------


def pytest_addoption(parser):
    """CLI flag để override config nhanh:
    pytest --browser firefox
    pytest --env staging --browser chrome
    """
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser: chrome | firefox | edge (override config.ini)",
    )
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Môi trường: dev | staging | prod (override TEST_ENV)",
    )


# ---------- Session setup ----------


def pytest_configure(config):
    # Chỉ xóa screenshots khi chạy full suite (không có -k filter và không phải worker xdist)
    is_xdist_worker = hasattr(config, "workerinput")
    if not is_xdist_worker and os.path.isdir(SCREENSHOTS_DIR):
        shutil.rmtree(SCREENSHOTS_DIR)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # Resolve config theo --env / --browser CLI flag (override env var)
    env = config.getoption("--env")
    browser = config.getoption("--browser")
    if env:
        os.environ["TEST_ENV"] = env
    if browser:
        os.environ["TEST_BROWSER"] = browser

    cfg = read_config()
    log.info(
        "Test session bắt đầu | env=%s | browser=%s | base_url=%s | headless=%s",
        cfg.get("_env"),
        cfg.get("browser"),
        cfg.get("base_url"),
        cfg.get("headless"),
    )

    # Custom metadata cho HTML report
    if hasattr(config, "stash"):
        from pytest_metadata.plugin import metadata_key

        meta = config.stash[metadata_key]
    else:
        meta = config._metadata
    meta.pop("JAVA_HOME", None)
    meta.pop("Plugins", None)
    meta["Environment"] = cfg.get("_env")
    meta["Base URL"] = cfg.get("base_url")
    meta["Browser"] = cfg.get("browser")
    meta["Headless"] = cfg.get("headless")
    meta["Log file"] = _get_log_file()


# ---------- Fixtures ----------


@pytest.fixture(scope="session")
def config():
    """Config đã resolve env + override - share giữa các test."""
    return read_config()


@pytest.fixture(scope="session")
def test_data():
    """Test data từ testdata/test_data.json (credentials, checkout info...)."""
    return read_test_data()


@pytest.fixture(scope="function")
def driver(config):
    """Tạo browser cho mỗi test. Tự đóng khi test xong."""
    headless = str(config.get("headless", "true")).lower() == "true"
    drv = create_driver(config.get("browser"), headless)
    drv.get(config.get("base_url"))
    yield drv
    drv.quit()


# ---------- Screenshot hook ----------


def _extract_tc_id(test_name):
    # 'test_TC_LOGIN_001_valid[standard_user]' -> 'TC_LOGIN_001'
    match = re.search(r"(TC_[A-Z0-9]+_\d+)", test_name)
    return match.group(1) if match else test_name


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Chụp screenshot sau mỗi test (pass/fail/skip)."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    drv = item.funcargs.get("driver")
    if drv is None:
        return

    tc_id = _extract_tc_id(item.name)
    status = "PASS" if report.passed else ("FAIL" if report.failed else "SKIP")
    # Param suffix phân biệt parametrize cases - bỏ qua nếu param chính là TC_ID
    # (tránh tên kiểu TC_URL_001_PASS_TC_URL_001.png)
    param = item.name.split("[")[1].rstrip("]") if "[" in item.name else ""
    suffix = f"_{re.sub(r'[^A-Za-z0-9]+', '_', param)}" if param and param != tc_id else ""
    filepath = os.path.join(SCREENSHOTS_DIR, f"{tc_id}_{status}{suffix}.png")

    try:
        drv.save_screenshot(filepath)
        report.extra_screenshot = filepath
    except Exception as exc:
        log.warning("Không chụp được screenshot cho %s: %s", item.name, exc)

    if report.failed:
        log.error("FAIL %s -> %s", item.name, filepath)


# ---------- HTML report customization ----------


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>TC ID</th>")


def pytest_html_results_table_row(report, cells):
    tc_id = _extract_tc_id(report.nodeid.split("::")[-1])
    cells.insert(2, f"<td>{tc_id}</td>")


def pytest_html_report_title(report):
    report.title = "SauceDemo - Automation Test Report"
