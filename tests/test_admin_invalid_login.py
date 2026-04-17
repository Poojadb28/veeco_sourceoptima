import pytest
import json
import os

from pages.login_page import LoginPage
from config.config import BASE_URL, TESTDATA_DIR


@pytest.mark.regression
def test_admin_invalid_login(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD TEST DATA ---------------- #
    with open(os.path.join(TESTDATA_DIR, "test_data.json")) as file:
        data = json.load(file)

    email = data["admin_invalid_login"]["email"]
    password = data["admin_invalid_login"]["password"]

    login = LoginPage(browser)

    # ---------------- LOGIN ATTEMPT ---------------- #
    login.login(email, password)

    # ---------------- VALIDATION ---------------- #
    error_msg = login.get_error_message()

    assert error_msg.strip() == "Error during login. Please try again.", \
        f"Expected error message not shown. Got: '{error_msg}'"