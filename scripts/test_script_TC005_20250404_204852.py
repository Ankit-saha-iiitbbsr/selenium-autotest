# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    """
    Set up the Selenium WebDriver (Chrome)
    """
    # Create a new Chrome driver instance
    driver = webdriver.Chrome()
    return driver

def navigate_to_url(driver, url):
    """
    Navigate to the given URL
    """
    # Navigate to the URL
    driver.get(url)

def perform_login(driver, username, password):
    """
    Perform login if needed
    """
    try:
        # Wait for the username field to be visible
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        # Wait for the password field to be visible
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        # Wait for the login button to be visible
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Enter the username
        username_field.send_keys(username)
        # Enter the password
        password_field.send_keys(password)
        # Click the login button
        login_button.click()
        print("Login successful")
    except TimeoutException:
        print("Login fields not found")

def execute_test_steps(driver, test_case):
    """
    Execute all test steps using proper waits and assertions
    """
    try:
        # Wait for the search field to be visible
        search_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_case['selectors']['target_elements'][0]['selector']))
        )
        # Enter a search query in the search field
        search_field.send_keys("test query")
        print("Search query entered")

        # Wait for the search button to be clickable
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, test_case['selectors']['target_elements'][1]['selector']))
        )
        # Click the search button
        search_button.click()
        print("Search button clicked")

        # Wait for the search results to be visible
        search_results = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, test_case['selectors']['verification_elements'][0]['selector']))
        )
        # Assert that search results are displayed
        assert search_results.is_displayed()
        print("Search results are displayed")

        print(f"Test case {test_case['id']} passed")
        return True
    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        print(f"Test case {test_case['id']} failed: {str(e)}")
        return False

def main():
    # Set up the test case
    test_case = {
        "id": "TC005",
        "name": "Verify search functionality",
        "type": "positive",
        "priority": "low",
        "steps": [
            "Enter a search query in the search field",
            "Click the 'go' button"
        ],
        "expected_result": "Search results should be displayed",
        "selectors": {
            "target_elements": [
                {
                    "name": "search_field",
                    "selector": "input[name='searchFor']"
                },
                {
                    "name": "search_button",
                    "selector": "input[name='goButton']"
                }
            ],
            "verification_elements": [
                {
                    "name": "search_results",
                    "selector": "div.search-results"
                }
            ]
        }
    }

    # Set up the base URL, username, and password
    base_url = "http://testphp.vulnweb.com/login.php"
    username = "test"
    password = "test"

    # Set up the driver
    driver = setup_driver()

    # Navigate to the URL
    navigate_to_url(driver, base_url)

    # Perform login if needed
    perform_login(driver, username, password)

    # Execute the test steps
    result = execute_test_steps(driver, test_case)

    # Close the driver
    driver.quit()

    # Print the test result
    print(f"Test case {test_case['id']} {'passed' if result else 'failed'}")

if __name__ == "__main__":
    main()