import os
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_new_file(driver, download_dir, before_files, timeout=120):
    """
    Wait for new file download (Jenkins safe)
    """

    def file_downloaded(d):
        after_files = set(os.listdir(download_dir))
        new_files = after_files - before_files

        for f in new_files:
            # ignore temp files
            if not f.endswith(".crdownload"):
                return True
        return False

    WebDriverWait(driver, timeout).until(file_downloaded)

    # return new downloaded files (optional but useful)
    after_files = set(os.listdir(download_dir))
    return after_files - before_files


def safe_click(driver, element):
    """
    Click with fallback (normal + JS)
    """

    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)