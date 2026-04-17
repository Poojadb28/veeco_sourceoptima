import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click, wait_for_new_file


class TariffPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ---------------- LOCATORS ---------------- #

    dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")
    tariff_option = (By.XPATH, "//option[normalize-space()='Tariff Analysis']")
    treat_checkbox = (By.XPATH, "//input[contains(@class,'w-4 h-4')]")
    set_top = (By.XPATH, "//button[normalize-space()='Set as Top Level']")
    run_btn = (By.XPATH, "//button[contains(normalize-space(),'Run Tariff Analysis')]")

    bom_export_btn = (By.XPATH, "(//button[normalize-space()='Export to Excel'])[1]")
    tariff_export_btn = (By.XPATH, "(//button[normalize-space()='Export to Excel'])[2]")

    approve_bom_btn = (By.XPATH, "//span[normalize-space()='Approve BOM']")

    back_project = (By.XPATH, "//span[normalize-space()='Back to Project']")
    back_btn = (By.XPATH, "//span[normalize-space()='Back']")

    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")

    # ---------------- ACTIONS ---------------- #

    def select_tariff_analysis(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.dropdown)))
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.tariff_option)))

    def treat_as_assembly(self):
        checkbox = self.wait.until(EC.element_to_be_clickable(self.treat_checkbox))
        safe_click(self.driver, checkbox)

    def set_top_level(self):
        elements = self.driver.find_elements(*self.set_top)
        if elements:
            safe_click(self.driver, elements[0])

    def run_tariff_analysis(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.run_btn)))

    # ---------------- APPROVE BOM ---------------- #

    def approve_bom(self):

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.approve_bom_btn)))

        # wait for page refresh
        old_element = self.wait.until(EC.presence_of_element_located(self.bom_export_btn))
        self.wait.until(EC.staleness_of(old_element))

        # wait new content
        self.wait.until(EC.presence_of_element_located(self.tariff_export_btn))

    # ---------------- BOM EXPORT ---------------- #

    def export_bom(self, download_dir):

        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        before_files = set(os.listdir(download_dir))

        button = self.wait.until(EC.element_to_be_clickable(self.bom_export_btn))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        safe_click(self.driver, button)

        new_files = wait_for_new_file(self.driver, download_dir, before_files)

        print("BOM Downloaded:", new_files)

        assert any(f.endswith(".xlsx") for f in new_files), \
            "BOM file not downloaded"

    # ---------------- TARIFF EXPORT ---------------- #

    def export_tariff(self, download_dir):

        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        before_files = set(os.listdir(download_dir))

        button = self.wait.until(EC.element_to_be_clickable(self.tariff_export_btn))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        safe_click(self.driver, button)

        new_files = wait_for_new_file(self.driver, download_dir, before_files)

        print("Tariff Downloaded:", new_files)

        assert any("tariff" in f.lower() and f.endswith(".xlsx") for f in new_files), \
            "Tariff file not downloaded"

    # ---------------- NAVIGATION ---------------- #

    def go_back(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.back_project)))
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.back_btn)))

        # wait until page stable again
        self.wait.until(EC.element_to_be_clickable(self.dropdown))