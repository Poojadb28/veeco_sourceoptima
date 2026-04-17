import pytest
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_edit_details(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    edit_data = data["projects"]["edit_space"]

    email = login_data["email"]
    password = login_data["password"]

    old_space = edit_data["old_space_name"]
    new_space = edit_data["new_space_name"]
    color = edit_data["color"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    projects = ProjectsPage(browser)

    # ---------------- FLOW ---------------- #
    projects.open_projects()

    projects.right_click_space(old_space)

    projects.click_edit_details()

    projects.edit_space_name(new_space)

    # Handle color dynamically (better design)
    if color.lower() == "purple":
        projects.select_purple_color()
    elif color.lower() == "blue":
        projects.select_blue_color()

    projects.change_icon()
    projects.save_changes()

    # ---------------- VALIDATION ---------------- #
    assert projects.verify_space_updated(), \
        f"Space update failed: {old_space} → {new_space}"