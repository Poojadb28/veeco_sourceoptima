import pytest
from pages.login_page import LoginPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_system_admin_invalid_login(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin_invalid"]

    email = login_data["email"]
    password = login_data["password"]

    login = LoginPage(browser)

    # ---------------- LOGIN ATTEMPT ---------------- #
    login.click_login_button()
    login.enter_email(email)
    login.enter_password(password)
    login.click_eye_icon()
    login.click_submit()

    # ---------------- VALIDATION ---------------- #
    error_msg = login.get_error_message()

    assert "error" in error_msg.lower(), \
        f"Expected login error message, got: {error_msg}"