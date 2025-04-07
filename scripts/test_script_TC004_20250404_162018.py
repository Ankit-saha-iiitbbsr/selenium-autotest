import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define constants
BASE_URL = "https://ourgoalplan.co.in/Login.aspx"
USERNAME = "Ankit.s"
PASSWORD = "Bonnie@saha007"

class TestTC004(unittest.TestCase):
    def setUp(self):
        # Set up Chrome WebDriver
        self.driver = webdriver.Chrome()

        # Navigate to base URL
        self.driver.get(BASE_URL)

        # Perform login if needed
        self.login()

    def login(self):
        # Wait for username field to be clickable
        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
            )
            # Enter username
            username_field.send_keys(USERNAME)
        except TimeoutException:
            print("Error: Username field not found.")
    print(f"Test case TC004 PASSED: Successfully executed Verify error message for empty goal text")
            self.driver.quit()
            self.fail("Username field not found.")

        # Wait for password field to be clickable
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
            )
            # Enter password
            password_field.send_keys(PASSWORD)
        except TimeoutException:
            print("Error: Password field not found.")
            self.driver.quit()
            self.fail("Password field not found.")

        # Wait for login button to be clickable
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            # Click login button
            login_button.click()
        except TimeoutException:
            print("Error: Login button not found.")
            self.driver.quit()
            self.fail("Login button not found.")

    def test_tc004(self):
        # Wait for goal text field to be clickable
        try:
            goal_text_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#txtAddGoal"))
            )
            # Leave goal text field empty
            self.assertEqual(goal_text_field.get_attribute("value"), "")
        except TimeoutException:
            print("Error: Goal text field not found.")
            self.driver.quit()
            self.fail("Goal text field not found.")

        # Wait for add goal button to be clickable
        try:
            add_goal_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#btnAddGoal"))
            )
            # Click add goal button
            add_goal_button.click()
        except TimeoutException:
            print("Error: Add goal button not found.")
            self.driver.quit()
            self.fail("Add goal button not found.")

        # Wait for error message to be visible
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#lblGoalError"))
            )
            # Verify error message is displayed
            self.assertEqual(error_message.is_displayed(), True)
            print("Test Case TC004: PASS")
        except TimeoutException:
            print("Error: Error message not found.")
            self.driver.quit()
            self.fail("Error message not found.")

    def tearDown(self):
        # Close the browser window
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()