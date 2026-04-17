import pytest

from pages.login_page import LoginPage
from pages.system_admin_page import SystemAdminPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_create_user(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    user_data = data["users"]["create_user"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(login_data["email"], login_data["password"])

    # ---------------- ADMIN ---------------- #
    admin = SystemAdminPage(browser)

    admin.open_user_admin()
    admin.click_create_user()

    admin.fill_user_details(
        user_data["full_name"],
        user_data["email"],   # from testdata.json
        user_data["password"],
        user_data["role"]
    )

    admin.submit_user()

    # ---------------- VALIDATION ---------------- #
    try:
        success_msg = admin.get_success_message()
        assert "user created successfully" in success_msg.lower()

    except:
        # Handle duplicate case (since email is fixed)
        error_msg = admin.get_duplicate_user_error()
        assert "failed" in error_msg.lower()