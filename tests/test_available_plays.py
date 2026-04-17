import pytest
import json
import os

from pages.login_page import LoginPage
from pages.system_admin_page import SystemAdminPage
from config.config import BASE_URL, TESTDATA_DIR


@pytest.mark.regression
def test_available_plays_enable_or_disable_actions(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD TEST DATA ---------------- #
    with open(os.path.join(TESTDATA_DIR, "test_data.json")) as file:
        data = json.load(file)

    email = data["system_admin_login"]["email"]
    password = data["system_admin_login"]["password"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    assert login.is_login_successful(), "Login failed"

    # ---------------- ADMIN ---------------- #
    admin = SystemAdminPage(browser)

    admin.open_user_admin()
    admin.scroll_to_available_plays()

    plays = [
        "Tariff Analysis",
        "Cost Reduction Analysis",
        "Design Review",
        "Drawing Checker - Both",
        "Drawing Checker - Veeco",
        "Drawing Checker - General"
    ]

    for play in plays:

        # -------- DISABLE -------- #
        admin.toggle_play_by_name(play)

        disable_msg = admin.get_disable_success_message()
        assert "disabled successfully" in disable_msg.lower(), \
            f"Disable failed for {play}: {disable_msg}"

        # -------- ENABLE -------- #
        admin.toggle_play_by_name(play)

        enable_msg = admin.get_enable_success_message()
        assert "enabled successfully" in enable_msg.lower(), \
            f"Enable failed for {play}: {enable_msg}"