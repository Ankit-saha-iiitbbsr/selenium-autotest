from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Constants
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"
TEST_CASE_ID = "TC001"

def setup_driver():
    """Initialize and return a configured Chrome WebDriver."""
    print("Setting up Chrome driver...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # Global wait for elements
    return driver

def login_to_application(driver):
    """Perform login with provided credentials."""
    try:
        print("Navigating to login page...")
        driver.get(BASE_URL)
        
        # Wait for username field and enter credentials
        print("Waiting for username field...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.clear()
        username_field.send_keys(USERNAME)
        
        # Wait for password field and enter password
        print("Waiting for password field...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.clear()
        password_field.send_keys(PASSWORD)
        
        # Wait for login button and click it
        print("Waiting for login button...")
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
        print("Login attempt completed.")
        return True
        
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return False

def verify_dashboard_access(driver):
    """Verify successful login by checking dashboard presence."""
    try:
        print("Waiting for dashboard header...")
        dashboard_header = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h6.oxd-text"))
        )
        print(f"Dashboard header found: {dashboard_header.text}")
        return True
        
    except Exception as e:
        print(f"Error verifying dashboard access: {str(e)}")
        return False

def main():
    """Main test execution function."""
    try:
        print(f"Starting test execution for {TEST_CASE_ID}")
        driver = setup_driver()
        
        # Perform login
        if not login_to_application(driver):
            print(f"{TEST_CASE_ID} - FAIL: Login failed")
            return
            
        # Verify dashboard access
        if verify_dashboard_access(driver):
            print(f"{TEST_CASE_ID} - PASS: Successfully logged in and redirected to dashboard")
        else:
            print(f"{TEST_CASE_ID} - FAIL: Dashboard verification failed")
            
    except Exception as e:
        print(f"{TEST_CASE_ID} - FAIL: An unexpected error occurred: {str(e)}")
        
    finally:
        # Clean up
        print("Closing browser session...")
        driver.quit()

if __name__ == "__main__":
    main()