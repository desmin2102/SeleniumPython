"""Test cases cho menu hamburger (TC_MENU_001 -> 005)."""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_page import MenuPage


@pytest.fixture(autouse=True)
def _login(driver, test_data):
    creds = test_data["users"]["standard_user"]
    LoginPage(driver).login(creds["username"], creds["password"])


@pytest.mark.menu
class TestMenu:
    def test_TC_MENU_001_hamburger_menu_opens(self, driver):
        # Click icon hamburger -> menu hiện ra
        menu = MenuPage(driver)
        menu.open()
        assert menu.is_all_items_visible()

    def test_TC_MENU_002_all_items_link_navigates_to_inventory(self, driver):
        # Click 'All Items' -> về inventory
        inv = InventoryPage(driver)
        inv.click_first_product_name()
        menu = MenuPage(driver)
        menu.open()
        menu.click_all_items()
        assert "/inventory.html" in driver.current_url

    def test_TC_MENU_003_logout_link_logs_out(self, driver):
        # Click Logout -> về trang login
        menu = MenuPage(driver)
        menu.open()
        menu.click_logout()
        assert LoginPage(driver).is_login_page()

    def test_TC_MENU_004_reset_app_state_clears_cart(self, driver):
        # Click 'Reset App State' -> cart bị xóa
        inv = InventoryPage(driver)
        inv.add_products_by_count(2)
        menu = MenuPage(driver)
        menu.open()
        menu.click_reset_app_state()
        menu.close()
        inv.go_to_cart()
        from pages.cart_page import CartPage

        assert CartPage(driver).is_empty()

    def test_TC_MENU_005_menu_closes_via_x(self, driver):
        # Click nút X -> menu đóng (close() đã chờ animation xong)
        menu = MenuPage(driver)
        menu.open()
        menu.close()
        assert not menu.is_open()
