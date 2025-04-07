# Import required libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """
    Set up the Selenium WebDriver with Chrome.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def navigate_to_url(driver, url):
    """
    Navigate to the specified URL.
    """
    driver.get(url)
    logging.info(f"Navigated to {url}")

def perform_login(driver, base_url, username, password):
    """
    Perform login using the provided credentials.
    """
    username_field_selector = "input[name='username']"
    password_field_selector = "input[name='password']"
    login_button_selector = "button[type='submit']"

    # Navigate to the login page
    login_url = f"{base_url}"
    driver.get(login_url)
    logging.info(f"Navigated to the login page: {login_url}")

    # Wait for the username field to be visible
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, username_field_selector))
        )
    except TimeoutException:
        logging.error("Username field not found")
        return False

    # Enter the username
    username_field.send_keys(username)
    logging.info(f"Entered username: {username}")

    # Wait for the password field to be visible
    try:
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, password_field_selector))
        )
    except TimeoutException:
        logging.error("Password field not found")
        return False

    # Enter the password
    password_field.send_keys(password)
    logging.info(f"Entered password: {password}")

    # Wait for the login button to be clickable
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, login_button_selector))
        )
    except TimeoutException:
        logging.error("Login button not found")
        return False

    # Click the login button
    login_button.click()
    logging.info("Clicked the login button")

    return True

def verify_navigation_menu(driver, base_url):
    """
    Verify the navigation menu functionality.
    """
    nav_menu_selector = "nav"
    nav_item_1_selector = "nav > ul > li:first-child"
    nav_item_2_selector = "nav > ul > li:nth-child(2)"

    # Navigate to the main page
    driver.get(base_url)
    logging.info(f"Navigated to the main page: {base_url}")

    # Wait for the navigation menu to be visible
    try:
        nav_menu = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, nav_menu_selector))
        )
    except TimeoutException:
        logging.error("Navigation menu not found")
        return False

    # Wait for the first navigation item to be clickable
    try:
        nav_item_1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, nav_item_1_selector))
        )
    except TimeoutException:
        logging.error("First navigation item not found")
        return False

    # Click the first navigation item
    nav_item_1.click()
    logging.info("Clicked the first navigation item")

    # Verify the current URL
    current_url = driver.current_url
    logging.info(f"Current URL: {current_url}")

    # Wait for the second navigation item to be clickable
    try:
        nav_item_2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, nav_item_2_selector))
        )
    except TimeoutException:
        logging.error("Second navigation item not found")
        return False

    # Click the second navigation item
    nav_item_2.click()
    logging.info("Clicked the second navigation item")

    # Verify the current URL
    current_url = driver.current_url
    logging.info(f"Current URL: {current_url}")

    return True

def main():
    # Set up the Selenium WebDriver
    driver = setup_driver()
    logging.info("Selenium WebDriver set up")

    # Define the test case details
    test_case_id = "TC005"
    base_url = "https://practicetestautomation.com/practice-test-login/"
    username = "student"
    password = "Password123"

    # Perform the login
    if perform_login(driver, base_url, username, password):
        logging.info("Login successful")
    else:
        logging.error("Login failed")
        driver.quit()
        return

    # Verify the navigation menu
    if verify_navigation_menu(driver, base_url):
        logging.info(f"Test case {test_case_id} passed")
    else:
        logging.error(f"Test case {test_case_id} failed")

    # Quit the Selenium WebDriver
    driver.quit()
    logging.info("Selenium WebDriver quit")

if __name__ == "__main__":
    main()