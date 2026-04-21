"""Test cases cho trang Cart (TC_CART_001 -> 007)."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.fixture(autouse=True)
def _login(driver):
    LoginPage(driver).login("standard_user", "secret_sauce")


@pytest.mark.cart
class TestCart:

    def test_TC_CART_001_navigate_to_cart(self, driver):
        # Click icon cart -> vào trang cart, title là 'Your Cart'
        InventoryPage(driver).go_to_cart()
        assert "/cart.html" in driver.current_url
        assert CartPage(driver).get_title_text() == "Your Cart"

    def test_TC_CART_002_items_display_after_adding(self, driver):
        # Add 2 sản phẩm -> cart hiện đủ 2 items
        inv = InventoryPage(driver)
        inv.add_products_by_count(2)
        inv.go_to_cart()
        assert CartPage(driver).get_item_count() == 2

    def test_TC_CART_003_remove_item_from_cart(self, driver):
        # Remove item trong cart -> cart rỗng
        inv = InventoryPage(driver)
        inv.add_first_product_to_cart()
        inv.go_to_cart()
        cart = CartPage(driver)
        cart.remove_first_item()
        assert cart.is_empty()

    def test_TC_CART_004_continue_shopping_returns_inventory(self, driver):
        # Click 'Continue Shopping' -> quay về inventory
        InventoryPage(driver).go_to_cart()
        CartPage(driver).click_continue_shopping()
        assert "/inventory.html" in driver.current_url

    def test_TC_CART_005_checkout_navigates_to_step_one(self, driver):
        # Click Checkout -> qua trang nhập thông tin (step 1)
        inv = InventoryPage(driver)
        inv.add_first_product_to_cart()
        inv.go_to_cart()
        CartPage(driver).click_checkout()
        assert "/checkout-step-one.html" in driver.current_url

    def test_TC_CART_006_cart_price_matches_inventory(self, driver):
        # Giá trong cart phải khớp với giá ở inventory
        inv = InventoryPage(driver)
        inventory_price = inv.get_first_product_price_text()
        inv.add_first_product_to_cart()
        inv.go_to_cart()
        cart_prices = CartPage(driver).get_item_prices_raw()
        assert cart_prices[0] == inventory_price

    def test_TC_CART_007_empty_cart_shows_no_items(self, driver):
        # Cart rỗng không có item nào
        InventoryPage(driver).go_to_cart()
        assert CartPage(driver).get_item_count() == 0
