"""Test cases cho chức năng Login."""

import pytest

from pages.login_page import LoginPage


@pytest.mark.login
class TestLogin:

    def test_TC_LOGIN_001_valid_standard_user(self, driver, test_data):
        creds = test_data["users"]["standard_user"]
        LoginPage(driver).login(creds["username"], creds["password"])
        assert "/inventory.html" in driver.current_url

    @pytest.mark.parametrize(
        "user_key",
        ["problem_user", "performance_glitch_user", "error_user", "visual_user"],
    )
    def test_alternate_user_can_login(self, driver, test_data, user_key):
        creds = test_data["users"][user_key]
        LoginPage(driver).login(creds["username"], creds["password"])
        assert "/inventory.html" in driver.current_url

    def test_TC_LOGIN_002_locked_out_user(self, driver, test_data):
        creds = test_data["users"]["locked_out_user"]
        lp = LoginPage(driver)
        lp.login(creds["username"], creds["password"])
        assert lp.is_error_displayed()
        assert "locked out" in lp.get_error_message().lower()

    @pytest.mark.parametrize(
        "username, password",
        [
            ("standard_user", "wrong_password"),
            ("invalid_user", "secret_sauce"),
        ],
    )
    def test_invalid_credentials(self, driver, username, password):
        lp = LoginPage(driver)
        lp.login(username, password)
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_009_empty_username(self, driver, test_data):
        password = test_data["users"]["standard_user"]["password"]
        lp = LoginPage(driver)
        lp.login("", password)
        assert lp.is_error_displayed()
        assert "username is required" in lp.get_error_message().lower()

    def test_TC_LOGIN_010_empty_password(self, driver, test_data):
        username = test_data["users"]["standard_user"]["username"]
        lp = LoginPage(driver)
        lp.login(username, "")
        assert lp.is_error_displayed()
        assert "password is required" in lp.get_error_message().lower()

    def test_TC_LOGIN_011_both_empty(self, driver):
        lp = LoginPage(driver)
        lp.login("", "")
        assert lp.is_error_displayed()
        assert "username is required" in lp.get_error_message().lower()

    def test_TC_LOGIN_012_password_field_masked(self, driver):
        lp = LoginPage(driver)
        assert lp.get_password_input_type() == "password"

    def test_TC_LOGIN_013_error_dismissible_via_X(self, driver):
        lp = LoginPage(driver)
        lp.login("", "")
        assert lp.is_error_displayed()
        lp.close_error()
        assert not lp.is_error_displayed()

    @pytest.mark.parametrize(
        "username, password",
        [
            ("STANDARD_USER", "secret_sauce"),
            ("standard_user", "SECRET_SAUCE"),
        ],
    )
    def test_credentials_case_sensitive(self, driver, username, password):
        # Username và password phân biệt chữ hoa/thường
        lp = LoginPage(driver)
        lp.login(username, password)
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_015_username_whitespace_padding(self, driver, test_data):
        password = test_data["users"]["standard_user"]["password"]
        lp = LoginPage(driver)
        lp.login(" standard_user ", password)
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_016_sql_injection_attempt(self, driver):
        lp = LoginPage(driver)
        lp.login("admin' OR '1'='1", "anything")
        assert lp.is_error_displayed()
        assert "/inventory.html" not in driver.current_url

    def test_TC_LOGIN_017_xss_attempt(self, driver):
        lp = LoginPage(driver)
        lp.login("<script>alert(1)</script>", "anything")
        assert lp.is_error_displayed()
        assert "/inventory.html" not in driver.current_url

    def test_TC_LOGIN_018_very_long_username(self, driver, test_data):
        password = test_data["users"]["standard_user"]["password"]
        lp = LoginPage(driver)
        lp.login("a" * 1000, password)
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()

    def test_TC_LOGIN_019_special_chars_username(self, driver, test_data):
        password = test_data["users"]["standard_user"]["password"]
        lp = LoginPage(driver)
        lp.login("!@#$%^&*()", password)
        assert lp.is_error_displayed()
        assert "do not match" in lp.get_error_message().lower()
