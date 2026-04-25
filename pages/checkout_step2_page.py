"""Page object cho Checkout Step 2 - Overview (URL: /checkout-step-two.html)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutStep2Page(BasePage):
    """
    Bước 2 của checkout - xem lại đơn hàng trước khi xác nhận.
    Hiện: list item đã đặt, payment/shipping info, tính tổng (subtotal + tax = total).
    2 nút: Finish (xác nhận) và Cancel (hủy về inventory).
    """

    TITLE = (By.CSS_SELECTOR, ".title")  # "Checkout: Overview"
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")

    # Payment/Shipping info dùng XPath tìm theo text vì site không có selector riêng
    PAYMENT_INFO_LABEL = (By.XPATH, "//*[contains(text(), 'Payment Information')]")
    SHIPPING_INFO_LABEL = (By.XPATH, "//*[contains(text(), 'Shipping Information')]")

    SUBTOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label")  # "Item total: $X.XX"
    TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label")  # "Tax: $X.XX"
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label")  # "Total: $X.XX"
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    def get_title_text(self):
        return self.get_text(self.TITLE)

    def get_item_count(self):
        """Số lượng item trong overview - dùng để verify đúng với số đã add vào cart."""
        return len(self.find_elements_safe(self.CART_ITEMS))

    def get_item_prices(self):
        """List giá từng item dạng float - dùng để kiểm tra phép tính subtotal."""
        return [float(el.text.replace("$", "")) for el in self.find_elements_safe(self.ITEM_PRICES)]

    def is_payment_info_displayed(self):
        return self.is_displayed(self.PAYMENT_INFO_LABEL)

    def is_shipping_info_displayed(self):
        return self.is_displayed(self.SHIPPING_INFO_LABEL)

    def get_subtotal(self):
        """Parse label 'Item total: $32.39' -> trả về số float 32.39.
        Split theo '$' và lấy phần sau cùng (trường hợp text có nhiều dấu $)."""
        text = self.get_text(self.SUBTOTAL_LABEL)
        return float(text.split("$")[-1])

    def get_tax(self):
        """Parse label 'Tax: $2.59' -> 2.59."""
        text = self.get_text(self.TAX_LABEL)
        return float(text.split("$")[-1])

    def get_total(self):
        """Parse label 'Total: $34.98' -> 34.98."""
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.split("$")[-1])

    def click_finish(self):
        """Click Finish -> qua trang Complete.
        Dùng JS click vì Selenium native click hay bị race condition với React
        (đã gặp lỗi ở Finish button - click thật nhưng navigation không trigger)."""
        element = self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait_for_url_contains("checkout-complete")

    def click_cancel(self):
        """Click Cancel ở step 2 -> về thẳng Inventory (không phải Cart như step 1)."""
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url_contains("inventory.html")
