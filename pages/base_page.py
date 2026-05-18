"""BasePage - class cha của mọi page object trong project."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import read_config


class BasePage:
    """Class cha chứa các method dùng chung. Mọi page đều kế thừa class này."""

    def __init__(self, driver):
        self.driver = driver
        timeout = int(read_config().get("explicit_wait", 15))
        self.wait = WebDriverWait(driver, timeout)

    # --- Tìm element ---

    def find_element(self, locator):
        """Tìm 1 element, chờ element xuất hiện trong DOM."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Tìm nhiều element, trả về list."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_elements_safe(self, locator):
        """Tìm element không chờ, trả về list rỗng nếu không có."""
        return self.driver.find_elements(*locator)

    # --- Thao tác với element ---

    def click(self, locator):
        """Click vào element, chờ element có thể click được."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text):
        """Xóa nội dung cũ rồi nhập text mới vào input."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Lấy text hiển thị của element."""
        return self.find_element(locator).text

    def get_attribute(self, locator, attr):
        """Lấy giá trị attribute của element (vd: 'href', 'type', 'value')."""
        return self.find_element(locator).get_attribute(attr)

    def is_displayed(self, locator):
        """Kiểm tra element có hiển thị trên màn hình không."""
        try:
            return self.find_element(locator).is_displayed()
        except Exception:
            return False

    def is_present(self, locator):
        """Kiểm tra element có tồn tại trong DOM không."""
        return len(self.find_elements_safe(locator)) > 0

    # --- Điều hướng và chờ trang ---

    def wait_for_url_contains(self, fragment):
        """Chờ URL chứa chuỗi cho trước."""
        self.wait.until(EC.url_contains(fragment))

    def wait_for_element_visible(self, locator):
        """Chờ element hiển thị trên màn hình."""
        return self.wait.until(EC.visibility_of_element_located(locator))
