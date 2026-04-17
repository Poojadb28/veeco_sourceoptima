import pytest
import os

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.design_review_play_page import DesignReviewPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_design_review_play(browser):

    browser.get(BASE_URL)

    login = LoginPage(browser)
    project = ProjectsPage(browser)
    design = DesignReviewPage(browser)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]
    play_data = data["plays"]["design_review"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = play_data["root_space"]
    project_name = play_data["project_name"]

    # Jenkins-safe download path
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ---------------- FLOW ---------------- #
    login.login(email, password)

    project.open_projects()
    project.open_root_space(root_space)
    project.open_project(project_name)
    project.select_all_files()

    design.select_design_review()
    design.click_run()

    design.wait_for_processing()
    design.click_view_results()

    design.click_view_details()
    design.open_report_tab()

    design.download_report(download_dir)

    design.close_popup()