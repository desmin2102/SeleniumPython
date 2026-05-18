"""Test cases cho luồng Checkout."""

import pytest

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step1_page import CheckoutStep1Page
from pages.checkout_step2_page import CheckoutStep2Page
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def go_to_checkout_step_one(driver, test_data, item_count=1):
    # Login + thêm sản phẩm + vào trang checkout step 1
    creds = test_data["users"]["standard_user"]
    LoginPage(driver).login(creds["username"], creds["password"])
    inv = InventoryPage(driver)
    inv.add_products_by_count(item_count)
    inv.go_to_cart()
    CartPage(driver).click_checkout()


def go_to_checkout_step_two(driver, test_data, item_count=1):
    # Tiếp tục từ step 1, điền thông tin và qua step 2
    go_to_checkout_step_one(driver, test_data, item_count)
    info = test_data["checkout_info"]
    step1 = CheckoutStep1Page(driver)
    step1.fill_info(info["first_name"], info["last_name"], info["postal_code"])
    step1.click_continue_and_wait()


@pytest.mark.checkout
class TestCheckoutStep1:
    def test_TC_CHK1_001_valid_info_proceeds_to_step_two(self, driver, test_data):
        # Nhập thông tin hợp lệ -> qua được Step 2
        go_to_checkout_step_one(driver, test_data)
        info = test_data["checkout_info"]
        step1 = CheckoutStep1Page(driver)
        step1.fill_info(info["first_name"], info["last_name"], info["postal_code"])
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_002_empty_first_name_error(self, driver, test_data):
        # Trống First Name -> báo lỗi
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("", "Doe", "1234")
        step1.click_continue()
        assert step1.is_error_displayed()
        assert "first name is required" in step1.get_error_message().lower()

    def test_TC_CHK1_003_empty_last_name_error(self, driver, test_data):
        # Trống Last Name -> báo lỗi
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "", "1234")
        step1.click_continue()
        assert step1.is_error_displayed()
        assert "last name is required" in step1.get_error_message().lower()

    def test_TC_CHK1_004_empty_postal_code_error(self, driver, test_data):
        # Trống Postal Code -> báo lỗi
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "Doe", "")
        step1.click_continue()
        assert step1.is_error_displayed()
        assert "postal code is required" in step1.get_error_message().lower()

    def test_TC_CHK1_005_cancel_returns_to_cart(self, driver, test_data):
        # Click Cancel -> về trang Cart
        go_to_checkout_step_one(driver, test_data)
        CheckoutStep1Page(driver).click_cancel()
        assert "/cart.html" in driver.current_url

    def test_TC_CHK1_006_title_text(self, driver, test_data):
        # Title trang là 'Checkout: Your Information'
        go_to_checkout_step_one(driver, test_data)
        assert CheckoutStep1Page(driver).get_title_text() == "Checkout: Your Information"

    def test_TC_CHK1_007_very_long_first_name(self, driver, test_data):
        # First name 200 ký tự vẫn được chấp nhận
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("a" * 200, "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_008_special_chars_first_name(self, driver, test_data):
        # First name toàn ký tự đặc biệt vẫn được chấp nhận
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("!@#$%^&*", "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_009_whitespace_only_first_name_accepted(self, driver, test_data):
        # BUG: First name chỉ có khoảng trắng vẫn qua được bước 2
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("   ", "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_010_unicode_first_name(self, driver, test_data):
        # First name có ký tự Unicode (tiếng Việt, tiếng Nhật...)
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("Nguyễn", "Doe", "1234")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_011_letters_in_postal_code(self, driver, test_data):
        # Postal code toàn chữ cái vẫn được chấp nhận
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "Doe", "abcd")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url

    def test_TC_CHK1_012_special_chars_postal_code(self, driver, test_data):
        # Postal code có ký tự đặc biệt vẫn được chấp nhận
        go_to_checkout_step_one(driver, test_data)
        step1 = CheckoutStep1Page(driver)
        step1.fill_info("John", "Doe", "!@#$")
        step1.click_continue_and_wait()
        assert "/checkout-step-two.html" in driver.current_url


@pytest.mark.checkout
class TestCheckoutStep2:
    def test_TC_CHK2_001_items_displayed_in_overview(self, driver, test_data):
        # Overview hiện đủ số items đã add vào cart
        go_to_checkout_step_two(driver, test_data, item_count=2)
        assert CheckoutStep2Page(driver).get_item_count() == 2

    def test_TC_CHK2_002_payment_info_displayed(self, driver, test_data):
        # Có section 'Payment Information'
        go_to_checkout_step_two(driver, test_data)
        assert CheckoutStep2Page(driver).is_payment_info_displayed()

    def test_TC_CHK2_003_shipping_info_displayed(self, driver, test_data):
        # Có section 'Shipping Information'
        go_to_checkout_step_two(driver, test_data)
        assert CheckoutStep2Page(driver).is_shipping_info_displayed()

    def test_TC_CHK2_004_subtotal_equals_sum_of_items(self, driver, test_data):
        # Item total = tổng giá các items
        go_to_checkout_step_two(driver, test_data, item_count=2)
        step2 = CheckoutStep2Page(driver)
        assert step2.get_subtotal() == sum(step2.get_item_prices())

    def test_TC_CHK2_005_total_equals_subtotal_plus_tax(self, driver, test_data):
        # Total = Subtotal + Tax
        go_to_checkout_step_two(driver, test_data)
        step2 = CheckoutStep2Page(driver)
        assert step2.get_total() == round(step2.get_subtotal() + step2.get_tax(), 2)

    def test_TC_CHK2_006_finish_navigates_to_complete(self, driver, test_data):
        # Click Finish -> qua trang Complete
        go_to_checkout_step_two(driver, test_data)
        CheckoutStep2Page(driver).click_finish()
        assert "/checkout-complete.html" in driver.current_url

    def test_TC_CHK2_007_cancel_returns_to_inventory(self, driver, test_data):
        # Click Cancel ở Step 2 -> về Inventory
        go_to_checkout_step_two(driver, test_data)
        CheckoutStep2Page(driver).click_cancel()
        assert "/inventory.html" in driver.current_url


@pytest.mark.checkout
class TestCheckoutComplete:
    def test_TC_CHK3_001_success_message_displayed(self, driver, test_data):
        # Hiện thông báo 'Thank you for your order!'
        go_to_checkout_step_two(driver, test_data)
        CheckoutStep2Page(driver).click_finish()
        assert CheckoutCompletePage(driver).get_complete_header() == "Thank you for your order!"

    def test_TC_CHK3_002_pony_express_image_displayed(self, driver, test_data):
        # Có ảnh Pony Express
        go_to_checkout_step_two(driver, test_data)
        CheckoutStep2Page(driver).click_finish()
        assert CheckoutCompletePage(driver).is_pony_express_image_displayed()

    def test_TC_CHK3_003_back_home_returns_to_inventory(self, driver, test_data):
        # Click 'Back Home' -> về Inventory
        go_to_checkout_step_two(driver, test_data)
        CheckoutStep2Page(driver).click_finish()
        CheckoutCompletePage(driver).click_back_home()
        assert "/inventory.html" in driver.current_url

    def test_TC_CHK3_004_cart_empty_after_order(self, driver, test_data):
        # Cart rỗng sau khi đặt hàng xong
        go_to_checkout_step_two(driver, test_data)
        CheckoutStep2Page(driver).click_finish()
        CheckoutCompletePage(driver).click_back_home()
        assert not InventoryPage(driver).is_cart_badge_displayed()
