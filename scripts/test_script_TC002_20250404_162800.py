# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Define constants and variables
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "invalid_username"
PASSWORD = "Bonnie@saha007"
TEST_CASE_ID = "TC002"

# Create a function to set up the Selenium WebDriver
def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    :return: webdriver
    """
    # Set up the Chrome WebDriver
    print("Setting up the Selenium WebDriver...")
    webdriver_path = "/path/to/chromedriver"  # Replace with your chromedriver path
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(webdriver_path, options=options)
    print("WebDriver set up successfully.")
    return driver

# Create a function to navigate to the URL
def navigate_to_url(driver):
    """
    Navigate to the given URL.
    :param driver: webdriver
    :return: None
    """
    print(f"Navigating to {BASE_URL}...")
    driver.get(BASE_URL)
    print("Navigation successful.")

# Create a function to perform the test steps
def perform_test_steps(driver):
    """
    Perform the test steps.
    :param driver: webdriver
    :return: bool (True if test passes, False if test fails)
    """
    try:
        # Wait for the username field to be visible
        print("Waiting for the username field...")
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        print("Username field found.")

        # Enter an invalid username
        print("Entering an invalid username...")
        username_field.send_keys(USERNAME)
        print("Username entered.")

        # Wait for the password field to be visible
        print("Waiting for the password field...")
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        print("Password field found.")

        # Enter a valid password
        print("Entering a valid password...")
        password_field.send_keys(PASSWORD)
        print("Password entered.")

        # Wait for the login button to be clickable
        print("Waiting for the login button...")
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        print("Login button found.")

        # Click the login button
        print("Clicking the login button...")
        login_button.click()
        print("Login button clicked.")

        # Wait for the error message to be visible
        print("Waiting for the error message...")
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-danger"))
        )
        print("Error message found.")

        # Check if the error message is displayed
        if error_message.is_displayed():
            print(f"Test case {TEST_CASE_ID} passed: Error message is displayed.")
            return True
        else:
            print(f"Test case {TEST_CASE_ID} failed: Error message is not displayed.")
            return False

    except TimeoutException:
        print(f"Test case {TEST_CASE_ID} failed: Timeout exception occurred.")
        return False
    except NoSuchElementException:
        print(f"Test case {TEST_CASE_ID} failed: Element not found.")
        return False
    except Exception as e:
        print(f"Test case {TEST_CASE_ID} failed: {str(e)}")
        return False

# Create a main function to execute the test
def main():
    """
    Execute the test.
    :return: None
    """
    driver = setup_webdriver()
    navigate_to_url(driver)
    test_result = perform_test_steps(driver)
    driver.quit()
    if test_result:
        print(f"Test case {TEST_CASE_ID} passed.")
    else:
        print(f"Test case {TEST_CASE_ID} failed.")

# Execute the main function
if __name__ == "__main__":
    main()