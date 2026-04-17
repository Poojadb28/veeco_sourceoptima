import pytest
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.system_admin_page import SystemAdminPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


@pytest.mark.regression
def test_export_credit_history(browser):

    browser.get(BASE_URL)

    wait = WebDriverWait(browser, 20)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data()

    login_data = data["logins"]["system_admin"]

    email = login_data["email"]
    password = login_data["password"]

    # Jenkins-safe download dir
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    admin = SystemAdminPage(browser)

    admin.open_user_admin()

    # ---------------- CLEAN OLD FILES ---------------- #
    before_files = set(os.listdir(download_dir))

    # ---------------- CLICK EXPORT ---------------- #
    wait.until(EC.element_to_be_clickable(admin.export_credit_history_button))
    admin.click_export_credit_history()

    # ---------------- WAIT FOR DOWNLOAD ---------------- #
    WebDriverWait(browser, 60).until(
        lambda d: len(set(os.listdir(download_dir)) - before_files) > 0
    )

    after_files = set(os.listdir(download_dir))
    new_files = after_files - before_files

    print("Downloaded files:", new_files)

    # ---------------- VALIDATION ---------------- #
    assert any(
        f.lower().endswith(".xlsx") and "credit" in f.lower()
        for f in new_files
    ), "Credit history file not downloaded"