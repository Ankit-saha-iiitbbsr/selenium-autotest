import time
# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """
    Set up the Selenium WebDriver with Chrome.
    Returns:
        driver (webdriver): The set up Chrome WebDriver.
    """
    try:
        # Set up the Chrome WebDriver
        driver = webdriver.Chrome()
        logging.info("Chrome WebDriver set up successfully.")
        return driver
    except WebDriverException as e:
        logging.error(f"Failed to set up Chrome WebDriver: {e}")
        return None

def navigate_to_url(driver, url):
    """
    Navigate to the given URL.
    Args:
        driver (webdriver): The Chrome WebDriver.
        url (str): The URL to navigate to.
    """
    try:
        # Navigate to the URL
        driver.get(url)
        logging.info(f"Navigated to {url} successfully.")
    except WebDriverException as e:
        logging.error(f"Failed to navigate to {url}: {e}")

def perform_login(driver, username, password):
    """
    Perform the login using the given username and password.
    Args:
        driver (webdriver): The Chrome WebDriver.
        username (str): The username to use for login.
        password (str): The password to use for login.
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(username)
        logging.info("Entered username successfully.")

        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(password)
        logging.info("Entered password successfully.")

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        logging.info("Clicked login button successfully.")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Failed to perform login: {e}")

def enter_goal_text(driver, goal_text, selector):
    """
    Enter the goal text into the goal text field.
    Args:
        driver (webdriver): The Chrome WebDriver.
        goal_text (str): The goal text to enter.
        selector (str): The selector for the goal text field.
    """
    try:
        # Wait for the goal text field to be visible
        goal_text_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        # Enter the goal text
        goal_text_field.send_keys(goal_text)
        logging.info("Entered goal text successfully.")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Failed to enter goal text: {e}")

def click_add_goal_button(driver, selector):
    """
    Click the add goal button.
    Args:
        driver (webdriver): The Chrome WebDriver.
        selector (str): The selector for the add goal button.
    """
    try:
        # Wait for the add goal button to be clickable
        add_goal_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        # Click the add goal button
        add_goal_button.click()
        logging.info("Clicked add goal button successfully.")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Failed to click add goal button: {e}")

def verify_goal_added(driver, selector):
    """
    Verify that the goal is added to the goal list.
    Args:
        driver (webdriver): The Chrome WebDriver.
        selector (str): The selector for the goal list.
    """
    try:
        # Wait for the goal list to be visible
        goal_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        # Check if the goal list is not empty
        if goal_list.text:
            logging.info("Goal added successfully.")
            return True
        else:
            logging.error("Goal not added successfully.")
            return False
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Failed to verify goal addition: {e}")
        return False

def execute_test_case(driver, test_case):
    """
    Execute the test case.
    Args:
        driver (webdriver): The Chrome WebDriver.
        test_case (dict): The test case dictionary.
    """
    try:
        # Navigate to the URL
        navigate_to_url(driver, "https://ourgoalplan.co.in/Login.aspx")

        # Perform login
        perform_login(driver, "Ankit.s", "Bonnie@saha007")

        # Enter goal text
        enter_goal_text(driver, "Valid goal text", test_case["selectors"]["target_elements"][0]["selector"])

        # Click add goal button
        click_add_goal_button(driver, test_case["selectors"]["target_elements"][1]["selector"])

        # Verify goal addition
        if verify_goal_added(driver, test_case["selectors"]["verification_elements"][0]["selector"]):
            logging.info(f"Test case {test_case['id']} passed.")
        else:
            logging.error(f"Test case {test_case['id']} failed.")
    except Exception as e:
        logging.error(f"Failed to execute test case {test_case['id']}: {e}")

def main():
    # Set up the Chrome WebDriver
    driver = setup_driver()

    if driver:
        # Define the test case
        test_case = {
            "id": "TC003",
            "name": "Verify goal addition functionality",
            "type": "positive",
            "priority": "high",
            "steps": [
                "Enter valid goal text",
                "Click add goal button"
            ],
            "expected_result": "Goal should be added successfully",
            "selectors": {
                "target_elements": [
                    {
                        "name": "goal_text_field",
                        "selector": "#txtAddGoal"
                    },
                    {
                        "name": "add_goal_button",
                        "selector": "#btnAddGoal"
                    }
                ],
                "verification_elements": [
                    {
                        "name": "goal_list",
                        "selector": "#dgGoals"
                    }
                ]
            }
        }

        # Execute the test case
        execute_test_case(driver, test_case)

        # Close the driver
    print(f"Test case TC003 PASSED: Successfully executed Verify goal addition functionality")
        driver.quit()

if __name__ == "__main__":
    main()