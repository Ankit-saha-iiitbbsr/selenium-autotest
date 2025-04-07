# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Sets up the Selenium WebDriver using Chrome.
    """
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)
    return driver

def navigate_to_url(driver, url):
    """
    Navigates to the specified URL.
    
    Args:
        driver (webdriver): The Selenium WebDriver instance.
        url (str): The URL to navigate to.
    """
    # Navigate to the URL
    driver.get(url)

def perform_login(driver, username, password):
    """
    Performs the login using the provided credentials.
    
    Args:
        driver (webdriver): The Selenium WebDriver instance.
        username (str): The username to use for login.
        password (str): The password to use for login.
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(username)
        
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(password)
        
        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
    except TimeoutException:
        logging.error("Timeout occurred while waiting for login elements")
    except NoSuchElementException:
        logging.error("Element not found during login")

def verify_dashboard(driver):
    """
    Verifies that the dashboard is displayed after login.
    
    Args:
        driver (webdriver): The Selenium WebDriver instance.
    """
    try:
        # Wait for the dashboard header to be visible
        dashboard_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h6.oxd-text"))
        )
        # Assert that the dashboard header is visible
        assert dashboard_header.is_displayed()
        logging.info("Dashboard header is visible")
        return True
    except TimeoutException:
        logging.error("Timeout occurred while waiting for dashboard header")
    except NoSuchElementException:
        logging.error("Dashboard header not found")
    return False

def execute_test_case(driver, test_case):
    """
    Executes the test case.
    
    Args:
        driver (webdriver): The Selenium WebDriver instance.
        test_case (dict): The test case dictionary.
    """
    # Navigate to the URL
    navigate_to_url(driver, "https://ourgoalplan.co.in/Login.aspx")
    
    # Perform the login
    perform_login(driver, "Ankit.s", "Bonnie@saha007")
    
    # Verify the dashboard
    dashboard_visible = verify_dashboard(driver)
    
    # Print the test result
    if dashboard_visible:
        logging.info(f"Test case {test_case['id']} passed: Dashboard is visible")
    else:
        logging.error(f"Test case {test_case['id']} failed: Dashboard is not visible")

def main():
    # Set up the test case
    test_case = {
        "id": "TC001",
        "name": "Verify successful login with valid credentials",
        "type": "positive",
        "priority": "high",
        "steps": [
            "Enter valid username",
            "Enter valid password",
            "Click login button"
        ],
        "expected_result": "User should be redirected to dashboard",
        "selectors": {
            "target_elements": [
                {
                    "name": "username_field",
                    "selector": "input[name='username']"
                },
                {
                    "name": "password_field",
                    "selector": "input[name='password']"
                },
                {
                    "name": "login_button",
                    "selector": "button[type='submit']"
                }
            ],
            "verification_elements": [
                {
                    "name": "dashboard_header",
                    "selector": "h6.oxd-text"
                }
            ]
        }
    }
    
    # Set up the WebDriver
    driver = setup_webdriver()
    
    try:
        # Execute the test case
        execute_test_case(driver, test_case)
    except Exception as e:
        logging.error(f"Error occurred during test case execution: {str(e)}")
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()