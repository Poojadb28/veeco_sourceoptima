import pytest

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_delete_file(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    delete_data = data["projects"]["delete_file"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = delete_data["root_space"]
    project_name = delete_data["project_name"]
    file_name = delete_data["file_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    # ---------------- PROJECT ---------------- #
    projects = ProjectsPage(browser)

    projects.open_projects()
    projects.open_root_space(root_space)
    projects.open_project(project_name)

    projects.delete_file(file_name)

    # ---------------- VALIDATION ---------------- #
    assert projects.is_file_deleted(file_name), "File deletion failed"