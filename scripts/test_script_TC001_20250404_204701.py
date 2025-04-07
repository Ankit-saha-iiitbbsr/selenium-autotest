# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    """
    try:
        # Set up Chrome WebDriver
        logging.info("Setting up Chrome WebDriver...")
        webdriver_path = "/path/to/chromedriver"  # Update with your chromedriver path
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
        driver.maximize_window()
        return driver
    except WebDriverException as e:
        logging.error(f"Error setting up WebDriver: {e}")
        return None

def navigate_to_url(driver, url):
    """
    Navigate to the given URL.
    """
    try:
        logging.info(f"Navigating to {url}...")
        driver.get(url)
    except WebDriverException as e:
        logging.error(f"Error navigating to URL: {e}")

def login(driver, username, password):
    """
    Perform login with the given username and password.
    """
    try:
        # Wait for username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Enter username
        username_field.send_keys(username)
        
        # Wait for password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Enter password
        password_field.send_keys(password)
        
        # Wait for login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Click login button
        login_button.click()
        
        logging.info("Login successful.")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error during login: {e}")

def fill_update_form(driver, name, credit_card, email, phone, address):
    """
    Fill the update form with the given details.
    """
    try:
        # Wait for name field to be visible
        name_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='urname']"))
        )
        # Enter name
        name_field.send_keys(name)
        
        # Wait for credit card field to be visible
        credit_card_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='ucc']"))
        )
        # Enter credit card number
        credit_card_field.send_keys(credit_card)
        
        # Wait for email field to be visible
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='uemail']"))
        )
        # Enter email
        email_field.send_keys(email)
        
        # Wait for phone number field to be visible
        phone_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='uphone']"))
        )
        # Enter phone number
        phone_field.send_keys(phone)
        
        # Wait for address field to be visible
        address_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[name='uaddress']"))
        )
        # Enter address
        address_field.send_keys(address)
        
        logging.info("Update form filled successfully.")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error filling update form: {e}")

def submit_update_form(driver):
    """
    Submit the update form.
    """
    try:
        # Wait for update button to be clickable
        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='update']"))
        )
        # Click update button
        update_button.click()
        
        logging.info("Update form submitted successfully.")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error submitting update form: {e}")

def verify_update_message(driver):
    """
    Verify the update message.
    """
    try:
        # Wait for update message to be visible
        update_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.story"))
        )
        # Check if update message is displayed
        if update_message.is_displayed():
            logging.info("Update message verified successfully.")
            return True
        else:
            logging.error("Update message not found.")
            return False
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error verifying update message: {e}")
        return False

def main():
    # Set up WebDriver
    driver = setup_webdriver()
    
    if driver:
        # Navigate to URL
        navigate_to_url(driver, "http://testphp.vulnweb.com/login.php")
        
        # Login
        login(driver, "test", "test")
        
        # Fill update form
        fill_update_form(driver, "John Doe", "1234-5678-9012-3456", "johndoe@example.com", "123-456-7890", "123 Main St")
        
        # Submit update form
        submit_update_form(driver)
        
        # Verify update message
        update_message_verified = verify_update_message(driver)
        
        # Print test result
        if update_message_verified:
            logging.info(f"Test Case TC001: Passed")
        else:
            logging.error(f"Test Case TC001: Failed")
        
        # Close WebDriver
        driver.quit()
    else:
        logging.error("WebDriver setup failed.")

if __name__ == "__main__":
    main()