# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Define test case constants
TEST_CASE_ID = "TC003"
TEST_CASE_NAME = "Verify goal date selection"
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"

# Define selectors
DATE_INPUT_SELECTOR = "input[id='dtGoalDate']"

def setup_webdriver():
    """
    Sets up the Selenium WebDriver (Chrome).
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def navigate_to_url(driver, url):
    """
    Navigates to the given URL.
    """
    try:
        driver.get(url)
        print(f"Successfully navigated to {url}")
    except Exception as e:
        print(f"Failed to navigate to {url}: {str(e)}")

def login(driver, username, password):
    """
    Performs login using the given credentials.
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.send_keys(username)
        
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys(password)
        
        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
        print("Successfully logged in")
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Failed to login: {str(e)}")

def select_date(driver, date_input_selector):
    """
    Selects a date from the calendar.
    """
    try:
        # Wait for the date input field to be clickable
        date_input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, date_input_selector))
        )
        date_input_field.click()
        
        # Select a date from the calendar (for simplicity, let's assume we're selecting the first date)
        # You may need to adjust this based on your actual calendar implementation
        date_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "td[data-day='1']"))
        )
        date_field.click()
        
        print("Successfully selected a date")
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Failed to select a date: {str(e)}")

def verify_selected_date(driver, date_input_selector):
    """
    Verifies the selected date is displayed in the input field.
    """
    try:
        # Wait for the date input field to be visible
        date_input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, date_input_selector))
        )
        selected_date = date_input_field.get_attribute("value")
        
        if selected_date:
            print(f"Successfully verified the selected date: {selected_date}")
            return True
        else:
            print("Failed to verify the selected date")
            return False
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Failed to verify the selected date: {str(e)}")
        return False

def execute_test_case(driver):
    """
    Executes the test case.
    """
    try:
        navigate_to_url(driver, BASE_URL)
        login(driver, USERNAME, PASSWORD)
        select_date(driver, DATE_INPUT_SELECTOR)
        verification_result = verify_selected_date(driver, DATE_INPUT_SELECTOR)
        
        if verification_result:
            print(f"Test case {TEST_CASE_ID} passed: {TEST_CASE_NAME}")
        else:
            print(f"Test case {TEST_CASE_ID} failed: {TEST_CASE_NAME}")
    except Exception as e:
        print(f"Test case {TEST_CASE_ID} failed with exception: {str(e)}")

def main():
    driver = setup_webdriver()
    execute_test_case(driver)
    driver.quit()

if __name__ == "__main__":
    main()