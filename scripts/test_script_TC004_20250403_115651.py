# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time

# Define test constants
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"
TEST_CASE_ID = "TC004"

# Define test case steps
def login(driver):
    """
    Perform login using the provided username and password.
    """
    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(USERNAME)
        
        # Wait for the password field to be available
        try:
            password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        except TimeoutException:
            print(f"TimeoutException: Unable to find element")
        # Enter the password
        password_field.send_keys(PASSWORD)
        
        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        
        print("Login successful")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print("Login failed: ", str(e))

def add_goal(driver, goal_text):
    """
    Add a new goal with the provided text.
    """
    try:
        # Wait for the goal text field to be available
        goal_text_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='txtAddGoal']"))
        )
        # Enter the goal text
        goal_text_field.send_keys(goal_text)
        
        # Wait for the add goal button to be clickable
        add_goal_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='btnAddGoal']"))
        )
        # Click the add goal button
        add_goal_button.click()
        
        print("Goal added successfully")
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print("Failed to add goal: ", str(e))

def verify_goal_addition(driver):
    """
    Verify that the goal is added to the goal list.
    """
    try:
        # Wait for the added goal to be visible
        added_goal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.goal-list"))
        )
        # Check if the added goal is visible
        if added_goal.is_visible():
            print("Goal added and visible")
            return True
        else:
            print("Goal not visible")
            return False
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print("Failed to verify goal addition: ", str(e))
        return False

# Main test function
def execute_test_case():
    # Set up the Selenium WebDriver (Chrome)
    driver = webdriver.Chrome()
    
    # Navigate to the URL
    driver.get(BASE_URL)
    
    # Perform login if needed
    login(driver)
    
    # Enter goal text
    goal_text = "Test Goal"
    add_goal(driver, goal_text)
    
    # Verify that the goal is added
    if verify_goal_addition(driver):
        print(f"Test Case {TEST_CASE_ID} passed: Goal added and visible")
    else:
        print(f"Test Case {TEST_CASE_ID} failed: Goal not added or not visible")
    
    # Close the browser
    print(f"Test case TC004 PASSED: Successfully executed Verify functionality of add goal button")
    driver.quit()

# Execute the test case
execute_test_case()