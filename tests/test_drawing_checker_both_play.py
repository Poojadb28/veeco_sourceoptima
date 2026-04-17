import pytest
import os
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.drawing_checker_both_play_page import DrawingCheckerPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_drawing_checker_both_play(browser):

    browser.get(BASE_URL)

    login = LoginPage(browser)
    project = ProjectsPage(browser)
    drawing = DrawingCheckerPage(browser)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    play_data = data["plays"]["drawing_checker_both"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = play_data["root_space"]
    project_name = play_data["project_name"]
    search_text = play_data["search_text"]
    severity = play_data["severity"]
    source = play_data["source"]

    # Jenkins-safe download path
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ---------------- FLOW ---------------- #
    login.login(email, password)

    project.open_projects()
    project.open_root_space(root_space)
    project.open_project(project_name)
    project.select_all_files()

    drawing.select_drawing_checker()
    drawing.click_run()

    drawing.wait_for_processing()
    drawing.click_view_results()

    # ---------------- SWITCH TAB ---------------- #
    main_window = browser.current_window_handle

    WebDriverWait(browser, 10).until(
        lambda d: len(d.window_handles) > 1
    )

    for window in browser.window_handles:
        if window != main_window:
            browser.switch_to.window(window)
            break

    # ---------------- SEARCH ---------------- #
    drawing.search_issue(search_text)
    drawing.clear_search()

    # ---------------- FILTERS ---------------- #
    drawing.filter_by_severity(severity)
    drawing.filter_by_severity("All Severities")

    drawing.filter_by_source(source)
    drawing.filter_by_source("All Sources")

    # ---------------- DRILLDOWN ---------------- #
    WebDriverWait(browser, 10).until(
        lambda d: len(d.find_elements(*drawing.drilldown_btn)) > 0
    )
    drawing.click_drilldown()

    # ---------------- DOWNLOAD ---------------- #
    drawing.download_report(download_dir)

    # VERIFY DOWNLOAD
    files = os.listdir(download_dir)
    assert any(f.endswith(".pdf") for f in files), \
        "Drawing Checker Both report not downloaded"

    # ---------------- CLOSE TAB ---------------- #
    browser.close()
    browser.switch_to.window(main_window)