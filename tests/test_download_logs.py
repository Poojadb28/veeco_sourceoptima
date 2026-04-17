import pytest
import os
import time
from datetime import datetime

from pages.login_page import LoginPage
from pages.system_stats_page import SystemStatsPage
from config.config import BASE_URL
from utils.testdata_loader import load_test_data


# Jenkins-safe download path
DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def wait_for_new_file(prefix, previous_count, timeout=20):

    for _ in range(timeout):

        files = [f for f in os.listdir(DOWNLOAD_PATH) if f.startswith(prefix)]

        if len(files) > previous_count:
            return True

        time.sleep(1)

    return False


def clean_old_files(prefix):

    for file in os.listdir(DOWNLOAD_PATH):
        if file.startswith(prefix):
            os.remove(os.path.join(DOWNLOAD_PATH, file))


@pytest.mark.regression
def test_download_logs(browser):

    browser.get(BASE_URL)

    # ---------------- LOAD DATA ---------------- #
    data = load_test_data("testdata.json")

    login_data = data["logins"]["system_admin"]

    email = login_data["email"]
    password = login_data["password"]

    # ---------------- LOGIN ---------------- #
    login = LoginPage(browser)
    login.login(email, password)

    system_stats = SystemStatsPage(browser)

    time_ranges = [
        system_stats.time_range_today,
        system_stats.time_range_2_days,
        system_stats.time_range_3_days,
        system_stats.time_range_5_days,
        system_stats.time_range_7_days
    ]

    today_date = datetime.today().strftime("%Y-%m-%d")
    file_prefix = f"sourceoptima_logs_{today_date}"

    # ---------------- CLEAN OLD FILES ---------------- #
    clean_old_files(file_prefix)

    # ---------------- DOWNLOAD FLOW ---------------- #
    for time_range in time_ranges:

        existing_files = [
            f for f in os.listdir(DOWNLOAD_PATH)
            if f.startswith(file_prefix)
        ]
        previous_count = len(existing_files)

        system_stats.select_time_range(time_range)
        system_stats.click_download_logs()

        assert wait_for_new_file(file_prefix, previous_count), \
            "Log file was not downloaded"

    # ---------------- VALIDATION ---------------- #
    all_logs = [
        f for f in os.listdir(DOWNLOAD_PATH)
        if f.startswith(file_prefix)
    ]

    print("Downloaded log files:", all_logs)

    assert len(all_logs) == 5, "Not all log files were downloaded"

    for file in all_logs:

        file_path = os.path.join(DOWNLOAD_PATH, file)

        assert os.path.getsize(file_path) > 0, \
            f"{file} is empty"