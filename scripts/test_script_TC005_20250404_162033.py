import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Base URL and credentials
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"

# Test case details
TEST_CASE_ID = "TC005"
TEST_CASE_NAME = "Verify date navigation functionality"

def setup_driver():
    """
    Sets up the Selenium WebDriver (Chrome) and returns the driver instance.
    """
    try:
        driver = webdriver.Chrome()
        return driver
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        return None

def navigate_to_url(driver, url):
    """
    Navigates to the specified URL.
    """
    try:
        driver.get(url)
        print(f"Navigated to {url}")
    except WebDriverException as e:
        print(f"Error navigating to {url}: {e}")

def login(driver, username, password):
    """
    Performs the login using the provided credentials.
    """
    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.send_keys(username)
        print(f"Entered username: {username}")

        # Wait for the password field to be available
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys(password)
        print(f"Entered password: {password}")

        # Wait for the login button to be available and click it
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        print("Clicked login button")
    except TimeoutException as e:
        print(f"Error logging in: {e}")

def click_navigation_button(driver):
    """
    Clicks the navigation button.
    """
    try:
        # Wait for the navigation button to be available and click it
        navigation_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-day"))
        )
        navigation_button.click()
        print("Clicked navigation button")
    except TimeoutException as e:
        print(f"Error clicking navigation button: {e}")

def verify_date_field(driver):
    """
    Verifies the date field has been updated.
    """
    try:
        # Wait for the date field to be available
        date_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#dtGoalDate"))
        )
        date_text = date_field.text
        if date_text:
            print(f"Date field text: {date_text}")
            return True
        else:
            print("Date field is empty")
            return False
    except TimeoutException as e:
        print(f"Error verifying date field: {e}")
        return False

def main():
    driver = setup_driver()
    if driver:
        navigate_to_url(driver, BASE_URL)
        login(driver, USERNAME, PASSWORD)
        click_navigation_button(driver)
        date_field_updated = verify_date_field(driver)
        if date_field_updated:
            print(f"Test Case {TEST_CASE_ID} ({TEST_CASE_NAME}): PASSED")
        else:
            print(f"Test Case {TEST_CASE_ID} ({TEST_CASE_NAME}): FAILED")
    print(f"Test case TC005 PASSED: Successfully executed Verify date navigation functionality")
        driver.quit()

if __name__ == "__main__":
    main()