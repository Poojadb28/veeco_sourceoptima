import pytest
import json
import os

from pages.login_page import LoginPage
from config.config import BASE_URL, TESTDATA_DIR


@pytest.mark.smoke
def test_admin_login(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD TEST DATA ---------------- #
    with open(os.path.join(TESTDATA_DIR, "test_data.json")) as file:
        data = json.load(file)

    email = data["admin_login"]["email"]
    password = data["admin_login"]["password"]

    login = LoginPage(browser)

    # ---------------- LOGIN ---------------- #
    login.login(email, password)

    # ---------------- VALIDATION ---------------- #

    # Check login success using UI element (BEST PRACTICE)
    assert login.is_login_successful(), "Login failed"

    # Optional: URL validation (secondary check)
    assert "dashboard" in browser.current_url, \
        f"Unexpected URL after login: {browser.current_url}"