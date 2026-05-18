"""Page object cho Checkout Step 2 - xem lại đơn hàng (URL: /checkout-step-two.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutStep2Page(BasePage):

    TITLE = (By.CSS_SELECTOR, ".title")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    PAYMENT_INFO_LABEL = (By.XPATH, "//div[contains(text(), 'Payment Information')]")
    SHIPPING_INFO_LABEL = (By.XPATH, "//div[contains(text(), 'Shipping Information')]")
    SUBTOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label")
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_item_count(self):
        """Đếm số item trong overview."""
        return len(self.find_elements_safe(self.CART_ITEMS))

    def get_item_prices(self):
        """Lấy danh sách giá từng item dạng float."""
        return [float(el.text.replace("$", "")) for el in self.find_elements_safe(self.ITEM_PRICES)]

    def is_payment_info_displayed(self):
        return self.is_displayed(self.PAYMENT_INFO_LABEL)

    def is_shipping_info_displayed(self):
        return self.is_displayed(self.SHIPPING_INFO_LABEL)

    def get_subtotal(self):
        """Lấy subtotal từ label 'Item total: $X.XX' -> trả về float."""
        return float(self.get_text(self.SUBTOTAL_LABEL).split("$")[-1])

    def get_tax(self):
        """Lấy tax từ label 'Tax: $X.XX' -> trả về float."""
        return float(self.get_text(self.TAX_LABEL).split("$")[-1])

    def get_total(self):
        """Lấy total từ label 'Total: $X.XX' -> trả về float."""
        return float(self.get_text(self.TOTAL_LABEL).split("$")[-1])

    def click_finish(self):
        """Xác nhận đặt hàng -> sang trang hoàn thành."""
        self.click(self.FINISH_BUTTON)
        self.wait_for_url_contains("checkout-complete")

    def click_cancel(self):
        """Hủy -> về trang danh sách sản phẩm."""
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url_contains("inventory.html")
