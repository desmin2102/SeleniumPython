"""Page object cho Checkout Step 1 - Your Information (URL: /checkout-step-one.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutStep1Page(BasePage):
    """
    Bước 1 của checkout - nhập thông tin giao hàng.
    Có 3 field bắt buộc: First Name, Last Name, Postal Code.
    Nếu thiếu field nào, site sẽ báo "Error: [Field name] is required".
    """

    TITLE = (By.CSS_SELECTOR, ".title")  # "Checkout: Your Information"
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def fill_info(self, first_name, last_name, postal_code):
        """Nhập 3 field. Field nào rỗng thì BỎ QUA không nhập - dùng cho test case
        cố tình để trống 1 field để verify error message."""
        if first_name:
            self.send_keys(self.FIRST_NAME_INPUT, first_name)
        if last_name:
            self.send_keys(self.LAST_NAME_INPUT, last_name)
        if postal_code:
            self.send_keys(self.POSTAL_CODE_INPUT, postal_code)

    def click_continue(self):
        """Click Continue mà KHÔNG chờ URL đổi.
        Dùng cho test case validation fail - URL không đổi vì error chặn navigation."""
        self.click(self.CONTINUE_BUTTON)

    def click_continue_and_wait(self):
        """Click Continue VÀ chờ URL chuyển sang step-two.
        Dùng cho test case validation pass - chắc chắn page đã load xong bước 2."""
        self.click_continue()
        self.wait_for_url_contains("checkout-step-two")

    def click_cancel(self):
        """Click Cancel -> quay lại cart."""
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url_contains("cart.html")

    def get_error_message(self):
        """Đọc text của error message khi validation fail."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_present(self.ERROR_MESSAGE)
