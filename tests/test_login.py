"""Test cases cho chức năng Login (TC_LOGIN_001 -> 020)."""

import pytest
from pages.login_page import LoginPage


@pytest.mark.login
class TestLogin:

    def test_TC_LOGIN_001_valid_standard_user(self, driver):
        # Login thành công với standard_user
        LoginPage(driver).login("standard_user", "secret_sauce")
        assert "/inventory.html" in driver.current_url

    def test_TC_LOGIN_002_locked_out_user(self, driver):
        # Login với user bị khóa phải báo lỗi
        lp = LoginPage(driver)
        lp.login("locked_out_user", "secret_sauce")
        assert lp.is_error_displayed()
        assert "locked out" in lp.get_error_message().lower()

    def test_TC_LOGIN_003_problem_user_can_login(self, driver):
        # problem_user vẫn login được (dù UI bị bug)
        LoginPage(driver).login("problem_user", "secret_sauce")
        assert "/inventory.html" in driver.current_url

    def test_TC_LOGIN_004_performance_glitch_user_can_login(self, driver):
        # performance_glitch_user login được (dù bị delay)
        LoginPage(driver).login("performance_glitch_user", "secret_sauce")
        assert "/inventory.html" in driver.current_url

    def test_TC_LOGIN_005_error_user_can_login(self, driver):
        # error_user login được
        LoginPage(driver).login("error_user", "secret_sauce")
        assert "/inventory.html" in driver.current_url

    def test_TC_LOGIN_006_visual_user_can_login(self, driver):
        # visual_user login được
        LoginPage(driver).login("visual_user", "secret_sauce")
        assert "/inventory.html" in driver.current_url

    def test_TC_LOGIN_007_invalid_password(self, driver):
        # Sai password phải báo lỗi
        lp = LoginPage(driver)
        lp.login("standard_user", "wrong_password")
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_008_invalid_username(self, driver):
        # Username không tồn tại phải báo lỗi
        lp = LoginPage(driver)
        lp.login("invalid_user", "secret_sauce")
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_009_empty_username(self, driver):
        # Để trống username phải báo "Username is required"
        lp = LoginPage(driver)
        lp.login("", "secret_sauce")
        assert lp.is_error_displayed()
        assert "username is required" in lp.get_error_message().lower()

    def test_TC_LOGIN_010_empty_password(self, driver):
        # Để trống password phải báo "Password is required"
        lp = LoginPage(driver)
        lp.login("standard_user", "")
        assert lp.is_error_displayed()
        assert "password is required" in lp.get_error_message().lower()

    def test_TC_LOGIN_011_both_empty(self, driver):
        # Để trống cả 2 field
        lp = LoginPage(driver)
        lp.login("", "")
        assert lp.is_error_displayed()
        assert "username is required" in lp.get_error_message().lower()

    def test_TC_LOGIN_012_password_field_masked(self, driver):
        # Password field phải ẩn ký tự (type='password')
        lp = LoginPage(driver)
        assert lp.get_password_input_type() == "password"

    def test_TC_LOGIN_013_error_dismissible_via_X(self, driver):
        # Error message có thể đóng bằng nút X
        lp = LoginPage(driver)
        lp.login("", "")
        assert lp.is_error_displayed()
        lp.close_error()
        assert not lp.is_error_displayed()

    def test_TC_LOGIN_014_username_case_sensitive(self, driver):
        # Username IN HOA phải fail (phân biệt hoa/thường)
        lp = LoginPage(driver)
        lp.login("STANDARD_USER", "secret_sauce")
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_015_username_whitespace_padding(self, driver):
        # Username có khoảng trắng đầu/cuối phải fail
        lp = LoginPage(driver)
        lp.login(" standard_user ", "secret_sauce")
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_016_sql_injection_attempt(self, driver):
        # Thử SQL injection - phải bị reject
        lp = LoginPage(driver)
        lp.login("admin' OR '1'='1", "anything")
        assert lp.is_error_displayed()
        assert "/inventory.html" not in driver.current_url

    def test_TC_LOGIN_017_xss_attempt(self, driver):
        # Thử XSS - script không được execute
        lp = LoginPage(driver)
        lp.login("<script>alert(1)</script>", "anything")
        assert lp.is_error_displayed()
        from selenium.common.exceptions import NoAlertPresentException
        try:
            driver.switch_to.alert.accept()
            pytest.fail("XSS đã execute - alert xuất hiện!")
        except NoAlertPresentException:
            pass

    def test_TC_LOGIN_018_very_long_username(self, driver):
        # Username 1000 ký tự - site không được crash
        lp = LoginPage(driver)
        lp.login("a" * 1000, "secret_sauce")
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_019_special_chars_username(self, driver):
        # Username toàn ký tự đặc biệt
        lp = LoginPage(driver)
        lp.login("!@#$%^&*()", "secret_sauce")
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_020_password_case_sensitive(self, driver):
        # Password IN HOA phải fail
        lp = LoginPage(driver)
        lp.login("standard_user", "SECRET_SAUCE")
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()
