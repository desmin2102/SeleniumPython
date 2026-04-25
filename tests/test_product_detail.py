"""Test cases cho trang chi tiết sản phẩm (TC_PROD_001 -> 004)."""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage


@pytest.fixture(autouse=True)
def _setup(driver, test_data):
    creds = test_data["users"]["standard_user"]
    LoginPage(driver).login(creds["username"], creds["password"])


@pytest.mark.product
class TestProductDetail:
    def test_TC_PROD_001_detail_page_shows_product_info(self, driver):
        # Info bên detail khớp với info bên inventory
        inv = InventoryPage(driver)
        expected_name = inv.get_first_product_name_text()
        expected_price = inv.get_first_product_price_text()
        inv.click_first_product_name()

        detail = ProductDetailPage(driver)
        assert detail.get_name() == expected_name
        assert detail.get_price() == expected_price
        assert detail.get_description().strip() != ""
        assert detail.get_image_src() != ""

    def test_TC_PROD_002_add_to_cart_from_detail(self, driver):
        # Add to cart từ trang detail
        InventoryPage(driver).click_first_product_name()
        detail = ProductDetailPage(driver)
        detail.click_add_to_cart()
        assert detail.is_remove_visible()
        assert detail.get_cart_badge_count() == "1"

    def test_TC_PROD_003_remove_from_detail(self, driver):
        # Remove từ trang detail
        InventoryPage(driver).click_first_product_name()
        detail = ProductDetailPage(driver)
        detail.click_add_to_cart()
        detail.click_remove()
        assert detail.is_add_to_cart_visible()
        assert not detail.is_cart_badge_displayed()

    def test_TC_PROD_004_back_to_products_returns_inventory(self, driver):
        # Click 'Back to products' -> về inventory
        InventoryPage(driver).click_first_product_name()
        ProductDetailPage(driver).click_back_to_products()
        assert "/inventory.html" in driver.current_url
