"""Page object cho footer - xuất hiện ở mọi trang sau khi login."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FooterPage(BasePage):
    """
    Footer có 3 link mạng xã hội (Twitter, Facebook, LinkedIn) và text copyright.
    """

    TWITTER_LINK = (By.CSS_SELECTOR, ".social_twitter a")
    FACEBOOK_LINK = (By.CSS_SELECTOR, ".social_facebook a")
    LINKEDIN_LINK = (By.CSS_SELECTOR, ".social_linkedin a")
    COPYRIGHT = (By.CSS_SELECTOR, ".footer_copy")

    def get_twitter_href(self):
        """Lấy URL link Twitter (để verify link đúng tên miền)."""
        return self.get_attribute(self.TWITTER_LINK, "href")

    def get_facebook_href(self):
        return self.get_attribute(self.FACEBOOK_LINK, "href")

    def get_linkedin_href(self):
        return self.get_attribute(self.LINKEDIN_LINK, "href")

    def get_copyright_text(self):
        """Đọc text copyright - phải chứa 'Sauce Labs'."""
        return self.get_text(self.COPYRIGHT)
