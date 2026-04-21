"""Test cases cho URL Security - truy cập trực tiếp URL khi chưa login (TC_URL_001 -> 003)."""

import pytest
from pages.login_page import LoginPage


@pytest.mark.security
class TestUrlSecurity:

    def test_TC_URL_001_direct_inventory_without_login(self, driver):
        # Vào thẳng /inventory.html khi chưa login -> bị block
        driver.get("https://www.saucedemo.com/inventory.html")
        lp = LoginPage(driver)
        assert lp.is_error_displayed()
        error = lp.get_error_message().lower()
        assert "inventory.html" in error and "logged in" in error

    def test_TC_URL_002_direct_cart_without_login(self, driver):
        # Vào thẳng /cart.html khi chưa login -> bị block
        driver.get("https://www.saucedemo.com/cart.html")
        lp = LoginPage(driver)
        assert lp.is_error_displayed()
        error = lp.get_error_message().lower()
        assert "cart.html" in error and "logged in" in error

    def test_TC_URL_003_direct_checkout_complete_without_login(self, driver):
        # Vào thẳng /checkout-complete.html khi chưa login -> bị block
        driver.get("https://www.saucedemo.com/checkout-complete.html")
        lp = LoginPage(driver)
        assert lp.is_error_displayed()
        error = lp.get_error_message().lower()
        assert "checkout-complete.html" in error and "logged in" in error
