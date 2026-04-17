import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click   # reuse common util


class CostReductionPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ================= LOCATORS ================= #

    dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")
    option = (By.XPATH, "//option[normalize-space()='Cost Reduction']")
    run_button = (By.XPATH, "//button[contains(text(),'Run Cost Reduction')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")
    view_details = (By.XPATH, "//button[normalize-space()='View Details']")

    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")
    report_tab = (By.XPATH, ".//button[normalize-space()='Cost Reduction']")

    close_icon = (By.XPATH, "//button[contains(@class,'p-2')]")

    # ================= ACTIONS ================= #

    def select_cost_reduction(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.dropdown)))
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.option)))

    def click_run(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.run_button)))

    def wait_for_processing(self):
        # wait until results ready
        self.wait.until(EC.element_to_be_clickable(self.view_details))

    def click_view_results(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.view_results)))

    def click_view_details(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.view_details)))

    def open_report_tab(self):
        # wait for popup
        popup = self.wait.until(EC.visibility_of_element_located(self.popup_overlay))

        tab = popup.find_element(By.XPATH, self.report_tab[1])

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)

        safe_click(self.driver, tab)

        #  better validation (not just tab visible)
        self.wait.until(EC.element_to_be_clickable(tab))

    def take_screenshot(self, file_name="Cost_Reduction_Report.png"):
        screenshot_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        file_path = os.path.join(screenshot_dir, file_name)

        self.driver.save_screenshot(file_path)

        print(f"Screenshot saved at: {file_path}")

    def close_popup(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.close_icon)))

        # wait until popup disappears
        self.wait.until(EC.invisibility_of_element_located(self.popup_overlay))

        # ensure page usable again
        self.wait.until(EC.element_to_be_clickable(self.dropdown))