import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click, wait_for_new_file


class DesignReviewPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ================= LOCATORS ================= #

    dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")
    option = (By.XPATH, "//option[normalize-space()='Design Review']")
    run_btn = (By.XPATH, "//button[contains(text(),'Run Design Review')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")
    view_details = (By.XPATH, "//button[normalize-space()='View Details']")

    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")

    download_btn = (By.XPATH, "//button[contains(@title,'Design Review')]")

    close_icon = (By.XPATH, "//button[contains(@class,'p-2')]")

    # ================= ACTIONS ================= #

    def select_design_review(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.dropdown)))
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.option)))

    def click_run(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.run_btn)))

    def wait_for_processing(self):
        self.wait.until(EC.element_to_be_clickable(self.view_details))

    def click_view_results(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.view_results)))

    def click_view_details(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.view_details)))

    def open_report_tab(self):
        popup = self.wait.until(EC.visibility_of_element_located(self.popup_overlay))

        tab = popup.find_element(By.XPATH, ".//button[normalize-space()='Design Review']")

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)

        safe_click(self.driver, tab)

        # Ensure tab actually loaded
        self.wait.until(EC.element_to_be_clickable(self.download_btn))

    def download_report(self, download_dir):

        # capture existing files
        before_files = set(os.listdir(download_dir))

        button = self.wait.until(EC.element_to_be_clickable(self.download_btn))

        safe_click(self.driver, button)

        # use common util (VERY IMPORTANT)
        new_files = wait_for_new_file(self.driver, download_dir, before_files)

        print("Downloaded files:", new_files)

        #  validate properly (no filename dependency)
        assert any(f.endswith(".xlsx") for f in new_files), \
            "Design Review file not downloaded"

    def close_popup(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.close_icon)))

        # wait until popup disappears
        self.wait.until(EC.invisibility_of_element_located(self.popup_overlay))

        # ensure page usable again
        self.wait.until(EC.element_to_be_clickable(self.dropdown))