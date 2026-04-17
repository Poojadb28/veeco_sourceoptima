import pytest
import json
import os

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL, TESTDATA_DIR


@pytest.mark.regression
def test_upload_new_file(browser):

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

    #  Ensure test independence (create unique names)
    import time
    unique_name = f"TestProject_{int(time.time())}"

    # Open existing root space (or create if needed)
    projects.open_root_space("TestSpace1")

    #  Use relative path
    file_path = os.path.join(TESTDATA_DIR, "files", "0187.pdf")

    # Create project (upload file)
    projects.create_project(unique_name, file_path)

    # Validate project created
    assert projects.verify_project_created(unique_name), "Project not created"