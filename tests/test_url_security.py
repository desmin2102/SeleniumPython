"""Test cases cho URL Security - truy cập trực tiếp URL khi chưa login (TC_URL_001 -> 003)."""

import pytest

from pages.login_page import LoginPage


@pytest.mark.security
class TestUrlSecurity:
    @pytest.mark.parametrize(
        "path",
        ["inventory.html", "cart.html", "checkout-complete.html"],
        ids=["TC_URL_001", "TC_URL_002", "TC_URL_003"],
    )
    def test_protected_url_requires_login(self, driver, config, path):
        # Truy cập trực tiếp URL bảo vệ khi chưa login -> bị block + báo lỗi
        # Lấy base_url từ config để dễ chuyển env (dev/staging/prod)
        driver.get(f"{config['base_url']}/{path}")
        lp = LoginPage(driver)
        assert lp.is_error_displayed()
        error = lp.get_error_message().lower()
        assert path in error and "logged in" in error
