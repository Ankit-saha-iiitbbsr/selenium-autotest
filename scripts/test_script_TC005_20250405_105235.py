# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Setup the Selenium WebDriver with Chrome.
    """
    try:
        # Set up the Chrome WebDriver
        logging.info("Setting up the Chrome WebDriver")
        driver = webdriver.Chrome()
        return driver
    except WebDriverException as e:
        logging.error(f"Failed to set up the Chrome WebDriver: {e}")
        return None

def navigate_to_url(driver, url):
    """
    Navigate to the given URL.
    """
    try:
        # Navigate to the URL
        logging.info(f"Navigating to {url}")
        driver.get(url)
    except WebDriverException as e:
        logging.error(f"Failed to navigate to {url}: {e}")

def login(driver, base_url, username, password):
    """
    Perform the login if needed.
    """
    try:
        # Navigate to the login page
        logging.info("Navigating to the login page")
        driver.get(base_url)

        # Wait for the username field to be available
        logging.info("Waiting for the username field")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )

        # Enter the username
        logging.info("Entering the username")
        username_field.send_keys(username)

        # Wait for the password field to be available
        logging.info("Waiting for the password field")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )

        # Enter the password
        logging.info("Entering the password")
        password_field.send_keys(password)

        # Wait for the login button to be available
        logging.info("Waiting for the login button")
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        # Click the login button
        logging.info("Clicking the login button")
        login_button.click()
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Failed to login: {e}")

def execute_test_steps(driver, test_case):
    """
    Execute all test steps using proper waits and assertions.
    """
    try:
        # Load an invalid URL
        logging.info("Loading an invalid URL")
        invalid_url = "https://practicetestautomation.com/practice-test-login/invalid"
        driver.get(invalid_url)

        # Wait for the error message to be available
        logging.info("Waiting for the error message")
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1#error"))
        )

        # Verify the error message is displayed
        logging.info("Verifying the error message is displayed")
        assert error_message.is_displayed()
        logging.info("Error message is displayed")
    except (TimeoutException, AssertionError, NoSuchElementException) as e:
        logging.error(f"Failed to execute test steps: {e}")
        return False
    return True

def handle_exceptions(driver, test_case):
    """
    Handle potential errors gracefully.
    """
    try:
        # Execute the test steps
        result = execute_test_steps(driver, test_case)
        if result:
            logging.info(f"Test case {test_case['id']} passed")
        else:
            logging.info(f"Test case {test_case['id']} failed")
    except Exception as e:
        logging.error(f"Failed to handle exceptions: {e}")
        logging.info(f"Test case {test_case['id']} failed")

def main():
    # Set up the test case
    test_case = {
        "id": "TC005",
        "name": "Verify negative - invalid URL",
        "type": "negative",
        "priority": "high",
        "steps": [
            "Load an invalid URL"
        ],
        "expected_result": "The page should display an error message or redirect to a valid page",
        "selectors": {
            "target_elements": [
                {
                    "name": "error_message",
                    "selector": "h1#error"
                }
            ],
            "verification_elements": [
                {
                    "name": "error_message_text",
                    "selector": "h1#error"
                }
            ]
        }
    }

    # Set up the base URL, username, and password
    base_url = "https://practicetestautomation.com/practice-test-login/"
    username = "student"
    password = "Password123"

    # Set up the WebDriver
    driver = setup_webdriver()

    if driver is not None:
        # Navigate to the URL
        navigate_to_url(driver, base_url)

        # Perform the login if needed
        login(driver, base_url, username, password)

        # Handle exceptions
        handle_exceptions(driver, test_case)

        # Close the WebDriver
        driver.quit()
    else:
        logging.info(f"Test case {test_case['id']} failed")

if __name__ == "__main__":
    main()