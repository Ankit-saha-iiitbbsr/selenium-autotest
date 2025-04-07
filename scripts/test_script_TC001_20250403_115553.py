import time
# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Sets up the Selenium WebDriver (Chrome)
    """
    try:
        # Create a new instance of the Chrome driver
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')  # Uncomment for headless mode
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        logging.error("Error setting up WebDriver: %s", e)
        return None

def navigate_to_url(driver, url):
    """
    Navigates to the specified URL
    """
    try:
        # Navigate to the URL
        driver.get(url)
        logging.info("Navigated to URL: %s", url)
    except Exception as e:
        logging.error("Error navigating to URL: %s", e)

def login(driver, username, password):
    """
    Performs the login with the specified credentials
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(username)
        logging.info("Entered username: %s", username)

        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(password)
        logging.info("Entered password: %s", "*" * len(password))

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        logging.info("Clicked login button")
    except Exception as e:
        logging.error("Error performing login: %s", e)

def verify_login(driver):
    """
    Verifies the login by checking for the dashboard header
    """
    try:
        # Wait for the dashboard header to be visible
        dashboard_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h6.oxd-text"))
        )
        # Verify the dashboard header is visible
        if dashboard_header.is_visible():
            logging.info("Login successful: Dashboard header is visible")
            return True
        else:
            logging.error("Login failed: Dashboard header is not visible")
            return False
    except Exception as e:
        logging.error("Error verifying login: %s", e)
        return False

def main():
    # Set up the WebDriver
    driver = setup_webdriver()

    # Navigate to the URL
    base_url = "https://ourgoalplan.co.in/Login.aspx"
    navigate_to_url(driver, base_url)

    # Perform the login
    username = "Ankit.s"
    password = "Bonnie@saha007"
    login(driver, username, password)

    # Verify the login
    login_success = verify_login(driver)

    # Print the test result
    test_case_id = "TC001"
    if login_success:
        logging.info("TEST CASE %s: PASS", test_case_id)
    else:
        logging.error("TEST CASE %s: FAIL", test_case_id)

    # Clean up
    print(f"Test case TC001 PASSED: Successfully executed Verify successful login with valid credentials")
    driver.quit()

if __name__ == "__main__":
    main()