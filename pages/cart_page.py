"""Page object cho trang giỏ hàng (URL: /cart.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    """
    Trang giỏ hàng - hiện danh sách item đã add từ inventory.
    Có 2 nút điều hướng: Continue Shopping (về lại inventory) và Checkout (qua step 1).
    """

    TITLE = (By.CSS_SELECTOR, ".title")  # "Your Cart"
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")  # Mỗi dòng item trong cart
    CART_ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    CART_ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")  # Nút Remove từng item
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def get_title_text(self):
        """Đọc tiêu đề trang - phải là 'Your Cart'."""
        return self.get_text(self.TITLE)

    def get_item_count(self):
        """Đếm số item trong cart. Dùng find_elements_safe để tránh chờ 15s khi cart rỗng."""
        return len(self.find_elements_safe(self.CART_ITEMS))

    def get_item_names(self):
        """Lấy list tên sản phẩm đang có trong cart."""
        return [el.text for el in self.find_elements_safe(self.CART_ITEM_NAMES)]

    def get_item_prices_raw(self):
        """Lấy list giá sản phẩm dạng chuỗi (có '$') - dùng để so sánh với giá bên inventory."""
        return [el.text for el in self.find_elements_safe(self.CART_ITEM_PRICES)]

    def is_empty(self):
        """Cart có rỗng không - dùng sau khi remove hết items hoặc sau khi order xong."""
        return self.get_item_count() == 0

    def remove_first_item(self):
        """Remove item đầu tiên trong cart."""
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()

    def click_checkout(self):
        """Click Checkout -> chuyển sang trang nhập thông tin (step 1).
        Có wait URL để chắc chắn page đã navigate xong trước khi trả về."""
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("checkout-step-one")

    def click_continue_shopping(self):
        """Click Continue Shopping -> quay về Inventory."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_url_contains("inventory.html")
