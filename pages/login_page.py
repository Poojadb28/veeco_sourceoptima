from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.common_utils import safe_click


class LoginPage:

    # ---------------- LOCATORS ---------------- #

    login_button = (By.XPATH, "//a[normalize-space()='Login']")
    email_field = (By.ID, "email")
    password_field = (By.ID, "password")
    eye_icon = (By.XPATH, "//*[name()='path' and contains(@d,'M320 400c-')]")
    submit_button = (By.XPATH, "//button[normalize-space()='Submit']")
    error_message = (By.XPATH, "//div[contains(text(),'Error')]")
    logout_button = (By.XPATH, "//button[normalize-space()='Logout']")

    # ---------------- INIT ---------------- #

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ---------------- ACTIONS ---------------- #

    def click_login_button(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.login_button)))

    def enter_email(self, email):
        field = self.wait.until(EC.visibility_of_element_located(self.email_field))
        field.clear()
        field.send_keys(email)

    def enter_password(self, password):
        field = self.wait.until(EC.visibility_of_element_located(self.password_field))
        field.clear()
        field.send_keys(password)

    def click_eye_icon(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.eye_icon)))

    def click_submit(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.submit_button)))

    # ---------------- COMPLETE FLOW ---------------- #

    def login(self, email, password):
        self.click_login_button()
        self.enter_email(email)
        self.enter_password(password)
        self.click_eye_icon()
        self.click_submit()

        # IMPORTANT: wait for login success OR failure
        self.wait.until(
            lambda d: d.find_elements(*self.logout_button) or d.find_elements(*self.error_message)
        )

    # ---------------- VALIDATION ---------------- #

    def is_login_successful(self):
        return len(self.driver.find_elements(*self.logout_button)) > 0

    def get_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.error_message)).text

    # ---------------- LOGOUT ---------------- #

    def logout(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.logout_button)))

        # wait until logout completes (login button appears again)
        self.wait.until(EC.element_to_be_clickable(self.login_button))