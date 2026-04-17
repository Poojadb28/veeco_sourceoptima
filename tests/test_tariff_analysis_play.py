import pytest
import os

from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage
from pages.tariff_play_page import TariffPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_tariff_analysis_play(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]
    project_data = data["projects"]["create_project"]

    email = login_data["email"]
    password = login_data["password"]

    root_space = project_data["root_space"]
    project_name = project_data["project_name"]

    # Jenkins-safe download path
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ---------------- PAGES ---------------- #
    login = LoginPage(browser)
    project = ProjectsPage(browser)
    tariff = TariffPage(browser)

    # ---------------- FLOW ---------------- #
    login.login(email, password)

    project.open_projects()
    project.open_root_space(root_space)
    project.open_project(project_name)
    project.select_all_files()

    tariff.select_tariff_analysis()
    tariff.treat_as_assembly()
    tariff.set_top_level()
    tariff.run_tariff_analysis()

    # ---------------- EXPORT BOM ---------------- #
    tariff.export_bom(download_dir)

    # ---------------- APPROVE BOM ---------------- #
    tariff.approve_bom()

    # ---------------- EXPORT TARIFF ---------------- #
    tariff.export_tariff(download_dir)

    # ---------------- NAVIGATION ---------------- #
    tariff.go_back()