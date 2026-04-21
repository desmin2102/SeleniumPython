"""Test cases cho footer (TC_FOOTER_001 -> 004)."""

import pytest
from pages.login_page import LoginPage
from pages.footer_page import FooterPage


@pytest.fixture(autouse=True)
def _login(driver):
    LoginPage(driver).login("standard_user", "secret_sauce")


@pytest.mark.footer
class TestFooter:

    def test_TC_FOOTER_001_twitter_link_present(self, driver):
        # Link Twitter hiện và trỏ tới saucelabs
        href = FooterPage(driver).get_twitter_href()
        assert href and "saucelabs" in href.lower()

    def test_TC_FOOTER_002_facebook_link_present(self, driver):
        # Link Facebook hiện và trỏ tới saucelabs
        href = FooterPage(driver).get_facebook_href()
        assert href and "saucelabs" in href.lower()

    def test_TC_FOOTER_003_linkedin_link_present(self, driver):
        # Link LinkedIn hiện và trỏ tới sauce-labs
        href = FooterPage(driver).get_linkedin_href()
        assert href and "sauce-labs" in href.lower()

    def test_TC_FOOTER_004_copyright_text_displayed(self, driver):
        # Text copyright chứa 'Sauce Labs'
        text = FooterPage(driver).get_copyright_text()
        assert "Sauce Labs" in text
