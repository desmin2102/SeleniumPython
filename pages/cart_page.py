"""Page object cho trang giỏ hàng (URL: /cart.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):

    TITLE = (By.CSS_SELECTOR, ".title")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CART_ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    CART_ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def get_title_text(self):
        """Đọc tiêu đề trang."""
        return self.get_text(self.TITLE)

    def get_item_count(self):
        """Đếm số item trong giỏ."""
        return len(self.find_elements_safe(self.CART_ITEMS))

    def get_item_names(self):
        """Lấy danh sách tên sản phẩm trong giỏ."""
        return [el.text for el in self.find_elements_safe(self.CART_ITEM_NAMES)]

    def get_item_prices_raw(self):
        """Lấy danh sách giá trong giỏ (có '$')."""
        return [el.text for el in self.find_elements_safe(self.CART_ITEM_PRICES)]

    def is_empty(self):
        """Giỏ hàng có đang trống không."""
        return self.get_item_count() == 0

    def remove_first_item(self):
        """Xóa item đầu tiên trong giỏ."""
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()

    def click_checkout(self):
        """Click Checkout -> sang trang nhập thông tin."""
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("checkout-step-one")

    def click_continue_shopping(self):
        """Click Continue Shopping -> về trang danh sách sản phẩm."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_url_contains("inventory.html")
