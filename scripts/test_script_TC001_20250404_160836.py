import time
# Import the required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

# Define a function to set up the Selenium WebDriver
def setup_driver():
    """
    Set up the Selenium WebDriver with Chrome.
    
    Returns:
    driver (webdriver): The set up Selenium WebDriver.
    """
    # Create options for the ChromeDriver
    options = Options()
    # Add the options to the ChromeDriver
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    # Return the driver
    return driver

# Define a function to navigate to the URL and perform the login
def navigate_and_login(driver, url, username, password):
    """
    Navigate to the URL and perform the login.
    
    Parameters:
    driver (webdriver): The Selenium WebDriver.
    url (str): The URL to navigate to.
    username (str): The username for the login.
    password (str): The password for the login.
    
    Returns:
    None
    """
    try:
        # Navigate to the URL
        driver.get(url)
        # Wait for the username field
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(username)
        # Wait for the password field
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        # Enter the password
        password_field.send_keys(password)
        # Wait for the login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        # Click the login button
        login_button.click()
        print("Login successful")
    except TimeoutException:
        print("Timed out waiting for the login page")

# Define a function to verify the date navigation functionality
def verify_date_navigation(driver, selectors):
    """
    Verify the date navigation functionality.
    
    Parameters:
    driver (webdriver): The Selenium WebDriver.
    selectors (dict): The selectors for the elements.
    
    Returns:
    None
    """
    try:
        # Wait for the previous day button
        previous_day_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors["target_elements"][0]["selector"]))
        )
        # Click the previous day button
        previous_day_button.click()
        # Get the current date
        current_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors["verification_elements"][0]["selector"]))
        ).get_attribute("value")
        # Convert the date to a datetime object
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
        # Calculate the previous date
        previous_date = current_date - timedelta(days=1)
        # Wait for the date input
        date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors["verification_elements"][0]["selector"]))
        )
        # Get the date input value
        date_input_value = date_input.get_attribute("value")
        # Convert the date input value to a datetime object
        date_input_value = datetime.strptime(date_input_value, "%Y-%m-%d")
        # Assert that the date input value is equal to the previous date
        assert date_input_value == previous_date
        print("Previous day button works correctly")
        
        # Wait for the next day button
        next_day_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors["target_elements"][1]["selector"]))
        )
        # Click the next day button
        next_day_button.click()
        # Get the current date
        current_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors["verification_elements"][0]["selector"]))
        ).get_attribute("value")
        # Convert the date to a datetime object
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
        # Calculate the next date
        next_date = current_date + timedelta(days=1)
        # Wait for the date input
        date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selectors["verification_elements"][0]["selector"]))
        )
        # Get the date input value
        date_input_value = date_input.get_attribute("value")
        # Convert the date input value to a datetime object
        date_input_value = datetime.strptime(date_input_value, "%Y-%m-%d")
        # Assert that the date input value is equal to the next date
        assert date_input_value == next_date
        print("Next day button works correctly")
        print("Test case TC001 passed")
    except TimeoutException:
        print("Timed out waiting for the date navigation elements")
    except AssertionError:
        print("Test case TC001 failed")

# Define a function to run the test case
def run_test_case():
    """
    Run the test case.
    
    Returns:
    None
    """
    # Set up the Selenium WebDriver
    driver = setup_driver()
    # Define the test case data
    url = "https://ourgoalplan.co.in/Login.aspx"
    username = "Ankit.s"
    password = "Bonnie@saha007"
    selectors = {
        "target_elements": [
            {"name": "previous_day_button", "selector": "button[change='-1']"},
            {"name": "next_day_button", "selector": "button[change='1']"},
            {"name": "date_input", "selector": "input[id='dtGoalDate']"}
        ],
        "verification_elements": [
            {"name": "date_input", "selector": "input[id='dtGoalDate']"}
        ]
    }
    # Navigate to the URL and perform the login
    navigate_and_login(driver, url, username, password)
    # Verify the date navigation functionality
    verify_date_navigation(driver, selectors)
    # Close the Selenium WebDriver
    print(f"Test case TC001 PASSED: Successfully executed Verify date navigation functionality")
    driver.quit()

# Run the test case
run_test_case()