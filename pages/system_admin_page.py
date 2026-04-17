import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click, wait_for_new_file


class SystemAdminPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ================= LOCATORS ================= #

    user_admin_view = (By.XPATH, "//button[normalize-space()='User Admin View']")
    create_user_button = (By.XPATH, "//button[normalize-space()='Create User']")

    full_name = (By.XPATH, "//input[contains(@placeholder,'full name')]")
    email = (By.XPATH, "//input[contains(@placeholder,'user@example.com')]")
    password = (By.XPATH, "//input[contains(@placeholder,'Enter secure password')]")
    confirm_password = (By.XPATH, "//input[contains(@placeholder,'Re-enter password')]")

    role_dropdown = (By.XPATH, "//select[contains(@class,'w-full')]")

    submit_button = (By.XPATH, "//button[@type='submit']")

    success_message = (By.XPATH, "//div[contains(text(),'User created successfully')]")
    duplicate_user_error = (By.XPATH, "//div[contains(text(),'Failed to create user')]")

    export_credit_history_button = (By.XPATH, "//button[normalize-space()='Export Credit History']")

    available_plays_section = (By.XPATH, "//h2[normalize-space()='Available Plays']")
    disable_success_message = (By.XPATH, "//div[contains(text(),'Play disabled successfully')]")
    enable_success_message = (By.XPATH, "//div[contains(text(),'Play enabled successfully')]")

    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")

    # ================= NAVIGATION ================= #

    def open_user_admin(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.user_admin_view)))
        self.wait.until(EC.visibility_of_element_located(self.create_user_button))

    def click_create_user(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.create_user_button)))
        self.wait.until(EC.visibility_of_element_located(self.full_name))

    # ================= CREATE USER ================= #

    def fill_user_details(self, name, email, password, role):

        self.wait.until(EC.visibility_of_element_located(self.full_name)).clear()
        self.driver.find_element(*self.full_name).send_keys(name)

        self.wait.until(EC.visibility_of_element_located(self.email)).clear()
        self.driver.find_element(*self.email).send_keys(email)

        self.wait.until(EC.visibility_of_element_located(self.password)).clear()
        self.driver.find_element(*self.password).send_keys(password)

        self.wait.until(EC.visibility_of_element_located(self.confirm_password)).clear()
        self.driver.find_element(*self.confirm_password).send_keys(password)

        # Select role dynamically
        dropdown = self.wait.until(EC.element_to_be_clickable(self.role_dropdown))
        safe_click(self.driver, dropdown)

        role_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//option[contains(text(),'{role}')]")
            )
        )
        safe_click(self.driver, role_option)

    def submit_user(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.submit_button)))

        # wait for success OR error
        self.wait.until(
            lambda d: d.find_elements(*self.success_message) or d.find_elements(*self.duplicate_user_error)
        )

        # wait for modal close
        try:
            self.wait.until(EC.invisibility_of_element_located(self.popup_overlay))
        except:
            pass

    # ================= VALIDATION ================= #

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.success_message)).text.strip()

    def get_duplicate_user_error(self):
        return self.wait.until(EC.visibility_of_element_located(self.duplicate_user_error)).text.strip()

    # ================= EXPORT ================= #

    def click_export_credit_history(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.export_credit_history_button)))

    def wait_for_credit_history_download(self, download_dir):

        before_files = set(os.listdir(download_dir))

        new_files = wait_for_new_file(self.driver, download_dir, before_files)

        assert any(
            "credit_history" in f.lower() and f.endswith(".xlsx")
            for f in new_files
        ), "Credit history file not downloaded"

    # ================= AVAILABLE PLAYS ================= #

    def scroll_to_available_plays(self):
        section = self.wait.until(EC.visibility_of_element_located(self.available_plays_section))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", section
        )

    def toggle_play_by_name(self, play_name):

        toggle_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//*[contains(text(),'{play_name}')]/ancestor::div[contains(@class,'rounded')]//button"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", toggle_button
        )

        safe_click(self.driver, toggle_button)

    def get_disable_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.disable_success_message)).text.strip()

    def get_enable_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.enable_success_message)).text.strip()