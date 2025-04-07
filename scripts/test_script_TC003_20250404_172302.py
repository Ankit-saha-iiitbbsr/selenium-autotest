from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Constants
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"
TEST_CASE_ID = "TC003"
GOAL_DESCRIPTION = "Complete Q1 Project Deliverables"
DUE_DATE = "05/31/2024"

def setup_driver():
    """Setup and initialize the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login(driver):
    """Perform login with provided credentials."""
    try:
        print("Navigating to login page...")
        driver.get(BASE_URL)
        
        print("Waiting for login form...")
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        
        print("Entering credentials...")
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        login_button.click()
        
        print("Login successful")
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Login failed: {str(e)}")
        return False

def create_goal(driver):
    """Create a new goal with specified details."""
    try:
        print("Navigating to goal creation page...")
        driver.get("https://ourgoalplan.co.in/CreateGoal.aspx")
        
        print("Waiting for goal creation form...")
        description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='goalDescription']"))
        )
        due_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='dueDate']"))
        )
        create_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'][name='createGoal']"))
        )
        
        print("Filling goal details...")
        description.send_keys(GOAL_DESCRIPTION)
        due_date.clear()
        due_date.send_keys(DUE_DATE)
        time.sleep(1)  # Small delay for date input to be registered
        create_button.click()
        
        print("Goal creation form submitted successfully")
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error creating goal: {str(e)}")
        return False

def verify_goal_creation(driver):
    """Verify that the goal is created and displayed."""
    try:
        print("Waiting for goals list to load...")
        goals_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.goal-list"))
        )
        
        print("Checking for newly created goal...")
        goal_elements = goals_list.find_elements(By.CSS_SELECTOR, "div.goal-item")
        for goal in goal_elements:
            if GOAL_DESCRIPTION in goal.text and DUE_DATE in goal.text:
                print("Goal verification successful")
                return True
        print("Goal not found in list")
        return False
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error verifying goal creation: {str(e)}")
        return False

def main():
    """Main function to execute the test case."""
    try:
        print(f"Starting test case {TEST_CASE_ID}: Test form validation for goal creation")
        driver = setup_driver()
        
        if not login(driver):
            print(f"Test {TEST_CASE_ID} failed: Login failed")
            return
        
        if not create_goal(driver):
            print(f"Test {TEST_CASE_ID} failed: Goal creation failed")
            return
        
        if not verify_goal_creation(driver):
            print(f"Test {TEST_CASE_ID} failed: Goal verification failed")
            return
        
        print(f"Test {TEST_CASE_ID} passed: Goal created and verified successfully")
        
    except Exception as e:
        print(f"Test {TEST_CASE_ID} failed with exception: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()