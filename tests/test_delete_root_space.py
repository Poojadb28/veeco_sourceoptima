import pytest

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_delete_root_space(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    delete_data = data["projects"]["delete_root_space"]

    email = login_data["email"]
    password = login_data["password"]

    space_name = delete_data["space_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    # ---------------- PROJECTS ---------------- #
    projects = ProjectsPage(browser)

    projects.open_projects()

    # Right click on space
    projects.right_click_space(space_name)

    # Delete
    projects.click_delete_space()
    projects.accept_delete_alert()

    # ---------------- VALIDATION ---------------- #
    assert projects.verify_space_deleted(space_name), \
        "Space deletion failed"