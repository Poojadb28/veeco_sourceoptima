import pytest
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_search_field(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    search_data = data["projects"]["search_file"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = search_data["root_space"]
    project_name = search_data["project_name"]
    file_name = search_data["file_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    projects = ProjectsPage(browser)

    # ---------------- NAVIGATION ---------------- #
    projects.open_projects()
    projects.open_root_space(root_space)
    projects.open_project(project_name)

    # ---------------- SEARCH ---------------- #
    projects.search_file(file_name)

    # ---------------- VALIDATION ---------------- #
    assert projects.verify_file_present(file_name), \
        f"Searched file not displayed: {file_name}"