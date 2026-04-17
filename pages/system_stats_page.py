import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click, wait_for_new_file


class SystemStatsPage:

    # ---------------- LOCATORS ---------------- #

    time_range_today = (By.XPATH, "//button[normalize-space()='Today']")
    time_range_2_days = (By.XPATH, "//button[normalize-space()='2 days']")
    time_range_3_days = (By.XPATH, "//button[normalize-space()='3 days']")
    time_range_5_days = (By.XPATH, "//button[normalize-space()='5 days']")
    time_range_7_days = (By.XPATH, "//button[normalize-space()='7 days']")

    download_logs_button = (By.XPATH, "//button[normalize-space()='Download Logs (.txt)']")

    # ---------------- INIT ---------------- #

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ---------------- ACTIONS ---------------- #

    def select_time_range(self, locator):

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(locator)))

        #  wait for UI refresh (logs table or activity change)
        self.wait.until(EC.presence_of_element_located(self.download_logs_button))

    def click_download_logs(self, download_dir):

        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        before_files = set(os.listdir(download_dir))

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.download_logs_button)))

        # wait for new file
        new_files = wait_for_new_file(self.driver, download_dir, before_files)

        print("Downloaded logs:", new_files)

        assert any(f.endswith(".txt") for f in new_files), \
            "Logs file NOT downloaded"