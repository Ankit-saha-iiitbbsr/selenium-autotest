# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define a function to set up the Selenium WebDriver
def setup_webdriver():
    """
    Set up the Selenium WebDriver with Chrome.
    """
    # Create a new instance of the Chrome driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

# Define a function to navigate to the URL and perform login
def navigate_and_login(driver, base_url, username, password):
    """
    Navigate to the URL and perform login if needed.

    Args:
        driver (webdriver): The Selenium WebDriver.
        base_url (str): The base URL of the application.
        username (str): The username for login.
        password (str): The password for login.
    """
    # Navigate to the base URL
    driver.get(base_url)

    try:
        # Check if the login page is displayed
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        if login_button:
            # Perform login
            username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
            password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

            # Enter username and password
            username_field.send_keys(username)
            password_field.send_keys(password)

            # Click the login button
            login_button.click()

            # Wait for the login to be successful
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element((By.CSS_SELECTOR, "button[type='submit']"))
            )
            print("Login successful")
    except TimeoutException:
        print("No login required")

# Define a function to execute the test steps
def execute_test_steps(driver, test_case):
    """
    Execute the test steps.

    Args:
        driver (webdriver): The Selenium WebDriver.
        test_case (dict): The test case dictionary.
    """
    try:
        # Click on the 'Your cart' link in the navigation bar
        cart_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, test_case["selectors"]["target_elements"][0]["selector"]))
        )
        cart_link.click()
        print(f"Clicked on the 'Your cart' link")

        # Verify the cart page is displayed
        cart_page_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, test_case["selectors"]["verification_elements"][0]["selector"]))
        )
        print(f"Cart page header: {cart_page_header.text}")

        # Verify the expected result
        assert cart_page_header.is_displayed()
        print(f"Test case {test_case['id']} passed")
    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        print(f"Test case {test_case['id']} failed: {str(e)}")

# Define a function to run the test case
def run_test_case(test_case, base_url, username, password):
    """
    Run the test case.

    Args:
        test_case (dict): The test case dictionary.
        base_url (str): The base URL of the application.
        username (str): The username for login.
        password (str): The password for login.
    """
    # Set up the Selenium WebDriver
    driver = setup_webdriver()

    try:
        # Navigate to the URL and perform login
        navigate_and_login(driver, base_url, username, password)

        # Execute the test steps
        execute_test_steps(driver, test_case)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the Selenium WebDriver
        driver.quit()

# Define the test case and run it
test_case = {
    "id": "TC004",
    "name": "Verify navigation to cart page",
    "type": "positive",
    "priority": "low",
    "steps": ["Click on the 'Your cart' link in the navigation bar"],
    "expected_result": "User should be redirected to the cart page",
    "selectors": {
        "target_elements": [{"name": "cart_link", "selector": "a[href='cart.php']"}],
        "verification_elements": [{"name": "cart_page_header", "selector": "h2"}],
    },
}
base_url = "http://testphp.vulnweb.com/login.php"
username = "test"
password = "test"

run_test_case(test_case, base_url, username, password)