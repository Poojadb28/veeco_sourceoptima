import pytest
import json
import os
import time

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL, TESTDATA_DIR


@pytest.mark.smoke
def test_add_new_project(browser):

    browser.get(BASE_URL)

    # ---------------- LOGIN ---------------- #
    with open(os.path.join(TESTDATA_DIR, "test_data.json")) as file:
        data = json.load(file)

    email = data["system_admin_login"]["email"]
    password = data["system_admin_login"]["password"]

    login = LoginPage(browser)
    login.login(email, password)

    assert login.is_login_successful(), "Login failed"

    # ---------------- PROJECT ---------------- #
    projects = ProjectsPage(browser)
    projects.open_projects()

    projects.open_root_space("TestSpace1")

    # Unique project name (important for Jenkins)
    project_name = f"TestProject_{int(time.time())}"

    # Relative path (Jenkins compatible)
    file_path = os.path.join(TESTDATA_DIR, "files", "0194.pdf")

    # Create project
    projects.create_project(project_name, file_path)

    # Validation
    assert projects.verify_project_created(project_name), "Project not created"