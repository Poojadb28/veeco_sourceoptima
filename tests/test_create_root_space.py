import pytest

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_create_root_space(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    space_data = data["projects"]["create_root_space"]

    email = login_data["email"]
    password = login_data["password"]
    space_name = space_data["space_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    # ---------------- PROJECTS ---------------- #
    projects = ProjectsPage(browser)

    projects.open_projects()
    projects.right_click_projects_area()

    projects.click_new_root_space()
    projects.enter_space_name(space_name)

    projects.choose_icon()
    projects.select_blue_color()
    projects.click_create_space()

    # ---------------- VALIDATION ---------------- #
    success_msg = projects.get_success_message()

    assert "space created" in success_msg.lower(), \
        f"Unexpected message: {success_msg}"