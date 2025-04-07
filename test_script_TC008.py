import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Set up the base URL
BASE_URL = "https://practicetestautomation.com/practice-test-login/"

# Set up the username and password
USERNAME = "student"
PASSWORD = "Password123"

def setup_webdriver():
    """Set up the Selenium WebDriver (Chrome)"""
    try:
        # Use the webdriver-manager to automatically manage the ChromeDriver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        return driver
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        return None

def navigate_to_url(driver):
    """Navigate to the base URL"""
    try:
        driver.get(BASE_URL)
        print("Navigated to the base URL")
    except WebDriverException as e:
        print(f"Error navigating to URL: {e}")

def login(driver):
    """Perform the login"""
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(USERNAME)
        print("Entered username")

        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(PASSWORD)
        print("Entered password")

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        print("Clicked login button")
    except TimeoutException as e:
        print(f"Timeout error during login: {e}")

def test_form_validation(driver):
    """Test the form validation"""
    try:
        # Enter invalid username and password
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter an invalid username
        username_field.send_keys("invalid_username")
        print("Entered invalid username")

        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter an invalid password
        password_field.send_keys("invalid_password")
        print("Entered invalid password")

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        print("Clicked login button")

        # Wait for the error message to be visible
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#error-message"))
        )
        # Check if the error message is displayed
        if error_message.is_displayed():
            print("Error message is displayed")
            return True
        else:
            print("Error message is not displayed")
            return False
    except TimeoutException as e:
        print(f"Timeout error during form validation test: {e}")
        return False

def main():
    driver = setup_webdriver()
    if driver is not None:
        navigate_to_url(driver)
        login_result = test_form_validation(driver)
        if login_result:
            print("Test Case TC008: PASS")
        else:
            print("Test Case TC008: FAIL")
        driver.quit()

if __name__ == "__main__":
    main()