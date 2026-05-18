"""Page object cho footer (xuất hiện ở mọi trang sau khi login)."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FooterPage(BasePage):

    TWITTER_LINK = (By.CSS_SELECTOR, ".social_twitter a")
    FACEBOOK_LINK = (By.CSS_SELECTOR, ".social_facebook a")
    LINKEDIN_LINK = (By.CSS_SELECTOR, ".social_linkedin a")
    COPYRIGHT = (By.CSS_SELECTOR, ".footer_copy")

    def get_twitter_href(self):
        return self.get_attribute(self.TWITTER_LINK, "href")

    def get_facebook_href(self):
        return self.get_attribute(self.FACEBOOK_LINK, "href")

    def get_linkedin_href(self):
        return self.get_attribute(self.LINKEDIN_LINK, "href")

    def get_copyright_text(self):
        return self.get_text(self.COPYRIGHT)
