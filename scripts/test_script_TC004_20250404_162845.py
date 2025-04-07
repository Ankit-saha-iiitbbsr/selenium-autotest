# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    """
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    return driver

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL.
    """
    driver.get(url)

def login(driver, username, password):
    """
    Perform the login using the provided username and password.
    """
    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(username)
        
        # Wait for the password field to be available
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(password)
        
        # Wait for the login button to be available
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        
        logging.info("Login successful")
    except TimeoutException:
        logging.error("Login failed: Timeout waiting for login elements")
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")

def add_goal(driver, goal):
    """
    Add a new goal to the list.
    """
    try:
        # Wait for the goal input field to be available
        goal_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='txtAddGoal']"))
        )
        # Enter the goal
        goal_input.send_keys(goal)
        
        # Wait for the add goal button to be available
        add_goal_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[id='btnAddGoal']"))
        )
        # Click the add goal button
        add_goal_button.click()
        
        logging.info("Goal added successfully")
    except TimeoutException:
        logging.error("Failed to add goal: Timeout waiting for goal elements")
    except Exception as e:
        logging.error(f"Failed to add goal: {str(e)}")

def verify_goal_added(driver, goal):
    """
    Verify that the new goal is added to the list.
    """
    try:
        # Wait for the goal list to be available
        goal_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.goal-list"))
        )
        
        # Check if the goal is in the list
        if goal in goal_list.text:
            logging.info("Goal added to the list successfully")
            return True
        else:
            logging.error("Goal not found in the list")
            return False
    except TimeoutException:
        logging.error("Failed to verify goal: Timeout waiting for goal list")
    except Exception as e:
        logging.error(f"Failed to verify goal: {str(e)}")
    return False

def main():
    base_url = "https://ourgoalplan.co.in/Login.aspx"
    username = "Ankit.s"
    password = "Bonnie@saha007"
    goal = "New Goal"
    test_case_id = "TC004"
    
    # Set up the WebDriver
    driver = setup_webdriver()
    
    try:
        # Navigate to the URL
        navigate_to_url(driver, base_url)
        
        # Login
        login(driver, username, password)
        
        # Add a new goal
        add_goal(driver, goal)
        
        # Verify the goal is added
        if verify_goal_added(driver, goal):
            print(f"Test Case {test_case_id}: PASS")
        else:
            print(f"Test Case {test_case_id}: FAIL")
    except Exception as e:
        print(f"Test Case {test_case_id}: FAIL - {str(e)}")
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()