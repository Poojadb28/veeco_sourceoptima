import pytest
from pages.login_page import LoginPage
from pages.system_admin_page import SystemAdminPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_duplicate_admin_creation(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    user_data = data["users"]["create_admin"]

    email = login_data["email"]
    password = login_data["password"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    admin = SystemAdminPage(browser)

    # ---------------- FLOW ---------------- #
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
    error_msg = admin.get_duplicate_user_error()

    print("Captured Error:", repr(error_msg))

    assert "failed" in error_msg.lower(), \
        f"Expected duplicate user error, got: {error_msg}"

    # IMPORTANT (avoid blocking next tests)
    admin.handle_modal_after_submit()