import pytest
import os

from pages.login_page import LoginPage
from pages.system_admin_page import SystemAdminPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_create_admin(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    user_data = data["users"]["create_admin"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(login_data["email"], login_data["password"])

    assert login.is_login_successful(), "Login failed"

    # ---------------- ADMIN ---------------- #
    admin = SystemAdminPage(browser)

    admin.open_user_admin()
    admin.click_create_user()

    admin.fill_user_details(
        user_data["full_name"],
        user_data["email"],   
        user_data["password"],
        user_data["role"]
    )

    admin.submit_user()

    # ---------------- VALIDATION ---------------- #
    try:
        success_msg = admin.get_success_message()
        assert "user created successfully" in success_msg.lower()

    except:
        # Handle duplicate (since email is fixed)
        error_msg = admin.get_duplicate_user_error()
        assert "failed" in error_msg.lower()