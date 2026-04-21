"""Page object cho menu hamburger (xuất hiện trên mọi trang sau khi login)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class MenuPage(BasePage):
    """
    Menu bên trái, mở ra khi click icon 3-gạch (hamburger) ở góc trái.
    Có 4 link: All Items, About, Logout, Reset App State.
    """

    BURGER_BUTTON = (By.ID, "react-burger-menu-btn")             # Icon 3 gạch
    MENU_WRAPPER = (By.CSS_SELECTOR, ".bm-menu-wrap")            # Container sidebar menu
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK = (By.ID, "about_sidebar_link")                   # Link ra trang saucelabs.com
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")         # Reset cart, sort về default
    CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")             # Nút X đóng menu

    def open(self):
        """Mở menu bằng cách click burger icon.
        Chờ link All Items hiện lên mới return (đảm bảo menu đã mở xong animation)."""
        self.click(self.BURGER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.ALL_ITEMS_LINK))

    def close(self):
        """Đóng menu bằng cách click nút X.
        Dùng JS click vì animation của menu có thể cover nút X -> click thường fail."""
        element = self.wait.until(EC.element_to_be_clickable(self.CLOSE_BUTTON))
        self.driver.execute_script("arguments[0].click();", element)

    def is_open(self):
        """Kiểm tra menu đang mở không.
        Dựa vào attribute aria-hidden của wrapper:
        - aria-hidden='true' -> đã đóng
        - aria-hidden='false' hoặc không có -> đang mở."""
        if not self.is_present(self.MENU_WRAPPER):
            return False
        aria_hidden = self.driver.find_element(*self.MENU_WRAPPER).get_attribute("aria-hidden")
        return aria_hidden != "true"

    def click_all_items(self):
        """Click 'All Items' -> về Inventory.
        Dùng JS click vì link có thể bị animation sidebar che."""
        element = self.wait.until(EC.element_to_be_clickable(self.ALL_ITEMS_LINK))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait_for_url_contains("inventory.html")

    def click_logout(self):
        """Click Logout -> về trang login."""
        element = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        self.driver.execute_script("arguments[0].click();", element)

    def click_reset_app_state(self):
        """Click Reset App State -> xóa cart, reset sort về default."""
        element = self.wait.until(EC.element_to_be_clickable(self.RESET_APP_STATE_LINK))
        self.driver.execute_script("arguments[0].click();", element)

    def is_all_items_visible(self):
        """Link 'All Items' có hiện không - dùng để verify menu đã mở."""
        return self.is_displayed(self.ALL_ITEMS_LINK)
