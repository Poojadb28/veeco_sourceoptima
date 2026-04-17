import pytest
import os
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_export_classification_to_excel(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    export_data = data["projects"]["export_classification"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = export_data["root_space"]
    project_name = export_data["project_name"]

    # Jenkins-safe download directory
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    projects = ProjectsPage(browser)

    # ---------------- NAVIGATION ---------------- #
    projects.open_projects()
    projects.open_root_space(root_space)
    projects.open_project(project_name)

    # ---------------- EXPORT ---------------- #
    before_files = set(os.listdir(download_dir))

    projects.click_export_classification()

    # Wait for new file
    WebDriverWait(browser, 120).until(
        lambda d: len(set(os.listdir(download_dir)) - before_files) > 0
    )

    after_files = set(os.listdir(download_dir))
    new_files = after_files - before_files

    print("Downloaded files:", new_files)

    # ---------------- VALIDATION ---------------- #
    assert any(f.endswith(".xlsx") for f in new_files), \
        "Classification Excel file was not downloaded"