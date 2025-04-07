from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

# Test case details
TEST_CASE_ID = "TC002"
TEST_CASE_NAME = "Test invalid login with incorrect password"
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
INVALID_PASSWORD = "Bonnie@saha007"  # Intentionally incorrect password

# Selectors
SELECTORS = {
    "username_field": (By.CSS_SELECTOR, "input[name='username']"),
    "password_field": (By.CSS_SELECTOR, "input[name='password']"),
    "login_button": (By.CSS_SELECTOR, "button[type='submit']"),
    "error_message": (By.CSS_SELECTOR, "div.alert.alert-danger")
}

# Set up Chrome options
def setup_driver():
    """Set up and return a new Chrome WebDriver instance."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=chrome_options)

def take_screenshot(driver, filename):
    """Take a screenshot and save it to the screenshots directory."""
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    filepath = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(filepath)

def perform_login(driver, username, password):
    """Perform the login action with the provided credentials."""
    try:
        # Wait for and enter username
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(SELECTORS["username_field"])
        )
        username_field.clear()
        username_field.send_keys(username)
        
        # Wait for and enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(SELECTORS["password_field"])
        )
        password_field.clear()
        password_field.send_keys(password)
        
        # Click login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(SELECTORS["login_button"])
        )
        login_button.click()
        
        # Wait for error message to appear
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(SELECTORS["error_message"])
        )
        return error_message.text
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Element interaction failed: {e}")
        return None

def main():
    """Main function to execute the test case."""
    try:
        print(f"Starting test case {TEST_CASE_ID}: {TEST_CASE_NAME}")
        
        # Set up driver
        driver = setup_driver()
        
        try:
            # Navigate to login page
            print("Navigating to login page...")
            driver.get(BASE_URL)
            
            # Perform login with invalid password
            print("Performing login with invalid password...")
            error_message = perform_login(driver, USERNAME, INVALID_PASSWORD)
            
            # Verify error message
            if error_message:
                expected_error_text = "Invalid username or password."
                assert expected_error_text in error_message, "Error message text does not match expected."
                print(f"Test passed: Error message displayed correctly - {error_message}")
                print(f"Test case {TEST_CASE_ID} PASSED")
            else:
                print(f"Test failed: No error message was displayed")
                print(f"Test case {TEST_CASE_ID} FAILED")
                take_screenshot(driver, f"TC{TEST_CASE_ID}_error.png")
                
        except Exception as e:
            print(f"Test failed with exception: {e}")
            print(f"Test case {TEST_CASE_ID} FAILED")
            take_screenshot(driver, f"TC{TEST_CASE_ID}_error.png")
            raise
            
    except Exception as e:
        print(f"Setup failed: {e}")
        raise
        
    finally:
        # Clean up
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()