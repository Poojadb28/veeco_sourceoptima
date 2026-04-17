import pytest
from pages.login_page import LoginPage
from pages.system_admin_page import SystemAdminPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_duplicate_create_user(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    user_data = data["users"]["create_user"]

    email = login_data["email"]
    password = login_data["password"]

    user_email = user_data["email"]

    login = LoginPage(browser)
    login.login(email, password)

    admin = SystemAdminPage(browser)

    admin.open_user_admin()

    # ---------------- FIRST CREATION ---------------- #
    admin.click_create_user()

    admin.fill_user_details(
        user_data["full_name"],
        user_email,
        user_data["password"],
        user_data["role"]
    )

    admin.submit_user()

    # Handle success modal (IMPORTANT)
    admin.handle_modal_after_submit()

    # ---------------- DUPLICATE CREATION ---------------- #
    admin.click_create_user()

    admin.fill_user_details(
        user_data["full_name"],
        user_email,   # same email again
        user_data["password"],
        user_data["role"]
    )

    admin.submit_user()

    # ---------------- VALIDATION ---------------- #
    error_msg = admin.get_duplicate_user_error()

    print("Duplicate Error:", error_msg)

    assert "failed" in error_msg.lower(), \
        f"Expected duplicate error, got: {error_msg}"

    # Close modal
    admin.handle_modal_after_submit()