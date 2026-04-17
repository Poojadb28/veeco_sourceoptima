import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_user_login(browser):

    browser.get(BASE_URL)

    wait = WebDriverWait(browser, 20)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["user"]

    email = login_data["email"]
    password = login_data["password"]

    login = LoginPage(browser)

    # ---------------- LOGIN ---------------- #
    login.click_login_button()
    login.enter_email(email)
    login.enter_password(password)
    login.click_eye_icon()
    login.click_submit()

    # ---------------- VALIDATION ---------------- #
    wait.until(lambda d: "org" in d.current_url.lower())

    assert "org" in browser.current_url.lower(), \
        f"Login failed, current URL: {browser.current_url}"