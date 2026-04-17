import pytest
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.smoke
def test_create_new_project(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    project_data = data["projects"]["create_project"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = project_data["root_space"]
    project_name = project_data["project_name"]
    file_name = project_data["file_name"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(text(),'Projects')]")
        )
    )

    # ---------------- PROJECT ---------------- #
    projects = ProjectsPage(browser)

    projects.open_projects()
    projects.right_click_root_space(root_space)

    projects.click_create_new_project()
    projects.enter_project_name(project_name)

    # Jenkins-safe file path
    file_path = os.path.join(os.getcwd(), "testdata", "files", file_name)

    projects.upload_file(file_path)
    projects.click_upload()

    # ---------------- VALIDATION ---------------- #
    assert projects.verify_project_created(project_name), "Project not created"