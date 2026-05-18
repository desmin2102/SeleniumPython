"""Page object cho trang chi tiết sản phẩm (URL: /inventory-item.html)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductDetailPage(BasePage):

    PRODUCT_NAME = (By.CSS_SELECTOR, ".inventory_details_name")
    PRODUCT_DESC = (By.CSS_SELECTOR, ".inventory_details_desc")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_details_price")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".inventory_details_img")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove']")
    BACK_TO_PRODUCTS = (By.ID, "back-to-products")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def get_name(self):
        return self.get_text(self.PRODUCT_NAME)

    def get_description(self):
        return self.get_text(self.PRODUCT_DESC)

    def get_price(self):
        return self.get_text(self.PRODUCT_PRICE)

    def get_image_src(self):
        """Lấy URL ảnh sản phẩm."""
        return self.get_attribute(self.PRODUCT_IMAGE, "src")

    def click_add_to_cart(self):
        """Thêm sản phẩm vào giỏ hàng."""
        self.click(self.ADD_TO_CART_BUTTON)

    def click_remove(self):
        """Xóa sản phẩm khỏi giỏ hàng."""
        self.click(self.REMOVE_BUTTON)

    def is_remove_visible(self):
        """Nút Remove có hiện không."""
        return self.is_present(self.REMOVE_BUTTON)

    def is_add_to_cart_visible(self):
        """Nút Add to cart có hiện không."""
        return self.is_present(self.ADD_TO_CART_BUTTON)

    def click_back_to_products(self):
        """Quay về trang danh sách sản phẩm."""
        self.click(self.BACK_TO_PRODUCTS)

    def get_cart_badge_count(self):
        return self.get_text(self.CART_BADGE)

    def is_cart_badge_displayed(self):
        return self.is_present(self.CART_BADGE)
