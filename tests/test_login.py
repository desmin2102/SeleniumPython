"""Test cases cho chức năng Login (TC_LOGIN_001 -> 020)."""

import pytest
from selenium.common.exceptions import NoAlertPresentException

from pages.login_page import LoginPage


@pytest.mark.login
class TestLogin:
    # ---------- Login thành công ----------

    def test_TC_LOGIN_001_valid_standard_user(self, driver, test_data):
        creds = test_data["users"]["standard_user"]
        LoginPage(driver).login(creds["username"], creds["password"])
        assert "/inventory.html" in driver.current_url

    @pytest.mark.parametrize(
        "user_key",
        ["problem_user", "performance_glitch_user", "error_user", "visual_user"],
        ids=["TC_LOGIN_003", "TC_LOGIN_004", "TC_LOGIN_005", "TC_LOGIN_006"],
    )
    def test_alternate_user_can_login(self, driver, test_data, user_key):
        # Cùng logic với TC_LOGIN_001 nhưng với 4 user khác (đặc biệt: bug UI hoặc delay).
        # Tách ID riêng qua ids=[...] để screenshot/HTML report vẫn map đúng TC.
        creds = test_data["users"][user_key]
        LoginPage(driver).login(creds["username"], creds["password"])
        assert "/inventory.html" in driver.current_url

    # ---------- Login fail ----------

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
        ids=["TC_LOGIN_007", "TC_LOGIN_008"],
    )
    def test_invalid_credentials(self, driver, username, password):
        # 007 = sai password, 008 = username không tồn tại - cùng error message
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
        ids=["TC_LOGIN_014", "TC_LOGIN_020"],
    )
    def test_credentials_case_sensitive(self, driver, username, password):
        # 014 = username IN HOA, 020 = password IN HOA
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

    # ---------- Security / robustness ----------

    def test_TC_LOGIN_016_sql_injection_attempt(self, driver):
        lp = LoginPage(driver)
        lp.login("admin' OR '1'='1", "anything")
        assert lp.is_error_displayed()
        assert "/inventory.html" not in driver.current_url

    def test_TC_LOGIN_017_xss_attempt(self, driver):
        lp = LoginPage(driver)
        lp.login("<script>alert(1)</script>", "anything")
        assert lp.is_error_displayed()
        try:
            driver.switch_to.alert.accept()
            pytest.fail("XSS đã execute - alert xuất hiện!")
        except NoAlertPresentException:
            pass

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
