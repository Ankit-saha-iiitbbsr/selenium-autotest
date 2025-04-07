# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging
import sys

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_chrome_driver():
    """
    Initialize the Chrome WebDriver.
    :return: WebDriver instance
    """
    try:
        # Create a new instance of the Chrome driver
        logging.info("Initializing Chrome WebDriver...")
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')  # Optional: run in headless mode
        driver = webdriver.Chrome(options=options)
        logging.info("Chrome WebDriver initialized successfully.")
        return driver
    except WebDriverException as e:
        logging.error("Failed to initialize Chrome WebDriver: %s", e)
        sys.exit(1)

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL.
    :param driver: WebDriver instance
    :param url: Target URL
    """
    try:
        logging.info("Navigating to %s...", url)
        driver.get(url)
    except Exception as e:
        logging.error("Failed to navigate to %s: %s", url, e)
        sys.exit(1)

def login_to_application(driver, username, password):
    """
    Perform login to the application.
    :param driver: WebDriver instance
    :param username: Login username
    :param password: Login password
    """
    try:
        # Wait for the username field to be available
        logging.info("Waiting for username field...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.send_keys(username)
        logging.info("Username entered.")

        # Wait for the password field to be available
        logging.info("Waiting for password field...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys(password)
        logging.info("Password entered.")

        # Wait for the login button to be clickable
        logging.info("Waiting for login button...")
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        logging.info("Login button clicked.")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error("Failed to perform login: %s", e)
        sys.exit(1)

def verify_dashboard_header(driver):
    """
    Verify the presence of the dashboard header.
    :param driver: WebDriver instance
    :return: boolean indicating whether the dashboard header is present
    """
    try:
        # Wait for the dashboard header to be visible
        logging.info("Waiting for dashboard header...")
        dashboard_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h6.oxd-text"))
        )
        logging.info("Dashboard header found.")
        return True
    except (TimeoutException, NoSuchElementException):
        logging.error("Dashboard header not found.")
        return False

def main():
    # Define test case constants
    test_case_id = "TC001"
    test_case_name = "Verify successful login with valid credentials"
    base_url = "https://practicetestautomation.com/practice-test-login/"
    username = "student"
    password = "Password123"

    # Set up the Chrome WebDriver
    driver = setup_chrome_driver()

    # Navigate to the URL
    navigate_to_url(driver, base_url)

    # Perform login
    login_to_application(driver, username, password)

    # Verify the dashboard header
    dashboard_header_present = verify_dashboard_header(driver)

    # Print test results
    if dashboard_header_present:
        logging.info("%s: %s - %s", test_case_id, test_case_name, "PASS")
        print(f"{test_case_id}: {test_case_name} - PASS")
    else:
        logging.error("%s: %s - %s", test_case_id, test_case_name, "FAIL")
        print(f"{test_case_id}: {test_case_name} - FAIL")

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()