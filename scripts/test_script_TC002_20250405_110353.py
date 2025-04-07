# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """
    Set up the Selenium WebDriver for Chrome.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def navigate_to_url(driver, url):
    """
    Navigate to the given URL using the Selenium WebDriver.
    """
    driver.get(url)
    print(f"Navigated to {url}")

def login(driver, username, password):
    """
    Perform the login if needed.
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.send_keys(username)

        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys(password)

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()

        print("Logged in successfully")
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error logging in: {e}")

def execute_test_case(driver, test_case):
    """
    Execute the test case using proper waits and assertions.
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_field.send_keys("invalid_username")

        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys("invalid_password")

        # Wait for the login button to be clickable
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()

        # Wait for the error message to be visible
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#error-message"))
        )

        print(f"Test case {test_case['id']} passed: Error message is displayed")
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Test case {test_case['id']} failed: {e}")
        return False

def main():
    # Define the base URL and test case
    base_url = "https://practicetestautomation.com/practice-test-login/"
    test_case = {
        "id": "TC002",
        "name": "Verify unsuccessful login with invalid credentials",
        "type": "functional_negative",
        "category": "authentication",
        "priority": "medium",
        "steps": [
            "Enter invalid username",
            "Enter invalid password",
            "Click login button"
        ],
        "expected_result": "Error message should be displayed",
        "selectors": {
            "target_elements": [
                {
                    "name": "username_field",
                    "selector": "input[name='username']"
                },
                {
                    "name": "password_field",
                    "selector": "input[name='password']"
                },
                {
                    "name": "login_button",
                    "selector": "button[type='submit']"
                }
            ],
            "verification_elements": [
                {
                    "name": "error_message",
                    "selector": "div#error-message"
                }
            ]
        }
    }

    # Set up the Selenium WebDriver
    driver = setup_driver()

    # Navigate to the URL
    navigate_to_url(driver, base_url)

    # Perform the login if needed
    login(driver, "student", "Password123")

    # Execute the test case
    result = execute_test_case(driver, test_case)

    # Print the test result
    if result:
        print(f"Test case {test_case['id']} passed")
    else:
        print(f"Test case {test_case['id']} failed")

    # Close the Selenium WebDriver
    driver.quit()

if __name__ == "__main__":
    main()