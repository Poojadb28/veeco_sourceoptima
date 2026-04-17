import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_logout(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]

    email = login_data["email"]
    password = login_data["password"]

    login = LoginPage(browser)

    # ---------------- LOGIN ---------------- #
    login.login(email, password)

    # ---------------- LOGOUT ---------------- #
    login.logout()

    # ---------------- VALIDATION ---------------- #
    # Wait for login button to appear again
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(login.login_button)
    )

    assert browser.current_url == BASE_URL or \
           "login" in browser.current_url.lower(), \
        "Logout failed"