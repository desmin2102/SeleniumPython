"""Test cases cho luồng Checkout - Step 1, Step 2, Complete (TC_CHK1/2/3_0xx)."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step1_page import CheckoutStep1Page
from pages.checkout_step2_page import CheckoutStep2Page
from pages.checkout_complete_page import CheckoutCompletePage


def _go_to_checkout_step_one(driver, item_count=1):
    # Helper: login + add sản phẩm + vào trang nhập thông tin giao hàng
    LoginPage(driver).login("standard_user", "secret_sauce")
    inv = InventoryPage(driver)
    inv.add_products_by_count(item_count)
    inv.go_to_cart()
    CartPage(driver).click_checkout()


def _go_to_checkout_step_two(driver, item_count=1):
    # Helper: qua luôn Step 2 (overview) với data hợp lệ
    _go_to_checkout_step_one(driver, item_count)
    step1 = CheckoutStep1Page(driver)
    step1.fill_info("John", "Doe", "1234")
    step1.click_continue_and_wait()


@pytest.mark.checkout
class TestCheckoutStep1:

    def test_TC_CHK1_001_valid_info_proceeds_to_step_two(self, driver):
        # Nhập thông tin hợp lệ -> qua được Step 2
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_002_empty_first_name_error(self, driver):
        # Trống First Name -> báo lỗi
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("", "Doe", "1234")
        step1.click_continue()
        assert step1.is_error_displayed()
        assert "first name is required" in step1.get_error_message().lower()

    def test_TC_CHK1_003_empty_last_name_error(self, driver):
        # Trống Last Name -> báo lỗi
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "", "1234")
        step1.click_continue()
        assert step1.is_error_displayed()
        assert "last name is required" in step1.get_error_message().lower()

    def test_TC_CHK1_004_empty_postal_code_error(self, driver):
        # Trống Postal Code -> báo lỗi
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "Doe", "")
        step1.click_continue()
        assert step1.is_error_displayed()
        assert "postal code is required" in step1.get_error_message().lower()

    def test_TC_CHK1_005_cancel_returns_to_cart(self, driver):
        # Click Cancel -> về trang Cart
        _go_to_checkout_step_one(driver)
        CheckoutStep1Page(driver).click_cancel()
        assert "/cart.html" in driver.current_url

    def test_TC_CHK1_006_title_text(self, driver):
        # Title trang là 'Checkout: Your Information'
        _go_to_checkout_step_one(driver)
        assert CheckoutStep1Page(driver).get_title_text() == "Checkout: Your Information"

    def test_TC_CHK1_007_very_long_first_name(self, driver):
        # First name 200 ký tự vẫn được chấp nhận
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("a" * 200, "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_008_special_chars_first_name(self, driver):
        # First name toàn ký tự đặc biệt vẫn được chấp nhận
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("!@#$%^&*", "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_009_whitespace_only_first_name_accepted(self, driver):
        # BUG: First name chỉ chứa khoảng trắng vẫn pass (đáng lẽ phải reject)
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("   ", "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_010_unicode_first_name(self, driver):
        # First name có Unicode + emoji (dùng JS vì send_keys không gõ được emoji)
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.js_set_value(step1.FIRST_NAME_INPUT, "Jöhn😀")
        step1.send_keys(step1.LAST_NAME_INPUT, "Doe")
        step1.send_keys(step1.POSTAL_CODE_INPUT, "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_011_letters_in_postal_code(self, driver):
        # Postal code toàn chữ cái vẫn được chấp nhận
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "Doe", "abcd")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_012_special_chars_postal_code(self, driver):
        # Postal code có ký tự đặc biệt vẫn được chấp nhận
        _go_to_checkout_step_one(driver)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "Doe", "!@#$")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url


@pytest.mark.checkout
class TestCheckoutStep2:

    def test_TC_CHK2_001_items_displayed_in_overview(self, driver):
        # Overview hiện đủ số items đã add vào cart
        _go_to_checkout_step_two(driver, item_count=2)
        assert CheckoutStep2Page(driver).get_item_count() == 2

    def test_TC_CHK2_002_payment_info_displayed(self, driver):
        # Có section 'Payment Information'
        _go_to_checkout_step_two(driver)
        assert CheckoutStep2Page(driver).is_payment_info_displayed()

    def test_TC_CHK2_003_shipping_info_displayed(self, driver):
        # Có section 'Shipping Information'
        _go_to_checkout_step_two(driver)
        assert CheckoutStep2Page(driver).is_shipping_info_displayed()

    def test_TC_CHK2_004_subtotal_equals_sum_of_items(self, driver):
        # Item total = tổng giá các items
        _go_to_checkout_step_two(driver, item_count=2)
        step2 = CheckoutStep2Page(driver)
        prices_sum = round(sum(step2.get_item_prices()), 2)
        assert round(step2.get_subtotal(), 2) == prices_sum

    def test_TC_CHK2_005_total_equals_subtotal_plus_tax(self, driver):
        # Total = Subtotal + Tax
        _go_to_checkout_step_two(driver)
        step2 = CheckoutStep2Page(driver)
        expected = round(step2.get_subtotal() + step2.get_tax(), 2)
        assert round(step2.get_total(), 2) == expected

    def test_TC_CHK2_006_finish_navigates_to_complete(self, driver):
        # Click Finish -> qua trang Complete
        _go_to_checkout_step_two(driver)
        CheckoutStep2Page(driver).click_finish()
        assert "/checkout-complete.html" in driver.current_url

    def test_TC_CHK2_007_cancel_returns_to_inventory(self, driver):
        # Click Cancel ở Step 2 -> về Inventory
        _go_to_checkout_step_two(driver)
        CheckoutStep2Page(driver).click_cancel()
        assert "/inventory.html" in driver.current_url


@pytest.mark.checkout
class TestCheckoutComplete:

    def test_TC_CHK3_001_success_message_displayed(self, driver):
        # Hiện thông báo 'Thank you for your order!'
        _go_to_checkout_step_two(driver)
        CheckoutStep2Page(driver).click_finish()
        assert CheckoutCompletePage(driver).get_complete_header() == "Thank you for your order!"

    def test_TC_CHK3_002_pony_express_image_displayed(self, driver):
        # Có ảnh Pony Express
        _go_to_checkout_step_two(driver)
        CheckoutStep2Page(driver).click_finish()
        assert CheckoutCompletePage(driver).is_pony_express_image_displayed()

    def test_TC_CHK3_003_back_home_returns_to_inventory(self, driver):
        # Click 'Back Home' -> về Inventory
        _go_to_checkout_step_two(driver)
        CheckoutStep2Page(driver).click_finish()
        CheckoutCompletePage(driver).click_back_home()
        assert "/inventory.html" in driver.current_url

    def test_TC_CHK3_004_cart_empty_after_order(self, driver):
        # Cart rỗng sau khi đặt hàng xong
        _go_to_checkout_step_two(driver)
        CheckoutStep2Page(driver).click_finish()
        CheckoutCompletePage(driver).click_back_home()
        assert not InventoryPage(driver).is_cart_badge_displayed()
