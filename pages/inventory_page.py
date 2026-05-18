"""Page object cho trang danh sách sản phẩm (URL: /inventory.html)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):

    TITLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_DESCRIPTIONS = (By.CSS_SELECTOR, ".inventory_item_desc")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ITEM_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".product_sort_container")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    FIRST_ITEM_BUTTON = (By.CSS_SELECTOR, ".inventory_item button")

    def get_page_title(self):
        """Lấy tiêu đề trang."""
        return self.get_text(self.TITLE)

    def get_product_count(self):
        """Đếm số sản phẩm đang hiển thị."""
        return len(self.find_elements(self.INVENTORY_ITEMS))

    def get_product_names(self):
        """Lấy danh sách tên sản phẩm."""
        return [el.text for el in self.find_elements(self.ITEM_NAMES)]

    def get_product_descriptions(self):
        return [el.text for el in self.find_elements(self.ITEM_DESCRIPTIONS)]

    def get_product_prices_raw(self):
        """Lấy danh sách giá dạng string có '$'."""
        return [el.text for el in self.find_elements(self.ITEM_PRICES)]

    def get_product_prices(self):
        """Lấy danh sách giá dạng float."""
        return [float(p.replace("$", "")) for p in self.get_product_prices_raw()]

    def get_product_image_srcs(self):
        """Lấy URL ảnh của tất cả sản phẩm."""
        return [el.get_attribute("src") for el in self.find_elements(self.ITEM_IMAGES)]

    def sort_products(self, value):
        """Chọn option sort: 'az', 'za', 'lohi', 'hilo'."""
        Select(self.find_element(self.SORT_DROPDOWN)).select_by_value(value)

    def add_first_product_to_cart(self):
        """Click Add to cart của sản phẩm đầu tiên."""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if buttons:
            buttons[0].click()

    def add_products_by_count(self, count):
        """Add count sản phẩm vào cart liên tiếp."""
        for _ in range(count):
            buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
            if not buttons:
                break
            buttons[0].click()

    def click_first_remove_button(self):
        """Click Remove của sản phẩm đầu tiên đã add."""
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()

    def get_first_item_button_text(self):
        """Lấy text nút của sản phẩm đầu tiên."""
        return self.find_element(self.FIRST_ITEM_BUTTON).text

    def get_cart_badge_count(self):
        """Đọc số trên cart badge."""
        return self.get_text(self.CART_BADGE)

    def is_cart_badge_displayed(self):
        """Cart badge có hiện không."""
        return self.is_present(self.CART_BADGE)

    def go_to_cart(self):
        """Click icon cart -> sang trang giỏ hàng."""
        self.click(self.CART_LINK)

    def click_first_product_name(self):
        """Click tên sản phẩm đầu tiên -> vào trang chi tiết."""
        self.find_elements(self.ITEM_NAMES)[0].click()

    def get_first_product_name_text(self):
        return self.find_elements(self.ITEM_NAMES)[0].text

    def get_first_product_price_text(self):
        return self.find_elements(self.ITEM_PRICES)[0].text
