"""BasePage - class cha của mọi page object trong project."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import read_config
from utils.logger import get_logger


class BasePage:
    """
    Class cha chứa các method dùng chung cho tất cả page.
    Mọi LoginPage, CartPage, CheckoutPage... đều kế thừa class này
    để tránh viết lại code click, nhập liệu, chờ element.
    """

    def __init__(self, driver):
        self.driver = driver
        timeout = int(read_config().get("explicit_wait", 15))
        # WebDriverWait = explicit wait, chờ điều kiện thỏa thì mới tiếp tục
        self.wait = WebDriverWait(driver, timeout)
        self.log = get_logger(self.__class__.__name__)

    # ================================================================
    # NHÓM 1: TÌM ELEMENT TRÊN TRANG
    # ================================================================

    def find_element(self, locator):
        """Tìm 1 element. Chờ đến khi element có trong DOM."""
        self.log.debug("find_element %s", locator)
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Tìm danh sách element. Chờ đến khi có ít nhất 1 element match."""
        self.log.debug("find_elements %s", locator)
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_elements_safe(self, locator):
        """Tìm element nhưng KHÔNG chờ, KHÔNG throw nếu không có.
        Trả về list rỗng nếu không tìm thấy."""
        return self.driver.find_elements(*locator)

    # ================================================================
    # NHÓM 2: THAO TÁC VỚI ELEMENT (click, nhập liệu, đọc text)
    # ================================================================

    def click(self, locator):
        """Click vào element. Chờ element clickable (hiện + enable + không bị overlay che)."""
        self.log.info("click %s", locator)
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def js_click(self, locator):
        """Click bằng JavaScript thay vì Selenium.
        Dùng khi click thường không hoạt động - thường là do React override
        event handler, hoặc element bị overlay che một phần."""
        self.log.info("js_click %s", locator)
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, text):
        """Nhập text vào input. Clear giá trị cũ trước, rồi mới type."""
        self.log.info("send_keys %s = %r", locator, text)
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def js_set_value(self, locator, text):
        """Set giá trị input bằng JavaScript, có fire React's change event.
        Dùng khi send_keys không xử lý được, ví dụ:
        - Emoji, ký tự ngoài BMP (U+10000 trở lên) - ChromeDriver không hỗ trợ
        - Input bị React kiểm soát rất chặt, giá trị set không kích hoạt onChange"""
        self.log.info("js_set_value %s = %r", locator, text)
        element = self.find_element(locator)
        self.driver.execute_script(
            """
            const el = arguments[0], val = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """,
            element,
            text,
        )

    def get_text(self, locator):
        """Đọc text hiển thị của element."""
        return self.find_element(locator).text

    def get_attribute(self, locator, attr):
        """Đọc attribute của element (ví dụ 'value', 'href', 'type')."""
        return self.find_element(locator).get_attribute(attr)

    def is_displayed(self, locator):
        """Kiểm tra element có hiện trên UI không.
        Trả về False nếu element không tồn tại hoặc bị hidden (display:none, visibility:hidden)."""
        try:
            return self.find_element(locator).is_displayed()
        except Exception:
            return False

    def is_present(self, locator):
        """Kiểm tra element có trong DOM không (không quan tâm hiện hay ẩn).
        Nhanh hơn is_displayed vì không chờ timeout."""
        return len(self.find_elements_safe(locator)) > 0

    # ================================================================
    # NHÓM 3: ĐIỀU HƯỚNG VÀ CHỜ TRANG LOAD
    # ================================================================

    def wait_for_url_contains(self, fragment):
        """Chờ đến khi URL chứa chuỗi cho trước."""
        self.log.debug("wait_for_url_contains %r", fragment)
        self.wait.until(EC.url_contains(fragment))

    def wait_for_element_visible(self, locator):
        """Chờ element HIỆN trên UI (không chỉ có trong DOM)."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_invisible(self, locator):
        """Chờ element BIẾN MẤT khỏi UI (đóng dialog, kết thúc animation...)."""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title

    def scroll_to_bottom(self):
        """Scroll xuống cuối trang - dùng khi test footer hoặc lazy-load content."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
