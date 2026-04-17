import pytest
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_select_and_deselect_all_button(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    page_data = data["projects"]["select_deselect"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = page_data["root_space"]
    project_name = page_data["project_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    projects = ProjectsPage(browser)

    # ---------------- NAVIGATION ---------------- #
    projects.open_projects()
    projects.open_root_space(root_space)
    projects.open_project(project_name)

    # ---------------- SELECT ALL ---------------- #
    projects.select_all_files()

    assert projects.verify_deselect_visible(), \
        "Deselect All button not visible after selecting files"

    # ---------------- DESELECT ALL ---------------- #
    projects.deselect_all_files()

    assert projects.verify_select_visible(), \
        "Select All button not visible after deselecting files"