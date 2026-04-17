import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from utils.common_utils import safe_click


class ProjectsPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ================= LOCATORS ================= #

    projects_button = (By.XPATH, "//span[normalize-space()='Projects']")
    page_body = (By.XPATH, "//div[contains(@class,'flex-1')]")

    new_root_space_button = (By.XPATH, "//button[normalize-space()='New Root Space']")
    space_name_field = (By.XPATH, "//input[@placeholder='e.g. Finance, Project Alpha...']")
    icon_button = (By.XPATH, "//button[.//*[name()='svg']]")
    blue_color = (By.XPATH, "//button[@title='Blue']")
    create_space_button = (By.XPATH, "//button[normalize-space()='Create Space']")
    success_message = (By.XPATH, "//div[contains(text(),'Space created')]")

    new_upload_button = (By.XPATH, "//button[normalize-space()='New Upload']")
    project_name_field = (By.XPATH, "//input[@placeholder='Enter project name']")
    upload_input = (By.XPATH, "//input[@type='file']")
    upload_button = (By.XPATH, "//button[normalize-space()='Upload']")

    delete_icon = (By.XPATH, "//button[@title='Delete project']")
    confirm_delete_input = (By.XPATH, "//input[@placeholder='Type DELETE to confirm']")
    delete_button = (By.XPATH, "//button[normalize-space()='Delete']")
    delete_success_message = (By.XPATH, "//div[contains(text(),'Project deleted')]")

    search_input = (By.XPATH, "//input[@placeholder='Search filename...']")

    select_all_button = (By.XPATH, "//button[normalize-space()='Select All']")
    deselect_all_button = (By.XPATH, "//button[normalize-space()='Deselect All']")

    # ================= COMMON ================= #

    def open_projects(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.projects_button)))
        self.wait.until(EC.visibility_of_element_located(self.page_body))

    def open_root_space(self, space_name):
        locator = (By.XPATH, f"//h4[contains(text(),'{space_name}')]")

        element = self.wait.until(EC.visibility_of_element_located(locator))

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

        safe_click(self.driver, element)

    def open_project(self, project_name):
        locator = (By.XPATH, f"//h3[normalize-space()='{project_name}']")

        element = self.wait.until(EC.visibility_of_element_located(locator))

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

        safe_click(self.driver, element)

    # ================= RIGHT CLICK ================= #

    def right_click_projects_area(self):
        area = self.wait.until(EC.visibility_of_element_located(self.page_body))

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", area)

        ActionChains(self.driver).context_click(area).perform()

        self.wait.until(EC.visibility_of_element_located(self.new_root_space_button))

    # ================= ROOT SPACE ================= #

    def create_root_space(self, name):

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.new_root_space_button)))

        field = self.wait.until(EC.visibility_of_element_located(self.space_name_field))
        field.clear()
        field.send_keys(name)

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.icon_button)))
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.blue_color)))

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.create_space_button)))

        # wait for success
        self.wait.until(EC.visibility_of_element_located(self.success_message))

        # wait overlay close
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'fixed inset-0')]")
            )
        )

    # ================= PROJECT ================= #

    def create_project(self, name, file_path):

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.new_upload_button)))

        field = self.wait.until(EC.visibility_of_element_located(self.project_name_field))
        field.clear()
        field.send_keys(name)

        upload = self.wait.until(EC.presence_of_element_located(self.upload_input))

        self.driver.execute_script("arguments[0].style.display='block';", upload)
        upload.send_keys(file_path)

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.upload_button)))

        # wait project visible
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//h3[normalize-space()='{name}']")
            )
        )

    # ================= DELETE ================= #

    def delete_project(self):

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.delete_icon)))

        confirm = self.wait.until(EC.visibility_of_element_located(self.confirm_delete_input))
        confirm.send_keys("DELETE")

        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.delete_button)))

        self.wait.until(EC.visibility_of_element_located(self.delete_success_message))

    # ================= SEARCH ================= #

    def search_file(self, name):
        box = self.wait.until(EC.visibility_of_element_located(self.search_input))
        box.clear()
        box.send_keys(name)

    # ================= SELECT ================= #

    def select_all_files(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.select_all_button)))

    def deselect_all_files(self):
        safe_click(self.driver, self.wait.until(EC.element_to_be_clickable(self.deselect_all_button)))