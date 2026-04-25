"""Test cases cho trang Inventory - danh sách sản phẩm (TC_INV_001 -> 019)."""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture(autouse=True)
def _login(driver, test_data):
    creds = test_data["users"]["standard_user"]
    LoginPage(driver).login(creds["username"], creds["password"])


@pytest.mark.inventory
class TestInventory:
    def test_TC_INV_001_six_products_displayed(self, driver):
        # Phải hiện đủ 6 sản phẩm
        assert InventoryPage(driver).get_product_count() == 6

    def test_TC_INV_002_page_title_products(self, driver):
        # Tiêu đề trang là 'Products'
        assert InventoryPage(driver).get_page_title() == "Products"

    def test_TC_INV_003_all_products_have_names(self, driver):
        # Mỗi sản phẩm phải có tên (không rỗng)
        names = InventoryPage(driver).get_product_names()
        assert len(names) == 6
        assert all(n.strip() for n in names)

    def test_TC_INV_004_all_products_have_prices(self, driver):
        # Mỗi sản phẩm phải có giá bắt đầu bằng '$'
        prices = InventoryPage(driver).get_product_prices_raw()
        assert len(prices) == 6
        assert all(p.startswith("$") for p in prices)

    def test_TC_INV_005_all_products_have_descriptions(self, driver):
        # Mỗi sản phẩm phải có mô tả
        descs = InventoryPage(driver).get_product_descriptions()
        assert len(descs) == 6
        assert all(d.strip() for d in descs)

    def test_TC_INV_006_all_products_have_images(self, driver):
        # Mỗi sản phẩm phải có ảnh (src khác rỗng)
        srcs = InventoryPage(driver).get_product_image_srcs()
        assert len(srcs) == 6
        assert all(s for s in srcs)

    def test_TC_INV_007_sort_name_a_to_z(self, driver):
        # Sort tên A-Z
        page = InventoryPage(driver)
        page.sort_products("az")
        names = page.get_product_names()
        assert names == sorted(names)

    def test_TC_INV_008_sort_name_z_to_a(self, driver):
        # Sort tên Z-A
        page = InventoryPage(driver)
        page.sort_products("za")
        names = page.get_product_names()
        assert names == sorted(names, reverse=True)

    def test_TC_INV_009_sort_price_low_to_high(self, driver):
        # Sort giá từ thấp đến cao
        page = InventoryPage(driver)
        page.sort_products("lohi")
        prices = page.get_product_prices()
        assert prices == sorted(prices)

    def test_TC_INV_010_sort_price_high_to_low(self, driver):
        # Sort giá từ cao đến thấp
        page = InventoryPage(driver)
        page.sort_products("hilo")
        prices = page.get_product_prices()
        assert prices == sorted(prices, reverse=True)

    def test_TC_INV_011_add_single_product_updates_badge(self, driver):
        # Add 1 sản phẩm -> cart badge = '1'
        page = InventoryPage(driver)
        page.add_first_product_to_cart()
        assert page.get_cart_badge_count() == "1"

    def test_TC_INV_012_add_multiple_products_updates_badge(self, driver):
        # Add 3 sản phẩm -> cart badge = '3'
        page = InventoryPage(driver)
        page.add_products_by_count(3)
        assert page.get_cart_badge_count() == "3"

    def test_TC_INV_013_remove_product_decreases_badge(self, driver):
        # Remove bớt 1 sản phẩm -> badge giảm tương ứng
        page = InventoryPage(driver)
        page.add_products_by_count(2)
        assert page.get_cart_badge_count() == "2"
        page.click_first_remove_button()
        assert page.get_cart_badge_count() == "1"

    def test_TC_INV_014_add_button_toggles_to_remove(self, driver):
        # Button 'Add to cart' đổi thành 'Remove' sau khi add
        page = InventoryPage(driver)
        page.add_first_product_to_cart()
        assert page.get_first_item_button_text() == "Remove"

    def test_TC_INV_015_click_product_name_navigates_to_detail(self, driver):
        # Click tên sản phẩm -> mở trang chi tiết
        page = InventoryPage(driver)
        page.click_first_product_name()
        assert "/inventory-item.html" in driver.current_url

    def test_TC_INV_016_cart_badge_hidden_when_empty(self, driver):
        # Cart rỗng -> badge không hiện
        page = InventoryPage(driver)
        assert not page.is_cart_badge_displayed()

    def test_TC_INV_017_add_all_six_products(self, driver):
        # Add hết 6 sản phẩm (max)
        page = InventoryPage(driver)
        page.add_products_by_count(6)
        assert page.get_cart_badge_count() == "6"

    def test_TC_INV_018_remove_all_products(self, driver):
        # Add 6 rồi remove hết
        page = InventoryPage(driver)
        page.add_products_by_count(6)
        while page.is_cart_badge_displayed():
            page.click_first_remove_button()
        assert not page.is_cart_badge_displayed()

    def test_TC_INV_019_sort_resets_after_detail_navigation(self, driver):
        # BUG: sort bị reset sau khi vào detail rồi back (site đáng lẽ phải persist)
        page = InventoryPage(driver)
        page.sort_products("za")
        names_before = page.get_product_names()
        assert names_before == sorted(names_before, reverse=True)

        page.click_first_product_name()
        from pages.product_detail_page import ProductDetailPage

        ProductDetailPage(driver).click_back_to_products()

        names_after = page.get_product_names()
        assert names_after == sorted(names_after)
