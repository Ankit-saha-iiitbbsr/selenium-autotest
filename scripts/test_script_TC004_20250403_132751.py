import time
# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Define constants for the test case
BASE_URL = 'https://ourgoalplan.co.in/Login.aspx'
USERNAME = 'Ankit.s'
PASSWORD = 'Bonnie@saha007'
TEST_CASE_ID = 'TC004'

# Define the test steps with their respective selectors
TEST_STEPS = {
    'goal_text': (By.CSS_SELECTOR, 'input[id="txtAddGoal"]'),
    'add_goal_button': (By.CSS_SELECTOR, 'button[id="btnAddGoal"]')
}

# Define the verification element selectors
VERIFICATION_ELEMENTS = {
    'added_goal': (By.CSS_SELECTOR, 'div.goal-item')
}

def setup_webdriver():
    """
    Sets up the Selenium WebDriver with Chrome.
    """
    try:
        # Set up the Chrome WebDriver
        print('Setting up the Chrome WebDriver...')
        webdriver_options = webdriver.ChromeOptions()
        # Comment out to run in non-headless mode
        # webdriver_options.add_argument('headless')
        # webdriver_options.add_argument('window-size=1920x1080')
        # webdriver_options.add_argument('disable-gpu')
        driver = webdriver.Chrome(options=webdriver_options)
        return driver
    except WebDriverException as e:
        print(f'Error setting up the WebDriver: {e}')
        raise

def navigate_to_url(driver, url):
    """
    Navigates to the given URL.
    """
    try:
        # Navigate to the given URL
        print(f'Navigating to {url}...')
        driver.get(url)
        return True
    except WebDriverException as e:
        print(f'Error navigating to {url}: {e}')
        return False

def login(driver):
    """
    Performs the login using the given credentials.
    """
    try:
        # Wait for the username field to be clickable
        print('Waiting for the username field to be clickable...')
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))
        )
        # Enter the username
        print('Entering the username...')
        username_field.send_keys(USERNAME)
        
        # Wait for the password field to be clickable
        print('Waiting for the password field to be clickable...')
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        # Enter the password
        print('Entering the password...')
        password_field.send_keys(PASSWORD)
        
        # Wait for the login button to be clickable
        print('Waiting for the login button to be clickable...')
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        # Click the login button
        print('Clicking the login button...')
        login_button.click()
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f'Error performing login: {e}')
        return False

def add_goal(driver):
    """
    Performs the add goal functionality.
    """
    try:
        # Wait for the goal text field to be clickable
        print('Waiting for the goal text field to be clickable...')
        goal_text_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(TEST_STEPS['goal_text'])
        )
        # Enter the goal text
        print('Entering the goal text...')
        goal_text_field.send_keys('Test Goal')
        
        # Wait for the add goal button to be clickable
        print('Waiting for the add goal button to be clickable...')
        add_goal_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(TEST_STEPS['add_goal_button'])
        )
        # Click the add goal button
        print('Clicking the add goal button...')
        add_goal_button.click()
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f'Error performing add goal functionality: {e}')
        return False

def verify_goal_added(driver):
    """
    Verifies if the goal is added successfully.
    """
    try:
        # Wait for the added goal element to be visible
        print('Waiting for the added goal element to be visible...')
        added_goal_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(VERIFICATION_ELEMENTS['added_goal'])
        )
        # Verify if the goal is added successfully
        print('Verifying if the goal is added successfully...')
        return added_goal_element.text != ''
    except TimeoutException as e:
        print(f'Error verifying added goal: {e}')
        return False

def main():
    # Set up the WebDriver
    driver = setup_webdriver()
    
    # Navigate to the URL
    if not navigate_to_url(driver, BASE_URL):
        print(f'Test Case {TEST_CASE_ID} failed: Unable to navigate to the URL')
        return
    
    # Perform login
    if not login(driver):
        print(f'Test Case {TEST_CASE_ID} failed: Unable to perform login')
        return
    
    # Perform add goal functionality
    if not add_goal(driver):
        print(f'Test Case {TEST_CASE_ID} failed: Unable to perform add goal functionality')
        return
    
    # Verify if the goal is added successfully
    if verify_goal_added(driver):
        print(f'Test Case {TEST_CASE_ID} passed: Goal added successfully')
    else:
        print(f'Test Case {TEST_CASE_ID} failed: Goal not added successfully')

if __name__ == '__main__':
    main()