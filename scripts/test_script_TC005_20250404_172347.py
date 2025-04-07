from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

# Test case details
TEST_CASE_ID = "TC005"
TEST_CASE_NAME = "Test UI responsiveness on different screen sizes"
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"

# Define window sizes to test
WINDOW_SIZES = [
    (1920, 1080),
    (1366, 768),
    (414, 896),  # Mobile view
    (800, 600)
]

def setup_driver():
    """Setup Chrome WebDriver with desired options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        sys.exit(1)

def login(driver):
    """Perform login with provided credentials."""
    try:
        # Wait for login page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Enter username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.send_keys(USERNAME)
        
        # Enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys(PASSWORD)
        
        # Click login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
        # Wait for dashboard to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.main-container"))
        )
        print("Successfully logged in")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def test_ui_responsiveness(driver):
    """Test UI responsiveness across different screen sizes."""
    try:
        # Navigate to base URL
        driver.get(BASE_URL)
        
        # Perform login if needed
        if not login(driver):
            return False
            
        # List of resolutions to test
        resolutions = WINDOW_SIZES
        
        # Elements to verify
        verification_elements = [
            {"name": "main_container", "selector": "div.main-container"},
            {"name": "header", "selector": "header.navbar"},
            {"name": "sidebar", "selector": "div.sidebar"},
            {"name": "goal_list", "selector": "div.goal-list"},
            {"name": "action_list", "selector": "div.action-list"}
        ]
        
        # Test each resolution
        all_responsive = True
        for width, height in resolutions:
            print(f"\nTesting resolution: {width}x{height}")
            
            # Resize window
            driver.set_window_size(width, height)
            time.sleep(1)  # Allow UI to adjust
            
            # Verify all elements are present and visible
            for element in verification_elements:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, element["selector"]))
                    )
                    print(f"✓ {element['name']} is visible at {width}x{height}")
                except Exception as e:
                    print(f"✗ {element['name']} is NOT visible at {width}x{height}")
                    print(f"Error: {str(e)}")
                    all_responsive = False
                    # Take screenshot for debugging
                    driver.save_screenshot(f"failed_ui_{width}x{height}.png")
                    
        return all_responsive
            
    except Exception as e:
        print(f"Error during UI responsiveness test: {e}")
        return False

def main():
    """Main function to execute test case."""
    try:
        print(f"Starting test case {TEST_CASE_ID}: {TEST_CASE_NAME}")
        driver = setup_driver()
        
        if not driver:
            print("Failed to initialize WebDriver")
            return
            
        try:
            # Navigate to base URL
            driver.get(BASE_URL)
            
            # Perform UI responsiveness test
            is_responsive = test_ui_responsiveness(driver)
            
            # Print test result
            if is_responsive:
                print(f"\nTest case {TEST_CASE_ID} PASSED: All UI elements are responsive across different screen sizes")
            else:
                print(f"\nTest case {TEST_CASE_ID} FAILED: UI responsiveness issues detected")
                
        except Exception as e:
            print(f"Test execution failed: {e}")
            return
            
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        # Clean up
        driver.quit()
        print("\nTest execution completed")

if __name__ == "__main__":
    main()