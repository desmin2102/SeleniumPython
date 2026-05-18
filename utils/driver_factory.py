"""Khởi tạo Chrome WebDriver với các option cần thiết."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from utils.logger import get_logger

log = get_logger(__name__)


def create_driver(headless=True):
    """Tạo và trả về Chrome driver. webdriver-manager tự download driver."""
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-notifications")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    log.info("Khởi tạo Chrome driver thành công")
    return driver
