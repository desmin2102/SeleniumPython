"""Page object cho trang Login."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_X = (By.CSS_SELECTOR, ".error-button")
    LOGIN_LOGO = (By.CSS_SELECTOR, ".login_logo")

    def login(self, username, password):
        """Nhập username, password rồi click Login.
        Nếu truyền vào rỗng thì bỏ qua field đó (dùng cho test empty field)."""
        if username:
            self.send_keys(self.USERNAME_INPUT, username)
        if password:
            self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Lấy text thông báo lỗi."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        """Có đang hiện thông báo lỗi không."""
        return self.is_present(self.ERROR_MESSAGE)

    def close_error(self):
        """Click X để đóng thông báo lỗi."""
        self.click(self.ERROR_CLOSE_X)

    def get_password_input_type(self):
        """Lấy attribute type của field password."""
        return self.get_attribute(self.PASSWORD_INPUT, "type")

    def is_login_page(self):
        """Kiểm tra có đang ở trang login không."""
        return self.is_displayed(self.LOGIN_LOGO)
