# import pytest
# import os
# import json
# import sys

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # =========================
# # BASE SETUP
# # =========================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(BASE_DIR)


# def pytest_addoption(parser):
#     parser.addoption("--browser", action="store", default="chrome")
#     parser.addoption("--headless", action="store", default="true")


# # =========================
# # BROWSER FIXTURE
# # =========================
# @pytest.fixture(scope="function")   
# def browser(request):
#     browser_name = request.config.getoption("browser")
#     headless = request.config.getoption("--headless").lower() == "true"

#     if browser_name == "chrome":
#         chrome_options = Options()

#         # Headless control (important for Jenkins)
#         if headless:
#             chrome_options.add_argument("--headless=new")

#         # Jenkins stability options
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--window-size=1920,1080")

#         #  REMOVED (was breaking Jenkins)
#         # chrome_options.add_argument("--user-data-dir=C:\\temp\\chrome-profile")

#         # Download handling (Jenkins safe)
#         download_dir = os.path.join(BASE_DIR, "downloads")
#         os.makedirs(download_dir, exist_ok=True)

#         prefs = {
#             "download.default_directory": download_dir,
#             "download.prompt_for_download": False,
#             "download.directory_upgrade": True,
#             "safebrowsing.enabled": True
#         }

#         chrome_options.add_experimental_option("prefs", prefs)

#         # FIX: Use WebDriver Manager (driver missing issue in Jenkins)
#         service = Service(ChromeDriverManager().install())

#         driver = webdriver.Chrome(service=service, options=chrome_options)

#     else:
#         raise Exception(f"Unsupported browser: {browser_name}")

#     driver.implicitly_wait(5)

#     yield driver

#     driver.quit()


# # =========================
# # TEST DATA FIX
# # =========================
# @pytest.fixture(scope="session")
# def test_data():
#     file_path = os.path.join(BASE_DIR, "testdata", "testdata.json")

#     # fallback for Jenkins
#     if not os.path.exists(file_path):
#         file_path = os.path.join(os.getcwd(), "testdata", "testdata.json")

#     if not os.path.exists(file_path):
#         raise FileNotFoundError(
#             f"testdata.json NOT FOUND.\nChecked:\n{file_path}"
#         )

#     with open(file_path) as f:
#         data = json.load(f)

#     return data

import pytest
import os
import json
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# =========================
# BASE SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="true")


# =========================
# FIX: CHROMEDRIVER PATH
# =========================
def get_chromedriver_path():
    path = ChromeDriverManager().install()

    #  Fix for WinError 193 (wrong file picked)
    if "THIRD_PARTY_NOTICES" in path:
        path = os.path.join(os.path.dirname(path), "chromedriver.exe")

    return path


# =========================
# BROWSER FIXTURE
# =========================
@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser")
    headless = request.config.getoption("--headless").lower() == "true"

    if browser_name == "chrome":
        chrome_options = Options()

        #  Headless (for Jenkins)
        if headless:
            chrome_options.add_argument("--headless=new")

        # Stability options (VERY IMPORTANT for Jenkins)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Download folder (Jenkins-safe)
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        chrome_options.add_experimental_option("prefs", prefs)

        #  FIXED DRIVER
        service = Service(get_chromedriver_path())

        driver = webdriver.Chrome(service=service, options=chrome_options)

    else:
        raise Exception(f"Unsupported browser: {browser_name}")

    driver.implicitly_wait(5)

    yield driver

    driver.quit()


# =========================
# TEST DATA FIXTURE
# =========================
@pytest.fixture(scope="session")
def test_data():
    # Try project structure path
    file_path = os.path.join(BASE_DIR, "testdata", "testdata.json")

    # Fallback for Jenkins workspace
    if not os.path.exists(file_path):
        file_path = os.path.join(os.getcwd(), "testdata", "testdata.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"testdata.json NOT FOUND.\nChecked:\n{file_path}"
        )

    with open(file_path) as f:
        data = json.load(f)

    return data