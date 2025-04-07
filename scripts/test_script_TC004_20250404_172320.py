from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Configuration
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"
TEST_CASE_ID = "TC004"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Explicit wait
wait = WebDriverWait(driver, 10)

try:
    # Step 1: Navigate to login page
    print(f"{TEST_CASE_ID} - Navigating to login page...")
    driver.get(BASE_URL)
    
    # Step 2: Login to the application
    print(f"{TEST_CASE_ID} - Performing login...")
    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    login_button.click()
    
    # Step 3: Navigate to goal creation page
    print(f"{TEST_CASE_ID} - Navigating to goal creation page...")
    time.sleep(2)  # Small delay to ensure page loads
    create_goal_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Create Goal")))
    create_goal_link.click()
    
    # Step 4: Perform test actions
    print(f"{TEST_CASE_ID} - Executing test steps...")
    
    # Leave goal description empty
    goal_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='goalDescription']")))
    # Clear any existing text (if any)
    goal_description.clear()
    
    # Select due date
    due_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='dueDate']")))
    due_date.send_keys("2024-01-31")  # Example future date
    
    # Click create goal button
    create_goal_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'][name='createGoal']")))
    create_goal_button.click()
    
    # Step 5: Verify error message
    print(f"{TEST_CASE_ID} - Verifying error message...")
    try:
        error_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.error-message")))
        if error_message.is_displayed():
            print(f"{TEST_CASE_ID} - Test PASSED: Error message displayed as expected")
            print(f"Error message text: {error_message.text}")
        else:
            print(f"{TEST_CASE_ID} - Test FAILED: Error message not displayed when expected")
    except TimeoutException:
        print(f"{TEST_CASE_ID} - Test FAILED: Error message did not appear within the expected timeframe")
    
except Exception as e:
    print(f"{TEST_CASE_ID} - Test FAILED with exception: {str(e)}")
    print("Stack trace:", e.__traceback__)

finally:
    # Clean up
    print(f"{TEST_CASE_ID} - Closing browser session...")
    driver.quit()