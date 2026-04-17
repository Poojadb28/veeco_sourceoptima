import pytest

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_delete_project(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    delete_data = data["projects"]["delete_project"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = delete_data["root_space"]
    project_name = delete_data["project_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    # ---------------- PROJECT ---------------- #
    projects = ProjectsPage(browser)

    projects.open_projects()
    projects.open_root_space(root_space)
    projects.open_project(project_name)

    # Delete project
    projects.click_delete_project()
    projects.confirm_delete()

    # ---------------- VALIDATION ---------------- #
    assert projects.verify_project_deleted(), "Project deletion failed"