"""Page object cho trang Inventory - danh sách sản phẩm (URL: /inventory.html)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """
    Trang danh sách sản phẩm sau khi login thành công.
    Có 6 sản phẩm cố định, dropdown sort, icon cart ở góc phải.
    """

    # Locator cho các element chính trên trang
    TITLE = (By.CSS_SELECTOR, ".title")  # Tiêu đề "Products"
    INVENTORY_LIST = (By.CSS_SELECTOR, ".inventory_list")  # Container chứa tất cả sản phẩm
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")  # Mỗi card sản phẩm
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")  # Tên sản phẩm (là link)
    ITEM_DESCRIPTIONS = (By.CSS_SELECTOR, ".inventory_item_desc")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ITEM_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".product_sort_container")  # Dropdown sort A-Z, giá
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")  # Số hiển thị trên icon cart
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")  # Icon cart ở góc phải
    # Dùng selector prefix "add-to-cart" và "remove" vì id dạng "add-to-cart-sauce-labs-backpack"
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    FIRST_ITEM_BUTTON = (By.CSS_SELECTOR, ".inventory_item button")

    # ---------- Đọc thông tin sản phẩm ----------

    def get_page_title(self):
        """Tiêu đề trang - phải là 'Products' sau khi login thành công."""
        return self.get_text(self.TITLE)

    def get_product_count(self):
        """Đếm số lượng sản phẩm đang hiển thị (SauceDemo có 6 sản phẩm)."""
        return len(self.find_elements(self.INVENTORY_ITEMS))

    def get_product_names(self):
        """Lấy list tên tất cả sản phẩm - dùng để verify sort A-Z."""
        return [el.text for el in self.find_elements(self.ITEM_NAMES)]

    def get_product_descriptions(self):
        return [el.text for el in self.find_elements(self.ITEM_DESCRIPTIONS)]

    def get_product_prices_raw(self):
        """Lấy list giá dạng chuỗi có '$' (ví dụ: '$29.99')."""
        return [el.text for el in self.find_elements(self.ITEM_PRICES)]

    def get_product_prices(self):
        """Lấy list giá dạng float (bỏ '$') - dùng để verify sort theo giá."""
        return [float(p.replace("$", "")) for p in self.get_product_prices_raw()]

    def get_product_image_srcs(self):
        """Lấy URL ảnh của tất cả sản phẩm - dùng để verify ảnh load được."""
        return [el.get_attribute("src") for el in self.find_elements(self.ITEM_IMAGES)]

    # ---------- Sort ----------

    def sort_products(self, value):
        """Chọn option sort từ dropdown. Các giá trị:
        - 'az'   : Name A to Z (default)
        - 'za'   : Name Z to A
        - 'lohi' : Price low to high
        - 'hilo' : Price high to low
        """
        Select(self.find_element(self.SORT_DROPDOWN)).select_by_value(value)

    # ---------- Thao tác cart ----------

    def add_first_product_to_cart(self):
        """Click nút Add to cart của sản phẩm ĐẦU TIÊN có nút này.
        Lưu ý: không phải sản phẩm đầu của danh sách vì sản phẩm đã add
        sẽ đổi button thành 'Remove', không match selector 'add-to-cart' nữa."""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if buttons:
            buttons[0].click()

    def add_product_by_index(self, index):
        """Add sản phẩm ở vị trí thứ index trong list các nút 'Add to cart' còn lại."""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(buttons):
            buttons[index].click()

    def add_products_by_count(self, count):
        """Add count sản phẩm liên tiếp vào cart.
        QUAN TRỌNG: phải tìm lại buttons sau mỗi lần click vì DOM bị re-render
        (button Add to cart đổi thành Remove -> list bị thay đổi)."""
        for _ in range(count):
            buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
            if not buttons:
                break
            buttons[0].click()

    def click_first_remove_button(self):
        """Click nút Remove của sản phẩm đầu tiên đã add vào cart."""
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()

    def get_first_item_button_text(self):
        """Lấy text nút của sản phẩm đầu tiên - dùng để verify toggle Add<->Remove."""
        return self.find_element(self.FIRST_ITEM_BUTTON).text

    def get_cart_badge_count(self):
        """Đọc số trên cart badge (vd: '1', '3')."""
        return self.get_text(self.CART_BADGE)

    def is_cart_badge_displayed(self):
        """Cart badge có hiện không (không hiện khi cart rỗng)."""
        return self.is_present(self.CART_BADGE)

    def go_to_cart(self):
        """Click icon cart ở góc phải -> chuyển sang /cart.html."""
        self.click(self.CART_LINK)

    # ---------- Điều hướng sang product detail ----------

    def click_first_product_name(self):
        """Click vào tên sản phẩm đầu tiên -> mở trang chi tiết."""
        self.find_elements(self.ITEM_NAMES)[0].click()

    def get_first_product_name_text(self):
        return self.find_elements(self.ITEM_NAMES)[0].text

    def get_first_product_price_text(self):
        return self.find_elements(self.ITEM_PRICES)[0].text
