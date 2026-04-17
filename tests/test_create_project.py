import pytest
import os

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_create_project(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    project_data = data["projects"]["create_project"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(login_data["email"], login_data["password"])

    # ---------------- PROJECT ---------------- #
    projects = ProjectsPage(browser)

    projects.open_projects()
    projects.open_root_space(project_data["root_space"])

    file_path = os.path.join(
        os.getcwd(),
        "testdata",
        "files",
        project_data["file_name"]
    )

    projects.create_project(
        project_data["project_name"],
        file_path
    )

    # ---------------- VALIDATION ---------------- #
    assert projects.verify_project_created(
        project_data["project_name"]
    ), "Project not created"