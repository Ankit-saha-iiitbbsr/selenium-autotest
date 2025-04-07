# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    
    Returns:
    driver (webdriver): The Selenium WebDriver instance.
    """
    try:
        # Initialize the Selenium WebDriver with Chrome
        logging.info("Setting up the Selenium WebDriver with Chrome...")
        driver = webdriver.Chrome()
        driver.maximize_window()  # Maximize the browser window
        return driver
    except Exception as e:
        logging.error(f"Failed to set up the Selenium WebDriver: {e}")
        return None

def navigate_to_url(driver, url):
    """
    Navigate to the given URL.
    
    Args:
    driver (webdriver): The Selenium WebDriver instance.
    url (str): The URL to navigate to.
    """
    try:
        # Navigate to the given URL
        logging.info(f"Navigating to the URL: {url}...")
        driver.get(url)
    except Exception as e:
        logging.error(f"Failed to navigate to the URL: {e}")

def login(driver, username, password):
    """
    Perform the login operation.
    
    Args:
    driver (webdriver): The Selenium WebDriver instance.
    username (str): The username to use for login.
    password (str): The password to use for login.
    """
    try:
        # Wait for the username field to be clickable
        logging.info("Waiting for the username field to be clickable...")
        username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        
        # Enter the username
        logging.info("Entering the username...")
        username_field.send_keys(username)
        
        # Wait for the password field to be clickable
        logging.info("Waiting for the password field to be clickable...")
        password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        
        # Enter the password
        logging.info("Entering the password...")
        password_field.send_keys(password)
        
        # Wait for the login button to be clickable
        logging.info("Waiting for the login button to be clickable...")
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        
        # Click the login button
        logging.info("Clicking the login button...")
        login_button.click()
    except Exception as e:
        logging.error(f"Failed to perform the login operation: {e}")

def measure_load_time(driver):
    """
    Measure the load time of the webpage.
    
    Args:
    driver (webdriver): The Selenium WebDriver instance.
    
    Returns:
    load_time (float): The load time of the webpage in seconds.
    """
    try:
        # Get the navigation start time
        navigation_start_time = driver.execute_script("return window.performance.timing.navigationStart")
        
        # Get the load event end time
        load_event_end_time = driver.execute_script("return window.performance.timing.loadEventEnd")
        
        # Calculate the load time
        load_time = (load_event_end_time - navigation_start_time) / 1000
        return load_time
    except Exception as e:
        logging.error(f"Failed to measure the load time: {e}")
        return None

def verify_expected_result(load_time, expected_load_time):
    """
    Verify the expected result.
    
    Args:
    load_time (float): The actual load time.
    expected_load_time (float): The expected load time.
    
    Returns:
    result (bool): Whether the expected result is met.
    """
    try:
        # Verify the expected result
        if load_time <= expected_load_time:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Failed to verify the expected result: {e}")
        return False

def main():
    # Set up the Selenium WebDriver
    driver = setup_webdriver()
    
    if driver is None:
        logging.error("Failed to set up the Selenium WebDriver. Exiting the test.")
        return
    
    # Define the test case parameters
    test_case_id = "TC007"
    url = "https://practicetestautomation.com/practice-test-login/"
    username = "student"
    password = "Password123"
    expected_load_time = 3  # seconds
    
    # Navigate to the URL
    navigate_to_url(driver, url)
    
    # Perform the login operation if needed
    login(driver, username, password)
    
    # Measure the load time of the webpage
    load_time = measure_load_time(driver)
    
    if load_time is None:
        logging.error("Failed to measure the load time. Exiting the test.")
        return
    
    # Verify the expected result
    result = verify_expected_result(load_time, expected_load_time)
    
    # Print the test result
    if result:
        logging.info(f"Test Case {test_case_id}: PASS - The webpage loaded within {expected_load_time} seconds.")
    else:
        logging.info(f"Test Case {test_case_id}: FAIL - The webpage took {load_time} seconds to load, which exceeds the expected load time of {expected_load_time} seconds.")
    
    # Close the Selenium WebDriver
    driver.quit()

if __name__ == "__main__":
    main()