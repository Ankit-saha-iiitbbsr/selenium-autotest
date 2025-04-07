# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotVisibleException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define base URL, username, and password
BASE_URL = "https://practicetestautomation.com/practice-test-login/"
USERNAME = "student"
PASSWORD = "Password123"

# Set up Selenium WebDriver (Chrome)
def setup_webdriver():
    """Set up and return Selenium WebDriver instance."""
    logging.info("Setting up Selenium WebDriver...")
    webdriver_options = webdriver.ChromeOptions()
    # Optional: Comment out the following line if you want to see the browser
    # webdriver_options.add_argument("headless")
    driver = webdriver.Chrome(options=webdriver_options)
    logging.info("Selenium WebDriver setup complete.")
    return driver

# Navigate to the URL
def navigate_to_url(driver, url):
    """Navigate to the specified URL."""
    logging.info(f"Navigating to URL: {url}")
    driver.get(url)

# Perform login if needed
def perform_login(driver, username, password):
    """Perform login with the provided credentials."""
    logging.info("Performing login...")
    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter username
        username_field.send_keys(username)
        
        # Wait for the password field to be available
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter password
        password_field.send_keys(password)
        
        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        logging.info("Login successful.")
    except (TimeoutException, NoSuchElementException, ElementNotVisibleException) as e:
        logging.error(f"Login failed: {str(e)}")

# Verify page title
def verify_page_title(driver, expected_title):
    """Verify the page title matches the expected title."""
    logging.info("Verifying page title...")
    try:
        # Wait for the page title to be available
        page_title = WebDriverWait(driver, 10).until(
            EC.title_contains(expected_title)
        )
        logging.info("Page title verification successful.")
        return True
    except TimeoutException:
        logging.error("Page title verification failed: Timed out waiting for the expected title.")
        return False

# Define the test case function
def test_case(driver, test_case_id, url, username, password):
    """Execute the test case."""
    logging.info(f"Executing test case {test_case_id}...")
    navigate_to_url(driver, url)
    perform_login(driver, username, password)
    expected_title = "Logged In Successfully | Practice Test Automation"
    if verify_page_title(driver, expected_title):
        logging.info(f"Test case {test_case_id} passed.")
        return True
    else:
        logging.error(f"Test case {test_case_id} failed: Page title does not match the expected title.")
        return False

# Main function
def main():
    # Set up Selenium WebDriver
    driver = setup_webdriver()
    
    # Define test case ID
    test_case_id = "TC001"
    
    # Execute test case
    test_result = test_case(driver, test_case_id, BASE_URL, USERNAME, PASSWORD)
    
    # Print test result
    if test_result:
        print(f"Test case {test_case_id} passed.")
    else:
        print(f"Test case {test_case_id} failed.")
    
    # Close the Selenium WebDriver
    driver.quit()

if __name__ == "__main__":
    main()