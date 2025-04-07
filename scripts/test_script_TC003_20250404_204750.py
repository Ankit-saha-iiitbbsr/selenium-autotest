# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, WebDriverException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the base URL, username, and password
BASE_URL = "http://testphp.vulnweb.com/login.php"
USERNAME = "test"
PASSWORD = "test"

# Define the test case
TEST_CASE = {
    "id": "TC003",
    "name": "Verify invalid credit card number validation",
    "type": "negative",
    "priority": "medium",
    "steps": [
        "Enter invalid credit card number in the credit card number field",
        "Click the update button"
    ],
    "expected_result": "Error message should be displayed for invalid credit card number",
    "selectors": {
        "target_elements": [
            {
                "name": "credit_card_field",
                "selector": "input[name='ucc']"
            },
            {
                "name": "update_button",
                "selector": "input[name='update']"
            }
        ],
        "verification_elements": [
            {
                "name": "error_message",
                "selector": "div.story"
            }
        ]
    }
}

def setup_chrome_driver():
    """
    Set up the Selenium Chrome WebDriver.
    """
    try:
        # Create a new Chrome driver instance
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Optional, comment out for visible browser
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        logging.error(f"Failed to create Chrome driver: {e}")
        return None

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL.
    """
    try:
        # Navigate to the base URL
        logging.info(f"Navigating to {url}")
        driver.get(url)
    except Exception as e:
        logging.error(f"Failed to navigate to {url}: {e}")

def perform_login(driver):
    """
    Perform the login using the provided username and password.
    """
    try:
        # Find the username field
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        logging.info("Entering username")
        username_field.send_keys(USERNAME)

        # Find the password field
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        logging.info("Entering password")
        password_field.send_keys(PASSWORD)

        # Find the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        logging.info("Clicking login button")
        login_button.click()
    except (TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"Failed to perform login: {e}")

def execute_test_steps(driver, test_case):
    """
    Execute the test steps for the provided test case.
    """
    try:
        # Find the credit card number field
        credit_card_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_case["selectors"]["target_elements"][0]["selector"]))
        )
        # Enter an invalid credit card number
        logging.info("Entering invalid credit card number")
        credit_card_field.send_keys("1234567890")

        # Find the update button
        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, test_case["selectors"]["target_elements"][1]["selector"]))
        )
        # Click the update button
        logging.info("Clicking update button")
        update_button.click()
    except (TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"Failed to execute test steps: {e}")

def verify_test_result(driver, test_case):
    """
    Verify the test result for the provided test case.
    """
    try:
        # Find the error message element
        error_message_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_case["selectors"]["verification_elements"][0]["selector"]))
        )
        # Verify the error message is displayed
        logging.info("Verifying error message is displayed")
        if error_message_element.text:
            return True
        else:
            return False
    except TimeoutException as e:
        logging.error(f"Failed to verify test result: {e}")
        return False

def main():
    # Set up the Chrome driver
    driver = setup_chrome_driver()
    if not driver:
        logging.error("Failed to create Chrome driver, exiting test")
        return

    # Navigate to the base URL
    navigate_to_url(driver, BASE_URL)

    # Perform the login
    perform_login(driver)

    # Navigate to the page with the credit card number field
    driver.get("http://testphp.vulnweb.com/listproducts.php")  # Assuming this is the correct URL

    # Execute the test steps
    execute_test_steps(driver, TEST_CASE)

    # Verify the test result
    result = verify_test_result(driver, TEST_CASE)

    # Print the test result
    if result:
        logging.info(f"Test {TEST_CASE['id']} passed: Error message is displayed for invalid credit card number")
    else:
        logging.error(f"Test {TEST_CASE['id']} failed: Error message is not displayed for invalid credit card number")

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    main()