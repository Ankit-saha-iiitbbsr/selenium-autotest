# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Set up the Selenium WebDriver (Chrome)
    """
    # Create a new instance of the Chrome driver
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')  # Uncomment to run in headless mode
    driver = webdriver.Chrome(options=options)
    return driver

def navigate_to_url(driver, url):
    """
    Navigate to the given URL
    """
    # Navigate to the given URL
    driver.get(url)
    logging.info(f"Navigated to {url}")

def perform_login(driver, username, password):
    """
    Perform login using the given username and password
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(username)
        
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(password)
        
        # Wait for the login button to be visible
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        
        logging.info("Login successful")
    except TimeoutException:
        logging.error("Login failed: Timeout exception occurred")
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")

def execute_test_steps(driver, test_case):
    """
    Execute the test steps for the given test case
    """
    try:
        # Clear the name field
        name_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_case["selectors"]["target_elements"][0]["selector"]))
        )
        name_field.clear()
        logging.info("Cleared the name field")

        # Click the update button
        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, test_case["selectors"]["target_elements"][1]["selector"]))
        )
        update_button.click()
        logging.info("Clicked the update button")

        # Wait for the error message to be visible
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_case["selectors"]["verification_elements"][0]["selector"]))
        )
        logging.info("Error message displayed for empty name field")

        # Check if the error message is displayed
        if error_message.is_displayed():
            logging.info(f"Test case {test_case['id']} passed: Error message displayed for empty name field")
            return True
        else:
            logging.error(f"Test case {test_case['id']} failed: Error message not displayed for empty name field")
            return False
    except TimeoutException:
        logging.error(f"Test case {test_case['id']} failed: Timeout exception occurred")
        return False
    except NoSuchElementException:
        logging.error(f"Test case {test_case['id']} failed: Element not found")
        return False
    except Exception as e:
        logging.error(f"Test case {test_case['id']} failed: {str(e)}")
        return False

def main():
    # Base URL
    base_url = "http://testphp.vulnweb.com/login.php"
    
    # Credentials
    username = "test"
    password = "test"
    
    # Test case
    test_case = {
        "id": "TC002",
        "name": "Verify empty name field validation",
        "type": "negative",
        "priority": "medium",
        "steps": [
            "Clear the name field",
            "Click the update button"
        ],
        "expected_result": "Error message should be displayed for empty name field",
        "selectors": {
            "target_elements": [
                {
                    "name": "name_field",
                    "selector": "input[name='urname']"
                },
                {
                    "name": "update_button",
                    "selector": "input[name='update']"
                }
            ],
            "verification_elements": [
                {
                    "name": "error_message",
                    "selector": "div.story"
                }
            ]
        }
    }

    # Set up the Selenium WebDriver
    driver = setup_webdriver()

    # Navigate to the URL
    navigate_to_url(driver, base_url)

    # Perform login
    perform_login(driver, username, password)

    # Execute the test steps
    result = execute_test_steps(driver, test_case)

    # Print the test result
    if result:
        print(f"Test case {test_case['id']} passed")
    else:
        print(f"Test case {test_case['id']} failed")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()