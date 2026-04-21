"""Page object cho trang Login của SauceDemo (URL: /)."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Trang đăng nhập - chứa 2 field (username, password) và nút Login.
    Khi login sai, error message hiện ở dưới form.
    """

    # Locator: tập hợp các element cần tương tác trên trang này
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    # Dùng [data-test='error'] thay vì class để tránh bị ảnh hưởng khi site đổi style
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_X = (By.CSS_SELECTOR, ".error-button")  # Nút X để đóng error
    LOGIN_LOGO = (By.CSS_SELECTOR, ".login_logo")       # Logo Swag Labs ở giữa trang

    def login(self, username, password):
        """Login với username và password.
        Nếu username hoặc password truyền vào là rỗng thì bỏ qua việc nhập
        (để test các case empty field)."""
        if username:
            self.send_keys(self.USERNAME_INPUT, username)
        if password:
            self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def click_login(self):
        """Chỉ click nút Login, không nhập gì - dùng khi đã nhập từ trước."""
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        """Lấy text của error message khi login fail."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        """Có error message hiện trên UI không."""
        return self.is_present(self.ERROR_MESSAGE)

    def close_error(self):
        """Click nút X trên error message để đóng thông báo lỗi."""
        self.click(self.ERROR_CLOSE_X)

    def get_password_input_type(self):
        """Lấy attribute 'type' của password field - phải là 'password' để ẩn ký tự."""
        return self.get_attribute(self.PASSWORD_INPUT, "type")

    def is_login_page(self):
        """Kiểm tra có đang ở trang login không (dựa vào logo)."""
        return self.is_displayed(self.LOGIN_LOGO)
