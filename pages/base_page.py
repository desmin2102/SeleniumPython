"""BasePage - class cha của mọi page object trong project."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Class cha chứa các method dùng chung cho tất cả page.
    Mọi LoginPage, CartPage, CheckoutPage... đều kế thừa class này
    để tránh viết lại code click, nhập liệu, chờ element.
    """

    # Timeout mặc định cho WebDriverWait (đơn vị: giây)
    # Để 15s vì SauceDemo dùng React, đôi khi render chậm
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        # WebDriverWait = explicit wait, chờ điều kiện thỏa thì mới tiếp tục
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # ================================================================
    # NHÓM 1: TÌM ELEMENT TRÊN TRANG
    # ================================================================

    def find_element(self, locator):
        """Tìm 1 element. Chờ đến khi element có trong DOM (tối đa 15s).
        Nếu không tìm thấy sau 15s -> throw TimeoutException."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Tìm danh sách element. Chờ đến khi có ít nhất 1 element match."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_elements_safe(self, locator):
        """Tìm element nhưng KHÔNG chờ, KHÔNG throw nếu không có.
        Trả về list rỗng nếu không tìm thấy.
        Dùng khi muốn kiểm tra element "có thể" tồn tại (ví dụ: cart badge
        có thể hiện hoặc không hiện - không muốn test fail vì chờ 15s vô ích)."""
        return self.driver.find_elements(*locator)

    # ================================================================
    # NHÓM 2: THAO TÁC VỚI ELEMENT (click, nhập liệu, đọc text)
    # ================================================================

    def click(self, locator):
        """Click vào element. Chờ element clickable (hiện + enable + không bị overlay che)."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def js_click(self, locator):
        """Click bằng JavaScript thay vì Selenium.
        Dùng khi click thường không hoạt động - thường là do React override
        event handler, hoặc element bị overlay che một phần.
        Trong project này, Finish button của checkout-step-two gặp case đó."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, text):
        """Nhập text vào input. Clear giá trị cũ trước, rồi mới type.
        Nếu không clear trước -> text sẽ nối vào giá trị cũ."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def js_set_value(self, locator, text):
        """Set giá trị input bằng JavaScript, có fire React's change event.
        Dùng khi send_keys không xử lý được, ví dụ:
        - Emoji, ký tự ngoài BMP (U+10000 trở lên) - ChromeDriver không hỗ trợ
        - Input bị React kiểm soát rất chặt, giá trị set không kích hoạt onChange
        Cách hoạt động:
        - Lấy setter gốc của HTMLInputElement.value (không bị React override)
        - Gọi setter để set giá trị thật
        - Fire sự kiện 'input' và 'change' để React biết giá trị đổi"""
        element = self.find_element(locator)
        self.driver.execute_script("""
            const el = arguments[0], val = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, element, text)

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
        Nhanh hơn is_displayed vì không chờ 15s."""
        return len(self.find_elements_safe(locator)) > 0

    # ================================================================
    # NHÓM 3: ĐIỀU HƯỚNG VÀ CHỜ TRANG LOAD
    # ================================================================

    def wait_for_url_contains(self, fragment):
        """Chờ đến khi URL chứa chuỗi cho trước.
        Dùng sau khi click 1 button để chắc chắn page đã navigate xong trước khi làm bước tiếp.
        Ví dụ: sau click Checkout -> chờ URL chứa 'checkout-step-one'."""
        self.wait.until(EC.url_contains(fragment))

    def wait_for_element_visible(self, locator):
        """Chờ element HIỆN trên UI (không chỉ có trong DOM).
        Khác presence_of_element_located ở chỗ: element có thể có trong DOM
        nhưng display:none - lúc đó visible wait vẫn chờ, presence wait thì return luôn."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_current_url(self):
        """Lấy URL hiện tại."""
        return self.driver.current_url

    def get_title(self):
        """Lấy <title> của trang (text trên tab browser)."""
        return self.driver.title

    def scroll_to_bottom(self):
        """Scroll xuống cuối trang - dùng khi test footer hoặc lazy-load content."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
