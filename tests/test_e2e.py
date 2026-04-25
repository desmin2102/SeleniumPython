"""End-to-End test cases - luồng mua hàng đầy đủ (TC_E2E_001, 002)."""

import pytest

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step1_page import CheckoutStep1Page
from pages.checkout_step2_page import CheckoutStep2Page
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.e2e
class TestEndToEnd:
    def test_TC_E2E_001_full_purchase_flow(self, driver, test_data):
        # Luồng mua 1 sản phẩm đầy đủ: login -> add -> cart -> checkout -> finish
        creds = test_data["users"]["standard_user"]
        info = test_data["checkout_info"]

        LoginPage(driver).login(creds["username"], creds["password"])
        inv = InventoryPage(driver)
        inv.add_first_product_to_cart()
        inv.go_to_cart()
        CartPage(driver).click_checkout()

        step1 = CheckoutStep1Page(driver)
        step1.fill_info(info["first_name"], info["last_name"], info["postal_code"])
        step1.click_continue_and_wait()

        CheckoutStep2Page(driver).click_finish()
        complete = CheckoutCompletePage(driver)
        assert complete.get_complete_header() == "Thank you for your order!"

        complete.click_back_home()
        assert not inv.is_cart_badge_displayed()

    def test_TC_E2E_002_multi_item_purchase(self, driver, test_data):
        # Luồng mua nhiều sản phẩm (3 items) - dùng checkout_info_alt để verify khác user
        creds = test_data["users"]["standard_user"]
        info = test_data["checkout_info_alt"]

        LoginPage(driver).login(creds["username"], creds["password"])
        inv = InventoryPage(driver)
        inv.add_products_by_count(3)
        inv.go_to_cart()
        CartPage(driver).click_checkout()

        step1 = CheckoutStep1Page(driver)
        step1.fill_info(info["first_name"], info["last_name"], info["postal_code"])
        step1.click_continue_and_wait()

        step2 = CheckoutStep2Page(driver)
        assert step2.get_item_count() == 3
        step2.click_finish()

        assert CheckoutCompletePage(driver).get_complete_header() == "Thank you for your order!"
