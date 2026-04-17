import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click, wait_for_new_file


class DrawingCheckerVeecoPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ---------------- LOCATORS ---------------- #

    dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")
    option = (By.XPATH, "//option[normalize-space()='Drawing Checker - Veeco']")
    run_btn = (By.XPATH, "//button[contains(text(),'Run Drawing Checker - Veeco')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")

    search_field = (By.XPATH, "//input[@id='issue-search']")
    severity_dropdown = (By.XPATH, "//select[@id='severity-filter']")
    source_dropdown = (By.XPATH, "//select[@id='source-filter']")

    drilldown_btn = (By.XPATH, "//button[contains(@class,'drill') or contains(.,'Drill')]")

    download_btn = (By.XPATH, "//a[normalize-space()='Download PDF Report']")

    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")
    close_icon = (By.XPATH, "//button[contains(@class,'p-2')]")

    # ---------------- ACTIONS ---------------- #

    def select_drawing_checker_veeco(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.dropdown)))
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.option)))

    def click_run(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.run_btn)))

    def wait_for_processing(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results))

    def click_view_results(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.view_results)))

    # ---------------- SEARCH ---------------- #

    def search_issue(self, text):
        field = self.wait.until(EC.visibility_of_element_located(self.search_field))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", field
        )

        field.clear()
        field.send_keys(text)

    def clear_search(self):
        self.wait.until(EC.visibility_of_element_located(self.search_field)).clear()

    # ---------------- FILTERS ---------------- #

    def filter_by_severity(self, value):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.severity_dropdown))
        safe_click(self.driver, dropdown)

        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//select[@id='severity-filter']/option[normalize-space()='{value}']")
            )
        )
        safe_click(self.driver, option)

    def filter_by_source(self, value):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.source_dropdown))
        safe_click(self.driver, dropdown)

        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//select[@id='source-filter']/option[normalize-space()='{value}']")
            )
        )
        safe_click(self.driver, option)

    # ---------------- DRILLDOWN ---------------- #

    def click_drilldown(self):

        # wait until buttons appear
        self.wait.until(lambda d: len(d.find_elements(*self.drilldown_btn)) > 0)

        buttons = self.driver.find_elements(*self.drilldown_btn)

        for btn in buttons:
            if btn.is_displayed():

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )

                safe_click(self.driver, btn)

                # wait for next screen (download button appears)
                self.wait.until(EC.presence_of_element_located(self.download_btn))

                return

        raise Exception("Drilldown button not found")

    # ---------------- DOWNLOAD ---------------- #

    def download_report(self, download_dir):

        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        before_files = set(os.listdir(download_dir))

        button = self.wait.until(EC.element_to_be_clickable(self.download_btn))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        safe_click(self.driver, button)

        # use common util
        new_files = wait_for_new_file(self.driver, download_dir, before_files)

        print("Downloaded files:", new_files)

        assert any(f.endswith(".pdf") for f in new_files), \
            "Drawing Checker Veeco file NOT downloaded"

    # ---------------- CLOSE ---------------- #

    def close_popup(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.close_icon)))

        self.wait.until(EC.invisibility_of_element_located(self.popup_overlay))

        self.wait.until(EC.element_to_be_clickable(self.dropdown))