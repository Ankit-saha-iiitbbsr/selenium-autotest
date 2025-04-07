# Import the necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
BASE_URL = 'https://practicetestautomation.com/practice-test-login/'
USERNAME = 'student'
PASSWORD = 'Password123'
TEST_CASE_ID = 'TC004'

def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    """
    try:
        # Create a new instance of the Chrome driver
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')  # Uncomment for headless mode
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        logging.error(f'Failed to set up WebDriver: {e}')
        return None

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL.
    """
    try:
        # Navigate to the URL
        driver.get(url)
        logging.info(f'Navigated to {url}')
    except WebDriverException as e:
        logging.error(f'Failed to navigate to {url}: {e}')

def perform_login(driver):
    """
    Perform the login using the provided username and password.
    """
    try:
        # Wait for the username field to be available
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter the username
        username_field.send_keys(USERNAME)
        logging.info('Entered username')
        
        # Wait for the password field to be available
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(PASSWORD)
        logging.info('Entered password')
        
        # Wait for the login button to be available
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
        logging.info('Clicked login button')
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f'Failed to perform login: {e}')

def verify_css_styles(driver):
    """
    Verify the expected CSS styles.
    """
    try:
        # Wait for the CSS style element to be available
        css_style_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "style[id='wp-emoji-styles-inline-css']"))
        )
        # Get the CSS style content
        css_style_content = css_style_element.get_attribute('innerHTML')
        logging.info('Retrieved CSS style content')
        
        # Verify the CSS style content is not empty
        assert css_style_content, 'CSS style content is empty'
        logging.info('Verified CSS style content')
    except (TimeoutException, AssertionError) as e:
        logging.error(f'Failed to verify CSS styles: {e}')
        return False
    return True

def main():
    # Set up the WebDriver
    driver = setup_webdriver()
    
    if driver:
        # Navigate to the URL
        navigate_to_url(driver, BASE_URL)
        
        # Perform the login
        perform_login(driver)
        
        # Verify the CSS styles
        css_styles_verified = verify_css_styles(driver)
        
        # Print the test result
        if css_styles_verified:
            logging.info(f'Test {TEST_CASE_ID} passed: CSS styles verified')
        else:
            logging.info(f'Test {TEST_CASE_ID} failed: CSS styles not verified')
        
        # Close the WebDriver
        driver.quit()
    else:
        logging.info(f'Test {TEST_CASE_ID} failed: Failed to set up WebDriver')

if __name__ == '__main__':
    main()