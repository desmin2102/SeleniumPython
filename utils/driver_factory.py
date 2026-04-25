"""Factory tạo WebDriver theo browser được chọn (Chrome, Firefox, Edge).

Mỗi browser có config riêng (headless flag, options chung và options đặc thù).
Driver tự download qua webdriver-manager nên không cần cài tay.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.logger import get_logger

log = get_logger("DriverFactory")

WINDOW_SIZE = "1920,1080"


def _build_chrome(headless):
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--window-size={WINDOW_SIZE}")

    # Disable Chrome password leak detection - dialog này block automation vì
    # 'secret_sauce' nằm trong list password bị breach
    opts.add_argument(
        "--disable-features=PasswordLeakDetection,"
        "AutofillServerCommunication,PasswordCheck,PasswordManagerOnboarding"
    )
    opts.add_argument("--disable-save-password-bubble")
    opts.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
        },
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def _build_firefox(headless):
    opts = FirefoxOptions()
    if headless:
        opts.add_argument("--headless")
    opts.add_argument(f"--width={WINDOW_SIZE.split(',')[0]}")
    opts.add_argument(f"--height={WINDOW_SIZE.split(',')[1]}")

    # Tắt password manager của Firefox để tránh dialog "Save password?" che element
    opts.set_preference("signon.rememberSignons", False)
    opts.set_preference("signon.autofillForms", False)

    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=opts)


def _build_edge(headless):
    opts = EdgeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--window-size={WINDOW_SIZE}")
    opts.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )

    service = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=opts)


_BUILDERS = {
    "chrome": _build_chrome,
    "firefox": _build_firefox,
    "edge": _build_edge,
}


def create_driver(browser, headless):
    """Tạo driver theo browser ('chrome' | 'firefox' | 'edge')."""
    browser = (browser or "chrome").lower()
    if browser not in _BUILDERS:
        raise ValueError(
            f"Browser không hỗ trợ: {browser!r}. " f"Chọn 1 trong: {list(_BUILDERS.keys())}"
        )
    log.info("Tạo driver: browser=%s headless=%s", browser, headless)
    return _BUILDERS[browser](headless)
