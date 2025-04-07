import time
# Import necessary libraries
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define constants for the test case
TEST_CASE_ID = "TC002"
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"

# Define a function to set up the Selenium WebDriver
def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    """
    # Set up the ChromeDriver options
    options = webdriver.ChromeOptions()
    # Set the headless mode to False (visible mode)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)
    return driver

# Define a function to navigate to the URL and perform login if needed
def navigate_and_login(driver):
    """
    Navigate to the URL and perform login if needed.
    """
    # Navigate to the base URL
    driver.get(BASE_URL)
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(USERNAME)
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(PASSWORD)
        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
    except TimeoutException:
        print(f"Failed to find the login fields or button within 10 seconds. Test case {TEST_CASE_ID} failed.")
        return False
    except Exception as e:
        print(f"An error occurred during login: {e}. Test case {TEST_CASE_ID} failed.")
        return False
    return True

# Define a function to execute the test steps
def execute_test_steps(driver):
    """
    Execute the test steps for the test case.
    """
    try:
        # Wait for the date input field to be visible
        date_input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id='dtGoalDate']"))
        )
        # Enter an invalid date (e.g., February 30)
        date_input_field.send_keys("2024-02-30")
        # Wait for the nav-day button to be clickable
        nav_day_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='nav-day']"))
        )
        # Click the nav-day button
        nav_day_button.click()
        # Wait for the error message to be visible
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "label[id='lblGoalError']"))
        )
        # Verify that the error message is displayed
        if error_message.text:
            print(f"Test case {TEST_CASE_ID} passed: Error message is displayed.")
            return True
        else:
            print(f"Test case {TEST_CASE_ID} failed: Error message is not displayed.")
            return False
    except TimeoutException:
        print(f"Failed to find the date input field or nav-day button within 10 seconds. Test case {TEST_CASE_ID} failed.")
        return False
    except Exception as e:
        print(f"An error occurred during test steps: {e}. Test case {TEST_CASE_ID} failed.")
        return False

# Define the main function to run the test case
def run_test_case():
    """
    Run the test case.
    """
    # Set up the Selenium WebDriver
    driver = setup_webdriver()
    try:
        # Navigate to the URL and perform login if needed
        if not navigate_and_login(driver):
            return
        # Execute the test steps
        if execute_test_steps(driver):
            print(f"Test case {TEST_CASE_ID} passed.")
        else:
            print(f"Test case {TEST_CASE_ID} failed.")
    except Exception as e:
        print(f"An error occurred: {e}. Test case {TEST_CASE_ID} failed.")
    finally:
        # Close the browser window
        driver.quit()

# Run the test case
if __name__ == "__main__":
    run_test_case()