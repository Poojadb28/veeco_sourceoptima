import pytest
import os
import time
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.drawing_checker_general_play_page import DrawingCheckerGeneralPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data   # ✅ IMPORTANT


@pytest.mark.regression
def test_drawing_checker_general_play(browser):

    browser.get(BASE_URL)

    login = LoginPage(browser)
    project = ProjectsPage(browser)
    general = DrawingCheckerGeneralPage(browser)

    #  LOAD FROM testdata.json
    data = load_test_data()

    email = data["logins"]["system_admin"]["email"]
    password = data["logins"]["system_admin"]["password"]

    play_data = data["plays"]["drawing_checker_general"]

    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # ================= LOGIN ================= #
    login.login(email, password)

    # ================= PROJECT FLOW ================= #
    project.open_projects()
    project.open_root_space(play_data["root_space"])
    project.open_project(play_data["project_name"])
    project.select_all_files()

    # ================= RUN PLAY ================= #
    general.select_drawing_checker_general()
    general.click_run()

    general.wait_for_processing()
    general.click_view_results()

    # ================= SWITCH TAB ================= #
    main_window = browser.current_window_handle

    WebDriverWait(browser, 15).until(lambda d: len(d.window_handles) > 1)

    for window in browser.window_handles:
        if window != main_window:
            browser.switch_to.window(window)
            break

    # ================= SEARCH ================= #
    general.search_issue(play_data["search_text"])
    general.clear_search()

    # ================= FILTER ================= #
    general.filter_by_severity(play_data["severity"])
    general.filter_by_severity("All Severities")

    general.filter_by_source(play_data["source"])
    general.filter_by_source("All Sources")

    # ================= DRILLDOWN ================= #
    time.sleep(3)
    general.click_drilldown()

    # ================= DOWNLOAD ================= #
    general.download_report(download_dir)

    # ================= CLOSE ================= #
    browser.close()
    browser.switch_to.window(main_window)