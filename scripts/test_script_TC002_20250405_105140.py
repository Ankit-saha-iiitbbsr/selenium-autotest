# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    
    Returns:
    driver (webdriver): The set up WebDriver instance.
    """
    # Create a new instance of the Chrome driver
    logging.info('Setting up Chrome WebDriver...')
    driver = webdriver.Chrome()
    return driver

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL.
    
    Args:
    driver (webdriver): The WebDriver instance.
    url (str): The URL to navigate to.
    """
    # Navigate to the specified URL
    logging.info(f'Navigating to {url}...')
    driver.get(url)

def perform_login(driver, username, password):
    """
    Perform the login action.
    
    Args:
    driver (webdriver): The WebDriver instance.
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
        
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter the password
        password_field.send_keys(password)
        
        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click the login button
        login_button.click()
    except TimeoutException:
        logging.error('Failed to perform login due to timeout.')
    except Exception as e:
        logging.error(f'Failed to perform login: {str(e)}')

def verify_meta_tags(driver):
    """
    Verify the required meta tags are present in the page.
    
    Args:
    driver (webdriver): The WebDriver instance.
    
    Returns:
    bool: True if the required meta tags are present, False otherwise.
    """
    try:
        # Wait for the meta description tag to be present
        meta_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "meta[name='description']"))
        )
        
        # Wait for the meta keywords tag to be present
        meta_keywords = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "meta[name='keywords']"))
        )
        
        # Get the content attribute of the meta description tag
        meta_description_content = driver.find_element(By.CSS_SELECTOR, "meta[name='description']").get_attribute('content')
        
        # If both tags are present and the meta description tag has content, return True
        if meta_description and meta_keywords and meta_description_content:
            logging.info('Required meta tags are present and valid.')
            return True
        else:
            logging.error('Required meta tags are missing or invalid.')
            return False
    except TimeoutException:
        logging.error('Failed to verify meta tags due to timeout.')
        return False
    except Exception as e:
        logging.error(f'Failed to verify meta tags: {str(e)}')
        return False

def main():
    # Define the test case ID
    test_case_id = 'TC002'
    
    # Define the base URL
    base_url = 'https://practicetestautomation.com/practice-test-login/'
    
    # Define the username and password for login
    username = 'student'
    password = 'Password123'
    
    try:
        # Set up the WebDriver
        driver = setup_webdriver()
        
        # Navigate to the URL
        navigate_to_url(driver, base_url)
        
        # Perform the login if needed
        perform_login(driver, username, password)
        
        # Verify the meta tags
        if verify_meta_tags(driver):
            logging.info(f'Test case {test_case_id} passed: Meta tags are present and valid.')
        else:
            logging.error(f'Test case {test_case_id} failed: Meta tags are missing or invalid.')
    except Exception as e:
        logging.error(f'Test case {test_case_id} encountered an error: {str(e)}')
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == '__main__':
    main()