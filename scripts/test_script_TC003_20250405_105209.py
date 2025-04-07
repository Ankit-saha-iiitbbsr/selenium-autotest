# Import required libraries
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define constants
BASE_URL = "https://practicetestautomation.com/practice-test-login/"
USERNAME = "student"
PASSWORD = "Password123"
TEST_CASE_ID = "TC003"

# Set up the Selenium WebDriver (Chrome)
def setup_webdriver():
    """
    Set up the Selenium WebDriver (Chrome) with the correct options.
    """
    # Set up the Chrome options to run in headless mode
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    return driver

# Navigate to the URL and perform login if needed
def navigate_and_login(driver):
    """
    Navigate to the URL and perform the login if needed.
    """
    try:
        # Navigate to the URL
        driver.get(BASE_URL)
        
        # Check if we are on the login page
        login_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        
        # If we are on the login page, perform the login
        if login_field:
            # Enter the username and password
            driver.find_element(By.CSS_SELECTOR, "input[name='username']").send_keys(USERNAME)
            driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(PASSWORD)
            
            # Click the login button
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            # Wait for the login to complete
            WebDriverWait(driver, 10).until(
                EC.url_changes(BASE_URL)
            )
    except TimeoutException:
        print(f"Timed out waiting for the login page to load. Test case {TEST_CASE_ID} failed.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}. Test case {TEST_CASE_ID} failed.")
        return False
    
    return True

# Verify header elements
def verify_header_elements(driver):
    """
    Verify the header elements.
    """
    try:
        # Wait for the header link to be present
        header_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "link[rel='canonical']"))
        )
        
        # Check if the header link is present
        if header_link:
            print(f"Header link is present. Test case {TEST_CASE_ID} passed.")
            return True
        else:
            print(f"Header link is not present. Test case {TEST_CASE_ID} failed.")
            return False
    except TimeoutException:
        print(f"Timed out waiting for the header link to be present. Test case {TEST_CASE_ID} failed.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}. Test case {TEST_CASE_ID} failed.")
        return False

# Main function
def main():
    # Set up the Selenium WebDriver
    driver = setup_webdriver()
    
    # Navigate to the URL and perform login if needed
    if not navigate_and_login(driver):
        return
    
    # Verify header elements
    if verify_header_elements(driver):
        print(f"Test case {TEST_CASE_ID} passed.")
    else:
        print(f"Test case {TEST_CASE_ID} failed.")
    
    # Close the Selenium WebDriver
    driver.quit()

if __name__ == "__main__":
    main()