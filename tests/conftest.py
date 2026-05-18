"""Pytest fixtures và hooks dùng chung cho toàn bộ test."""

import os
import shutil

import pytest

from utils.driver_factory import create_driver
from utils.helpers import read_config, read_test_data
from utils.logger import get_logger

SCREENSHOTS_DIR = "screenshots"
log = get_logger("conftest")


def pytest_configure(config):
    """Xóa screenshots cũ trước khi chạy. Bỏ qua nếu đang là worker khi chạy parallel."""
    is_xdist_worker = hasattr(config, "workerinput")
    if not is_xdist_worker and os.path.isdir(SCREENSHOTS_DIR):
        shutil.rmtree(SCREENSHOTS_DIR)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def config():
    """Đọc config một lần, dùng chung cho cả session."""
    return read_config()


@pytest.fixture(scope="session")
def test_data():
    """Đọc test data một lần, dùng chung cho cả session."""
    return read_test_data()


@pytest.fixture(scope="function")
def driver(config):
    """Tạo browser cho mỗi test, tự đóng khi test xong."""
    headless = config.get("headless", "true").lower() == "true"
    drv = create_driver(headless)
    drv.get(config.get("base_url"))
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Chụp screenshot sau mỗi test, đặt tên theo kết quả PASS/FAIL/SKIP."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    drv = item.funcargs.get("driver")
    if drv is None:
        return

    status = "PASS" if report.passed else ("FAIL" if report.failed else "SKIP")
    filename = f"{item.name}_{status}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)

    try:
        drv.save_screenshot(filepath)
    except Exception as e:
        log.warning("Không chụp được screenshot: %s", e)

    if report.failed:
        log.error("TEST FAIL: %s", item.name)


def pytest_html_report_title(report):
    """Đặt tiêu đề cho HTML report."""
    report.title = "SauceDemo - Automation Test Report"
