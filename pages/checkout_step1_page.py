"""Page object cho Checkout Step 1 - nhập thông tin giao hàng (URL: /checkout-step-one.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutStep1Page(BasePage):

    TITLE = (By.CSS_SELECTOR, ".title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def fill_info(self, first_name, last_name, postal_code):
        """Điền thông tin giao hàng. Field nào truyền vào rỗng thì bỏ qua."""
        if first_name:
            self.send_keys(self.FIRST_NAME_INPUT, first_name)
        if last_name:
            self.send_keys(self.LAST_NAME_INPUT, last_name)
        if postal_code:
            self.send_keys(self.POSTAL_CODE_INPUT, postal_code)

    def click_continue(self):
        """Click Continue, không chờ URL đổi."""
        self.click(self.CONTINUE_BUTTON)

    def click_continue_and_wait(self):
        """Click Continue và chờ chuyển sang step 2."""
        self.click_continue()
        self.wait_for_url_contains("checkout-step-two")

    def click_cancel(self):
        """Click Cancel -> quay lại giỏ hàng."""
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url_contains("cart.html")

    def get_error_message(self):
        """Lấy text thông báo lỗi."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_present(self.ERROR_MESSAGE)
