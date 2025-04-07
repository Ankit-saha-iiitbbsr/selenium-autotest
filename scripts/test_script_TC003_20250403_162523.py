import time
# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define constants for test data and URLs
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"
TEST_CASE_ID = "TC003"

# Define a function to set up the Selenium WebDriver
def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    """
    options = webdriver.ChromeOptions()
    # Add any desired Chrome options here
    driver = webdriver.Chrome(options=options)
    return driver

# Define a function to navigate to the base URL and perform login
def navigate_and_login(driver):
    """
    Navigate to the base URL and perform login if needed.
    """
    driver.get(BASE_URL)

    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        # Enter the username
        username_field.send_keys(USERNAME)

        # Wait for the password field to be available
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        # Enter the password
        password_field.send_keys(PASSWORD)

        # Wait for the login button to be available
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()

        print("Login successful")
    except TimeoutException:
        print("Login failed: Timed out waiting for login elements")
    except Exception as e:
        print(f"Login failed: {str(e)}")

# Define a function to execute the test steps
def execute_test_steps(driver):
    """
    Execute the test steps for the given test case.
    """
    try:
        # Wait for the goal text field to be available
        goal_text_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='txtAddGoal']"))
        )
        # Enter a valid goal text
        goal_text_field.send_keys("Test Goal")

        # Wait for the add goal button to be available
        add_goal_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='btnAddGoal']"))
        )
        # Click the add goal button
        add_goal_button.click()

        # Wait for the added goal to be visible
        added_goal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[id='gvTodayAction']"))
        )

        print("Goal added successfully")
        return True
    except TimeoutException:
        print("Goal addition failed: Timed out waiting for elements")
    except NoSuchElementException:
        print("Goal addition failed: Unable to locate elements")
    except Exception as e:
        print(f"Goal addition failed: {str(e)}")
    return False

# Define a function to run the test case
def run_test_case():
    """
    Run the test case and print the result.
    """
    driver = setup_webdriver()
    navigate_and_login(driver)

    if execute_test_steps(driver):
        print(f"Test Case {TEST_CASE_ID} Passed")
        return True
    else:
        print(f"Test Case {TEST_CASE_ID} Failed")
        return False

# Run the test case
if __name__ == "__main__":
    run_test_case()