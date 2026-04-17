import pytest
import os

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.cost_reduction_play_page import CostReductionPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_cost_reduction_play(browser):

    browser.get(BASE_URL)

    login = LoginPage(browser)
    project = ProjectsPage(browser)
    cost = CostReductionPage(browser)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    play_data = data["plays"]["cost_reduction"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = play_data["root_space"]
    project_name = play_data["project_name"]

    # ---------------- LOGIN ---------------- #
    login.login(email, password)

    # (Optional: keep only if method exists)
    if hasattr(login, "is_login_successful"):
        assert login.is_login_successful(), "Login failed"

    # ---------------- PROJECT ---------------- #
    project.open_projects()
    project.open_root_space(root_space)
    project.open_project(project_name)

    project.select_all_files()

    # ---------------- COST REDUCTION ---------------- #
    cost.select_cost_reduction()
    cost.click_run()

    cost.wait_for_processing()

    cost.click_view_results()
    cost.click_view_details()
    cost.open_report_tab()

    # ---------------- VALIDATION ---------------- #
    cost.take_screenshot()

    screenshot_path = os.path.join(
        os.getcwd(),
        "screenshots",
        "Cost_Reduction_Report.png"
    )

    assert os.path.exists(screenshot_path), "Screenshot not captured"

    # ---------------- CLEANUP ---------------- #
    cost.close_popup()