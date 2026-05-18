"""Page object cho trang xác nhận đặt hàng thành công (URL: /checkout-complete.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):

    TITLE = (By.CSS_SELECTOR, ".title")
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")
    PONY_EXPRESS_IMAGE = (By.CSS_SELECTOR, ".pony_express")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def get_complete_header(self):
        """Đọc tiêu đề xác nhận đặt hàng thành công."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self):
        return self.get_text(self.COMPLETE_TEXT)

    def is_pony_express_image_displayed(self):
        return self.is_displayed(self.PONY_EXPRESS_IMAGE)

    def click_back_home(self):
        """Quay về trang chủ."""
        self.click(self.BACK_HOME_BUTTON)
        self.wait_for_url_contains("inventory.html")
