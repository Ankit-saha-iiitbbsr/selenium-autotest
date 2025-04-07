# # Import required libraries
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import logging
# from webdriver_manager.chrome import ChromeDriverManager
# # Add at the top of the file
# from selenium.webdriver.chrome.service import Service
# import logging

# # Set up logging configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Test case constants
# BASE_URL = 'https://practicetestautomation.com/practice-test-login/'
# USERNAME = 'student'
# PASSWORD = 'Password123'
# TEST_CASE_ID = 'TC004'

# # Set up Chrome WebDriver
# def setup_webdriver():
#     # Create Chrome options
#     options = webdriver.ChromeOptions()
#     options.add_argument('--start-maximized')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
    
#     try:
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)
#         return driver
#     except Exception as e:
#         logging.error(f"Driver setup failed: {str(e)}")
#         raise

# # Navigate to the base URL and perform login if needed
# def navigate_to_url_and_login(driver):
#     # Navigate to the base URL
#     driver.get(BASE_URL)
#     logging.info(f'Navigated to {BASE_URL}')
    
#     # Wait for the username field to be visible
#     username_field = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
#     )
#     logging.info('Username field is visible')
    
#     # Enter username
#     username_field.send_keys(USERNAME)
#     logging.info(f'Entered username: {USERNAME}')
    
#     # Wait for the password field to be visible
#     password_field = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
#     )
#     logging.info('Password field is visible')
    
#     # Enter password
#     password_field.send_keys(PASSWORD)
#     logging.info(f'Entered password: {PASSWORD}')
    
#     # Wait for the login button to be visible
#     login_button = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
#     )
#     logging.info('Login button is visible')
    
#     # Click the login button
#     login_button.click()
#     logging.info('Clicked the login button')

# # Verify responsiveness of the page
# def verify_responsiveness(driver):
#     # Add viewport testing
#     screen_sizes = [
#         (1920, 1080),  # Desktop
#         (414, 896),    # Mobile
#         (768, 1024)    # Tablet
#     ]

#     # Define page header and footer selectors
#     page_header_selector = 'header'
#     page_footer_selector = 'footer'
    
#     # Wait for the page to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, 'body'))
#     )
#     logging.info('Page has finished loading')
    
#     # Wait for the page header to be visible
#     page_header = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.TAG_NAME, page_header_selector))
#     )
#     logging.info('Page header is visible')
    
#     # Wait for the page footer to be visible
#     page_footer = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.TAG_NAME, page_footer_selector))
#     )
#     logging.info('Page footer is visible')
    
#     # # Verify the page layout adapts to the screen size
#     # try:
#     #     # Assume the page layout adapts to the screen size
#     #     logging.info('Page layout seems to adapt to the screen size')
#     # except Exception as e:
#     #     # Handle any exceptions during responsiveness verification
#     #     logging.error(f'Error verifying responsiveness: {str(e)}')
#     #     return False
#     # return True
#     try:
#         for width, height in screen_sizes:
#             driver.set_window_size(width, height)
#             WebDriverWait(driver, 5).until(
#                 EC.presence_of_element_located((By.TAG_NAME, 'main'))
#             )
#             logging.info(f"Layout verified at {width}x{height}")
#         return True
#     except Exception as e:
#         logging.error(f"Responsiveness check failed: {str(e)}")
#         return False


# # Main function to execute the test case
# def execute_test_case():
#     # try:
#     #     # Set up the WebDriver
#     #     driver = setup_webdriver()
#     #     logging.info('WebDriver set up successfully')
        
#     #     # Navigate to the URL and perform login
#     #     navigate_to_url_and_login(driver)
        
#     #     # Verify the responsiveness of the page
#     #     if verify_responsiveness(driver):
#     #         logging.info(f'Test Case {TEST_CASE_ID} passed: Page layout adapts to the screen size')
#     #     else:
#     #         logging.error(f'Test Case {TEST_CASE_ID} failed: Page layout does not adapt to the screen size')
#     # except Exception as e:
#     #     # Handle any exceptions during test case execution
#     #     logging.error(f'Test Case {TEST_CASE_ID} failed: {str(e)}')
#     # finally:
#     #     # Close the WebDriver
#     #     try:
#     #         driver.quit()
#     #         logging.info('WebDriver quit successfully')
#     #     except Exception as e:
#     #         # Handle any exceptions during WebDriver quit
#     #         logging.error(f'Error quitting WebDriver: {str(e)}')
#     driver = None
#     try:
#         driver = setup_webdriver()
#         # Rest of the implementation
#     except Exception as e:
#         logging.error(f"Test Case {TEST_CASE_ID} failed during setup: {str(e)}")
#     finally:
#         if driver:
#             try:
#                 driver.save_screenshot(f"TC004_failure_{datetime.now().isoformat()}.png")
#                 driver.quit()
#             except Exception as e:
#                 logging.error(f"Cleanup failed: {str(e)}")

# # Execute the test case
# if __name__ == '__main__':
#     execute_test_case()

# test_script_TC004.py - Fixed Version
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'tc004_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

# Constants
BASE_URL = 'https://practicetestautomation.com/practice-test-login/'
USERNAME = 'student'
PASSWORD = 'Password123'
TEST_CASE_ID = 'TC004'
VIEWPORTS = [
    (1920, 1080),  # Desktop
    (414, 896),     # iPhone X
    (768, 1024),    # iPad
    (360, 640)      # Small mobile
]

def setup_webdriver():
    """Set up Chrome WebDriver with automatic management"""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logging.info('Chrome WebDriver initialized successfully')
        return driver
    except Exception as e:
        logging.error(f'Driver setup failed: {str(e)}')
        raise

def navigate_and_login(driver):
    """Navigate to URL and perform login"""
    try:
        # Navigate to base URL
        driver.get(BASE_URL)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
        logging.info(f'Navigated to {BASE_URL}')

        # Perform login
        driver.find_element(By.CSS_SELECTOR, 'input[name="username"]').send_keys(USERNAME)
        driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Verify successful login
        WebDriverWait(driver, 15).until(
            EC.url_contains('logged-in-successfully'))
        logging.info('Login successful')
        return True
        
    except Exception as e:
        logging.error(f'Navigation/login failed: {str(e)}')
        driver.save_screenshot(f'{TEST_CASE_ID}_login_failure.png')
        return False

def check_viewport_meta(driver):
    """Verify viewport meta tag configuration"""
    try:
        viewport_meta = driver.find_element(By.CSS_SELECTOR, 'meta[name="viewport"]')
        content = viewport_meta.get_attribute('content')
        if 'width=device-width' in content:
            logging.info('Viewport meta tag configured correctly')
            return True
        logging.warning('Viewport meta tag missing device-width')
        return False
    except NoSuchElementException:
        logging.warning('Viewport meta tag not found')
        return False

def verify_responsiveness(driver):
    """Test responsiveness across different viewports"""
    try:
        results = []
        for width, height in VIEWPORTS:
            try:
                driver.set_window_size(width, height)
                
                # Wait for stabilization
                WebDriverWait(driver, 5).until(
                    lambda d: d.execute_script('return document.readyState === "complete"'))
                
                # Verify critical elements
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'main, .main-content')))
                
                # Check element positioning
                header = driver.find_element(By.TAG_NAME, 'header')
                assert header.location['y'] < 100, "Header positioning incorrect"
                
                logging.info(f'Viewport {width}x{height} verified')
                results.append(True)
                
            except Exception as e:
                logging.error(f'Failed at {width}x{height}: {str(e)}')
                driver.save_screenshot(f'{TEST_CASE_ID}_failure_{width}x{height}.png')
                results.append(False)
        
        return all(results)
        
    except Exception as e:
        logging.error(f'Responsiveness test failed: {str(e)}')
        return False

def execute_test_case():
    """Main test execution flow"""
    driver = None
    try:
        driver = setup_webdriver()
        
        if not navigate_and_login(driver):
            raise Exception("Login failed")
            
        if not check_viewport_meta(driver):
            logging.warning('Viewport meta issues detected')
            
        if not verify_responsiveness(driver):
            raise Exception("Responsiveness verification failed")
            
        logging.info(f'Test Case {TEST_CASE_ID} PASSED')
        return True
        
    except Exception as e:
        logging.error(f'Test Case {TEST_CASE_ID} FAILED: {str(e)}')
        if driver:
            driver.save_screenshot(f'{TEST_CASE_ID}_final_failure.png')
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                logging.info('Browser closed successfully')
            except Exception as e:
                logging.error(f'Browser cleanup failed: {str(e)}')

if __name__ == '__main__':
    execute_test_case()