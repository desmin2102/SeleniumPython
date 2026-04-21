"""Pytest fixtures + hooks dùng chung cho toàn bộ test."""

import os
import re
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import read_config

SCREENSHOTS_DIR = "screenshots"


def pytest_configure(config):
    # Dọn sạch thư mục screenshot trước mỗi lần chạy full suite
    if os.path.isdir(SCREENSHOTS_DIR):
        shutil.rmtree(SCREENSHOTS_DIR)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # Custom metadata cho HTML report - bỏ info không liên quan (JAVA_HOME),
    # thêm info hữu ích (URL test, browser, headless)
    cfg = read_config()
    if hasattr(config, "stash"):
        from pytest_metadata.plugin import metadata_key
        meta = config.stash[metadata_key]
    else:
        meta = config._metadata
    meta.pop("JAVA_HOME", None)
    meta.pop("Plugins", None)
    meta["Base URL"] = cfg.get("base_url")
    meta["Browser"] = cfg.get("browser")
    meta["Headless"] = cfg.get("headless")


@pytest.fixture(scope="function")
def driver():
    # Khởi tạo Chrome cho mỗi test, tự đóng browser sau khi test xong
    config = read_config()

    chrome_options = Options()
    if config.get("headless", "false").lower() == "true":
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Disable Chrome password leak detection (dialog này block automation vì
    # password 'secret_sauce' nằm trong list password bị breach)
    chrome_options.add_argument("--disable-features=PasswordLeakDetection,"
                                "AutofillServerCommunication,"
                                "PasswordCheck,PasswordManagerOnboarding")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "autofill.profile_enabled": False,
    })
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=chrome_options)
    drv.get(config.get("base_url"))

    yield drv

    drv.quit()


def _extract_tc_id(test_name):
    # Lấy TC ID từ tên test, vd: 'test_TC_LOGIN_001_valid' -> 'TC_LOGIN_001'
    match = re.search(r"(TC_[A-Z0-9]+_\d+)", test_name)
    return match.group(1) if match else test_name


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Chụp screenshot sau mỗi test (pass/fail/skip), tên file = TC_ID + status
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    drv = item.funcargs.get("driver")
    if drv is None:
        return

    tc_id = _extract_tc_id(item.name)
    status = "PASS" if report.passed else ("FAIL" if report.failed else "SKIP")
    filepath = os.path.join(SCREENSHOTS_DIR, f"{tc_id}_{status}.png")
    try:
        drv.save_screenshot(filepath)
        report.extra_screenshot = filepath
    except Exception:
        pass


# Hook customize HTML report: thêm cột TC ID và đổi tiêu đề

def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>TC ID</th>")


def pytest_html_results_table_row(report, cells):
    tc_id = _extract_tc_id(report.nodeid.split("::")[-1])
    cells.insert(2, f"<td>{tc_id}</td>")


def pytest_html_report_title(report):
    report.title = "SauceDemo - Automation Test Report"
