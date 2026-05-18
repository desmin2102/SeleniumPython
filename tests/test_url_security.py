"""Test cases kiểm tra bảo vệ URL khi chưa đăng nhập."""

import pytest

from pages.login_page import LoginPage


@pytest.mark.security
class TestUrlSecurity:
    @pytest.mark.parametrize(
        "path",
        ["inventory.html", "cart.html", "checkout-complete.html"],
    )
    def test_protected_url_requires_login(self, driver, config, path):
        # Truy cập URL khi chưa login -> bị block và hiện thông báo lỗi
        driver.get(f"{config['base_url']}/{path}")
        lp = LoginPage(driver)
        assert lp.is_error_displayed()
        error = lp.get_error_message().lower()
        assert path in error and "logged in" in error
