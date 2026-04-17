import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click, wait_for_new_file


class DrawingCheckerPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ================= LOCATORS ================= #

    dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")
    option = (By.XPATH, "//option[normalize-space()='Drawing Checker - Both']")
    run_btn = (By.XPATH, "//button[contains(text(),'Run Drawing Checker - Both')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")
    view_details = (By.XPATH, "//button[normalize-space()='View Details']")

    search_field = (By.XPATH, "//input[@id='issue-search']")
    severity_dropdown = (By.XPATH, "//select[@id='severity-filter']")
    source_dropdown = (By.XPATH, "//select[@id='source-filter']")

    # FIXED (dynamic locator)
    drilldown_btn = (By.XPATH, "//button[contains(@class,'drill') or contains(.,'Drill')]")

    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")
    report_tab = (By.XPATH, ".//button[normalize-space()='Drawing Checker - Both']")

    download_btn = (By.XPATH, "//a[normalize-space()='Download PDF Report']")
    close_icon = (By.XPATH, "//button[contains(@class,'p-2')]")

    # ================= ACTIONS ================= #

    def select_drawing_checker(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.dropdown)))
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.option)))

    def click_run(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.run_btn)))

    def wait_for_processing(self):
        self.wait.until(EC.element_to_be_clickable(self.view_details))

    def click_view_results(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.view_results)))

    # ================= SEARCH ================= #

    def search_issue(self, issue_type):
        field = self.wait.until(EC.visibility_of_element_located(self.search_field))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", field
        )

        field.clear()
        field.send_keys(issue_type)

    def clear_search(self):
        self.wait.until(EC.visibility_of_element_located(self.search_field)).clear()

    # ================= FILTER ================= #

    def filter_by_severity(self, severity):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.severity_dropdown))
        safe_click(self.driver, dropdown)

        option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//select[@id='severity-filter']/option[normalize-space()='{severity}']")
        ))
        safe_click(self.driver, option)

    def filter_by_source(self, source):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.source_dropdown))
        safe_click(self.driver, dropdown)

        option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//select[@id='source-filter']/option[normalize-space()='{source}']")
        ))
        safe_click(self.driver, option)

    # ================= DRILLDOWN ================= #

    def click_drilldown(self):
        buttons = self.driver.find_elements(*self.drilldown_btn)

        for btn in buttons:
            if btn.is_displayed():
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )
                safe_click(self.driver, btn)
                return

        raise Exception("Drilldown button not found")

    # ================= DOWNLOAD ================= #

    def download_report(self, download_dir):

        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        before_files = set(os.listdir(download_dir))

        button = self.wait.until(EC.element_to_be_clickable(self.download_btn))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        safe_click(self.driver, button)

        # use common util (IMPORTANT)
        new_files = wait_for_new_file(self.driver, download_dir, before_files)

        print("Downloaded files:", new_files)

        assert any(f.endswith(".pdf") for f in new_files), \
            "Drawing Checker file not downloaded"

    # ================= CLOSE ================= #

    def close_popup(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.close_icon)))

        self.wait.until(EC.invisibility_of_element_located(self.popup_overlay))

        self.wait.until(EC.element_to_be_clickable(self.dropdown))