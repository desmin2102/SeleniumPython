"""Page object cho menu hamburger (xuất hiện trên mọi trang sau khi login)."""

import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MenuPage(BasePage):

    BURGER_BUTTON = (By.ID, "react-burger-menu-btn")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")
    CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")

    def open(self):
        """Mở menu bằng cách click burger icon."""
        self.click(self.BURGER_BUTTON)
        self.wait_for_element_visible(self.ALL_ITEMS_LINK)

    def close(self):
        """Đóng menu bằng cách click nút X."""
        self.click(self.CLOSE_BUTTON)
        time.sleep(0.5)

    def is_open(self):
        """Kiểm tra menu đang mở hay không."""
        return self.is_displayed(self.ALL_ITEMS_LINK)

    def click_all_items(self):
        """Click 'All Items' -> về trang inventory."""
        self.click(self.ALL_ITEMS_LINK)
        self.wait_for_url_contains("inventory.html")

    def click_logout(self):
        """Click Logout -> về trang login."""
        self.click(self.LOGOUT_LINK)

    def click_reset_app_state(self):
        """Click Reset App State -> xóa cart."""
        self.click(self.RESET_APP_STATE_LINK)

    def is_all_items_visible(self):
        """Kiểm tra link All Items có hiển thị không."""
        return self.is_displayed(self.ALL_ITEMS_LINK)
