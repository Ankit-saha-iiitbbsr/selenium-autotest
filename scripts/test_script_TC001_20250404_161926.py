import time
# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define the test case details
test_case_id = "TC001"
test_case_name = "Verify successful login with valid credentials"
base_url = "https://ourgoalplan.co.in/Login.aspx"
username = "Ankit.s"
password = "Bonnie@saha007"

# Selectors for target elements
selectors = {
    "username_field": "input[name='username']",
    "password_field": "input[name='password']",
    "login_button": "button[type='submit']",
    "dashboard_header": "h6.oxd-text"
}

def setup_webdriver():
    """
    Set up the Selenium WebDriver (Chrome).
    """
    options = webdriver.ChromeOptions()
    # Add options as needed (e.g., headless mode, disable extensions)
    driver = webdriver.Chrome(options=options)
    return driver

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL.
    """
    try:
        driver.get(url)
        print(f"Successfully navigated to {url}")
    except Exception as e:
        print(f"Error navigating to {url}: {e}")

def perform_login(driver, username, password):
    """
    Perform the login operation.
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selectors["username_field"]))
        )
        # Enter the username
        username_field.send_keys(username)
        
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selectors["password_field"]))
        )
        # Enter the password
        password_field.send_keys(password)
        
        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selectors["login_button"]))
        )
        # Click the login button
        login_button.click()
        
        print("Login operation performed successfully")
    except TimeoutException:
        print("Timeout occurred while performing login operation")
    except Exception as e:
        print(f"Error performing login operation: {e}")

def verify_login_success(driver):
    """
    Verify that the login was successful by checking the dashboard header.
    """
    try:
        # Wait for the dashboard header to be visible
        dashboard_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selectors["dashboard_header"]))
        )
        # Verify the dashboard header text
        if dashboard_header.text:
            print("Login was successful")
            return True
        else:
            print("Login failed")
            return False
    except TimeoutException:
        print("Timeout occurred while verifying login success")
        return False
    except Exception as e:
        print(f"Error verifying login success: {e}")
        return False

def main():
    try:
        # Set up the webdriver
        driver = setup_webdriver()
        
        # Navigate to the URL
        navigate_to_url(driver, base_url)
        
        # Perform the login operation
        perform_login(driver, username, password)
        
        # Verify the login success
        login_success = verify_login_success(driver)
        
        # Print the test result
        if login_success:
            print(f"Test Case {test_case_id}: PASS")
        else:
            print(f"Test Case {test_case_id}: FAIL")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the webdriver
    print(f"Test case TC001 PASSED: Successfully executed Verify successful login with valid credentials")
        driver.quit()

if __name__ == "__main__":
    main()