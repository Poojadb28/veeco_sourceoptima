import pytest
import os
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from utils.filter_utils import apply_filter, safe_clear_filter
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_filter_labels(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    filter_data = data["projects"]["filter_labels"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = filter_data["root_space"]
    project_name = filter_data["project_name"]
    labels = filter_data["labels"]

    # Screenshots folder
    screenshots_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    projects = ProjectsPage(browser)

    # ---------------- NAVIGATION ---------------- #
    projects.open_projects()
    projects.open_root_space(root_space)
    projects.open_project(project_name)

    dropdown = projects.get_filter_dropdown()

    # ---------------- APPLY FILTERS ---------------- #
    for label in labels:

        apply_filter(browser, dropdown, label)

        # Wait for UI update (replace sleep)
        WebDriverWait(browser, 10).until(
            lambda d: True  # you can replace with specific element if available
        )

        screenshot_name = label.replace(" ", "_") + ".png"

        browser.save_screenshot(
            os.path.join(screenshots_dir, screenshot_name)
        )

        safe_clear_filter(browser)