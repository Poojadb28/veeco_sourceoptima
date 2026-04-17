from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def apply_filter(browser, select_element, label_text):
    
    # Wait for dropdown to be visible
    WebDriverWait(browser, 20).until(
        EC.visibility_of(select_element)
    )

    #  Wait for options to be present
    WebDriverWait(browser, 20).until(
        lambda d: len(select_element.find_elements(By.TAG_NAME, "option")) > 0
    )

    # Apply filter using JS (React safe)
    result = browser.execute_script(
        """
        const select = arguments[0];
        const label = arguments[1];

        for (let option of select.options) {
            if (option.text.includes(label)) {
                select.value = option.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            }
        }
        return false;
        """,
        select_element,
        label_text
    )

    #  If option not found → fail clearly
    if not result:
        raise Exception(f"Filter option '{label_text}' not found")

    # Wait for page update (IMPORTANT FIX)
    WebDriverWait(browser, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def safe_clear_filter(browser):
    """
    Click clear filter only if present
    """

    try:
        clear_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@title='Clear filter']")
            )
        )

        browser.execute_script("arguments[0].click();", clear_btn)

        # Wait for UI update properly
        WebDriverWait(browser, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    except Exception:
        print("[INFO] Clear filter not found — skipping")