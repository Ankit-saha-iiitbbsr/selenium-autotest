# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Set up the Selenium WebDriver (Chrome)
    """
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL
    """
    try:
        # Navigate to the URL
        driver.get(url)
        logging.info(f"Successfully navigated to {url}")
    except WebDriverException as e:
        logging.error(f"Failed to navigate to {url}: {e}")

def login(driver, username, password):
    """
    Perform the login if needed
    """
    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(username)
        logging.info(f"Entered username: {username}")

        # Wait for the password field to be available
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        # Enter the password
        password_field.send_keys(password)
        logging.info(f"Entered password: {password}")

        # Wait for the login button to be available
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        logging.info("Clicked the login button")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Failed to perform login: {e}")

def execute_test_steps(driver, test_case):
    """
    Execute all test steps using proper waits and assertions
    """
    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_case["selectors"]["target_elements"][0]["selector"]))
        )
        # Enter an invalid username
        invalid_username = "invalid_username"
        username_field.send_keys(invalid_username)
        logging.info(f"Entered invalid username: {invalid_username}")

        # Wait for the submit button to be available
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the submit button
        submit_button.click()
        logging.info("Clicked the submit button")

        # Wait for the error message to be displayed
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_case["selectors"]["verification_elements"][0]["selector"]))
        )
        # Assert that the error message is displayed
        if error_message.is_displayed():
            logging.info("Error message is displayed")
            return True
        else:
            logging.error("Error message is not displayed")
            return False
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Failed to execute test steps: {e}")
        return False

def run_test_case(test_case, base_url, username, password):
    """
    Run the test case
    """
    # Set up the WebDriver
    driver = setup_webdriver()

    # Navigate to the URL
    navigate_to_url(driver, base_url)

    # Perform the login if needed
    login(driver, username, password)

    # Execute the test steps
    test_passed = execute_test_steps(driver, test_case)

    # Print the test result
    if test_passed:
        logging.info(f"Test case {test_case['id']} passed")
        print(f"Test case {test_case['id']} passed")
    else:
        logging.error(f"Test case {test_case['id']} failed")
        print(f"Test case {test_case['id']} failed")

    # Close the WebDriver
    driver.quit()

# Test case data
test_case = {
    "id": "TC006",
    "name": "Verify input validation for username field",
    "type": "security_input_validation",
    "category": "security",
    "priority": "high",
    "steps": [
        "Enter invalid username",
        "Click on the submit button"
    ],
    "expected_result": "Error message should be displayed for invalid username",
    "selectors": {
        "target_elements": [
            {
                "name": "username_field",
                "selector": "input[name='username']"
            }
        ],
        "verification_elements": [
            {
                "name": "error_message",
                "selector": "div#error-message"
            }
        ]
    }
}

# Base URL
base_url = "https://practicetestautomation.com/practice-test-login/"

# Username and password
username = "student"
password = "Password123"

# Run the test case
run_test_case(test_case, base_url, username, password)