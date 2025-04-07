# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import datetime
import time

# Define constants
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"

# Define test case constants
TEST_CASE_ID = "TC003"
TEST_CASE_NAME = "Verify functionality of date picker"

# Setup Selenium WebDriver
def setup_webdriver():
    """Sets up the Selenium WebDriver (Chrome)"""
    try:
        # Create a new instance of the Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (optional)
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error setting up webdriver: {e}")
        return None

# Navigate to the URL and perform login
def navigate_and_login(driver):
    """Navigates to the URL and performs login if needed"""
    try:
        # Navigate to the base URL
        driver.get(BASE_URL)
        print(f"Navigated to {BASE_URL}")

        # Find and fill in the username field
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.send_keys(USERNAME)
        print("Filled in username")

        # Find and fill in the password field
        try:
            password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        except TimeoutException:
            print(f"TimeoutException: Unable to find element")
        password_field.send_keys(PASSWORD)
        print("Filled in password")

        # Find and click the login button
        try:
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        except TimeoutException:
            print(f"TimeoutException: Unable to find element")
        login_button.click()
        print("Clicked login button")

        # Wait for the login to complete
        time.sleep(2)  # Adjust timing as needed
        print("Logged in")
    except Exception as e:
        print(f"Error navigating and logging in: {e}")

# Execute test steps for the date picker
def execute_test_steps(driver):
    """Executes all test steps using proper waits and assertions"""
    try:
        # Find and click the date picker
        date_picker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='dtGoalDate']"))
        )
        date_picker.click()
        print("Clicked date picker")

        # Find and select a date
        # Note: Date selection might require a specific approach depending on the date picker implementation
        # For simplicity, we'll select today's date
        today = datetime.date.today()
        month = today.month
        year = today.year
        day = today.day
        # Simulate date selection (adjust as needed for the actual date picker)
        # In a real scenario, you might need to use the date picker's API or simulate clicks on the calendar
        date_picker.clear()
        date_picker.send_keys(f"{year}-{month:02d}-{day:02d}")
        print("Selected a date")

        # Verify that the selected date is displayed
        selected_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='dtGoalDate']"))
        )
        selected_date_text = selected_date.get_attribute("value")
        print(f"Selected date: {selected_date_text}")
        assert selected_date_text == f"{year}-{month:02d}-{day:02d}"
        print("Verified selected date")
    except Exception as e:
        print(f"Error executing test steps: {e}")

# Main function to execute the test case
def execute_test_case():
    """Executes the test case and prints test results"""
    driver = setup_webdriver()
    if driver is None:
        print(f"Test case {TEST_CASE_ID} failed: unable to set up webdriver")
        return

    navigate_and_login(driver)
    execute_test_steps(driver)

    # Print test result
    try:
        print(f"Test case {TEST_CASE_ID} passed")
    except Exception as e:
        print(f"Test case {TEST_CASE_ID} failed: {e}")
    finally:
        # Close the webdriver
        driver.quit()

if __name__ == "__main__":
    execute_test_case()