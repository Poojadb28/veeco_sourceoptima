import pytest

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_add_sub_space(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    subspace_data = data["projects"]["create_sub_space"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = subspace_data["root_space"]
    sub_space_name = subspace_data["sub_space_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    # ---------------- PROJECTS ---------------- #
    projects = ProjectsPage(browser)

    projects.open_projects()

    projects.right_click_root_space(root_space)

    projects.click_add_sub_space()
    projects.enter_sub_space_name(sub_space_name)

    projects.choose_icon()
    projects.select_color()
    projects.click_create_space()

    # ---------------- VALIDATION ---------------- #
    assert projects.verify_sub_space_created(sub_space_name), \
        "Sub-space not created"