import os
import json
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import groq
import base64
from io import BytesIO
from PIL import Image
import argparse

import logging
import os
from datetime import datetime

# Load environment variables
load_dotenv()

class WebTestGenerator:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama-3.3-70b-versatile"
        self.client = groq.Client(api_key=self.groq_api_key)
        self.driver = None
        self.alternative_selectors = {}  # Add this line
        #self.headless = headless
        self.setup_browser()
        self.logger = self.setup_logging()  # Add this line
        
    def setup_browser(self):
        """Set up the Chrome browser with appropriate options."""
        chrome_options = Options()
        #if self.headless:
        #    chrome_options.add_argument("--headless")
        chrome_options.add_argument("--headless")  # Run in headless mode (optional)
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def capture_screenshot(self):
        """Capture screenshot and convert to base64 for LLM analysis."""
        screenshot = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def setup_logging(self):
        """Set up logging configuration for better debugging."""
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        # Configure logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/test_run_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("WebTestGenerator")
        self.logger.info(f"Starting new test run at {timestamp}")
        return self.logger
    
    def save_debug_screenshot(self, name):
        """Save a screenshot for debugging purposes."""
        if self.driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/{name}_{timestamp}.png"
            try:
                self.driver.save_screenshot(filename)
                self.logger.info(f"Screenshot saved to {filename}")
                return filename
            except Exception as e:
                self.logger.error(f"Failed to save screenshot: {str(e)}")
        return None
    

    def log_page_state(self, context=""):
        """Log the current state of the page for debugging."""
        try:
            self.logger.info(f"--- Current page state ({context}) ---")
            self.logger.info(f"Current URL: {self.driver.current_url}")
            
            # Take and save screenshot
            screenshot_file = self.save_debug_screenshot(f"page_state_{context}")
            
            # Log basic page structure (first 10 elements)
            elements = self.driver.find_elements(By.XPATH, "//*")
            self.logger.info(f"Found {len(elements)} elements on page")
            
            # Log the first 10 elements for debugging
            for i, element in enumerate(elements[:10]):
                try:
                    tag_name = element.tag_name
                    element_id = element.get_attribute("id")
                    element_class = element.get_attribute("class")
                    element_text = element.text[:50] + "..." if len(element.text) > 50 else element.text
                    
                    self.logger.info(f"Element {i+1}: <{tag_name}> id='{element_id}' class='{element_class}' text='{element_text}'")
                except:
                    pass
                    
            self.logger.info("--- End of page state ---")
        except Exception as e:
            self.logger.error(f"Error logging page state: {str(e)}")
        
    def login_to_website(self, url, username, password):
        """Navigate to the URL and log in with provided credentials."""
        try:
            self.logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "form")))
    
            # Locate elements
            username_element = self.driver.find_element(By.NAME, "username")
            password_element = self.driver.find_element(By.NAME, "password")
            submit_button = self.driver.find_element(By.ID, "submit")
    
            # Perform login actions
            username_element.send_keys(username)
            password_element.send_keys(password)
            submit_button.click()
    
            # Wait for post-login state
            WebDriverWait(self.driver, 10).until(EC.url_changes(url))
            self.logger.info("Login successful!")
    
            # Capture page source and screenshot after login
            page_source = self.driver.page_source
            screenshot = self.capture_screenshot()
    
            return True, page_source, screenshot
    
        except TimeoutException:
            self.logger.error("Timeout while waiting for login elements.")
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during login: {str(e)}")
    
        # Return failure indicators on exception
        return False, None, None

    
    def analyze_login_page(self, page_source, screenshot):
        """Use LLM to analyze the login page and identify form elements."""
        prompt = f"""
        Analyze this webpage HTML for the login form elements.
        
        I need precise and accurate CSS selectors that will work with Selenium WebDriver.
        For each element, provide multiple selector options in order of preference (most reliable first).
        
        Please identify:
        1. CSS selectors for the username input field
        2. CSS selectors for the password input field
        3. CSS selectors for the submit/login button
        
        Follow these guidelines for reliable selectors:
        - Prefer selectors using 'name' attributes over 'id' for form fields (e.g., input[name='username'])
        - Prefer specific attributes like 'name', 'id', or 'type' over class names when available
        - For buttons, try [type='submit'] before classes
        - Avoid complex CSS selectors with multiple class names when simpler options exist
        - Provide at least 2 alternative selectors for each element
        
        Return your response as JSON with the following structure:
        {{
            "username_selector": {{
                "primary": "input[name='username']",
                "alternatives": ["#username", "input[type='text']"]
            }},
            "password_selector": {{
                "primary": "input[name='password']",
                "alternatives": ["#password", "input[type='password']"]
            }},
            "submit_selector": {{
                "primary": "button[type='submit']",
                "alternatives": [".login-button", "input[type='submit']"]
            }}
        }}
        
        HTML: {page_source[:15000]}  # Increased limit for better context
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a web testing expert specializing in reliable selector generation. You analyze web pages and provide precise, robust CSS selectors that work with Selenium WebDriver."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            
            # Extract the JSON response
            result = response.choices[0].message.content
            try:
                # Extract JSON from potential text explanation
                json_str = result
                if "```json" in result:
                    json_str = result.split("```json")[1].split("```")[0].strip()
                elif "```" in result:
                    json_str = result.split("```")[1].strip()
                
                selectors = json.loads(json_str)
                # Extract primary selectors but keep alternatives for fallback
                simplified_selectors = {
                    'username_selector': selectors.get('username_selector', {}).get('primary', "input[name='username']"),
                    'password_selector': selectors.get('password_selector', {}).get('primary', "input[name='password']"),
                    'submit_selector': selectors.get('submit_selector', {}).get('primary', "button[type='submit']")
                }
                
                # Store alternatives for potential fallback
                self.alternative_selectors = {
                    'username_alternatives': selectors.get('username_selector', {}).get('alternatives', []),
                    'password_alternatives': selectors.get('password_selector', {}).get('alternatives', []),
                    'submit_alternatives': selectors.get('submit_selector', {}).get('alternatives', [])
                }
                
                return simplified_selectors

                #return selectors

            except json.JSONDecodeError:
                print("Failed to parse JSON response from LLM")
                print(f"Raw response: {result}")
                # Fallback: use reliable common selectors
                return {
                    'username_selector': "input[name='username'], input[type='text']",
                    'password_selector': "input[name='password'], input[type='password']",
                    'submit_selector': "button[type='submit'], input[type='submit']"
                }
                
        except Exception as e:
            print(f"Error analyzing login page: {str(e)}")
            return None
        
    # Add this new method to the WebTestGenerator class
    # After the analyze_login_page method

    def find_element_with_alternatives(self, driver, primary_selector, alternatives):
        """Try to find an element using primary selector, fall back to alternatives if needed."""
        try:
            return WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, primary_selector)))
        except TimeoutException:
            for alt_selector in alternatives:
                try:
                    return WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, alt_selector)))
                except TimeoutException:
                    continue
        raise NoSuchElementException(f"Could not find element with selector '{primary_selector}' or alternatives.")


            
    def verify_login_success(self, page_source, screenshot):
        """Use LLM to determine if login was successful based on the page content."""
        prompt = f"""
        Analyze this webpage content and determine if a user is successfully logged in.
        
        Things to check:
        1. Presence of dashboard elements
        2. Absence of login form
        3. Presence of user-specific information (like username display)
        4. Error messages indicating failed login
        
        Return your response as JSON with the following keys:
        - success: boolean (true if logged in, false otherwise)
        - reason: string (explanation of your determination)
        
        HTML: {page_source[:10000]}  # Limit to avoid token limits
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a web testing expert. Analyze web pages to determine login status."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            try:
                # Extract JSON from potential text explanation
                json_str = result
                if "```json" in result:
                    json_str = result.split("```json")[1].split("```")[0].strip()
                elif "```" in result:
                    json_str = result.split("```")[1].strip()
                
                login_status = json.loads(json_str)
                return login_status
            except json.JSONDecodeError:
                print("Failed to parse JSON response for login verification")
                # Default to failure if parsing fails
                return {"success": False, "reason": "Failed to verify login status"}
                
        except Exception as e:
            print(f"Error verifying login: {str(e)}")
            return {"success": False, "reason": f"Error: {str(e)}"}
    
    
    def generate_test_cases(self, page_source, screenshot):
        """Generate test cases for the current page using LLM."""
        self.logger.info("Generating test cases for the current page...")
        
        # Take a screenshot of the current page for reference
        self.save_debug_screenshot("before_test_case_generation")
        
        prompt = f"""
        Generate comprehensive test cases for this web page, covering ALL major testing types and scenarios.

        Include these testing types (at least 2-3 test cases for each type):

        1. Functional Testing:
        - Positive test cases (testing expected functionality works correctly)
        - Negative test cases (testing error handling and edge cases)
        - Boundary value tests (testing at the limits of acceptable inputs)

        2. UI/UX Testing:
        - Layout and appearance tests
        - Responsiveness tests
        - Navigation tests
        - Accessibility tests

        3. Security Testing:
        - Input validation tests
        - Authentication/Authorization tests
        - Session management tests

        4. Performance Testing:
        - Load time tests
        - Response time tests

        5. Data Validation:
        - Form validation tests
        - Data integrity tests
        - Input sanitization tests
        
        Return your response as JSON with the following structure:
        {{
            "test_cases": [
                {{
                    "id": "TC001",
                    "name": "Verify successful login with valid credentials",
                    "type": "functional_positive",
                    "category": "authentication",
                    "priority": "high",
                    "steps": [
                        "Enter valid username",
                        "Enter valid password",
                        "Click login button"
                    ],
                    "expected_result": "User should be redirected to dashboard",
                    "selectors": {{
                        "target_elements": [
                            {{ "name": "username_field", "selector": "input[name='username']" }},
                            {{ "name": "password_field", "selector": "input[name='password']" }},
                            {{ "name": "login_button", "selector": "button[type=submit]" }}
                        ],
                        "verification_elements": [
                            {{ "name": "dashboard_header", "selector": "h6.oxd-text" }}
                        ]
                    }}
                }}
            ]
        }}
        
        Provide AT LEAST 7-8 test cases covering the different testing types above.
        Be comprehensive and ensure selectors are accurate and specific - prefer attributes like name, id, or type over classes.
        Consider the various UI elements, forms, buttons, and functionality visible on the page.
        Make sure to include a mix of test types and priorities.
        
        HTML: {page_source[:15000]}  # Limit to avoid token limits
        """
        
        try:
            self.logger.info("Sending request to LLM for test case generation...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "YYou are a senior QA automation expert specializing in comprehensive website testing. Your goal is to create exhaustive test suites that cover all aspects of web applications including functionality, UI/UX, security, performance, and data validation. Generate detailed, accurate test cases with precise, reliable CSS selectors."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000
            )
            
            result = response.choices[0].message.content
            self.logger.info("Received response from LLM")
            
            try:
                # Extract JSON from potential text explanation
                json_str = result
                if "```json" in result:
                    json_str = result.split("```json")[1].split("```")[0].strip()
                elif "```" in result:
                    json_str = result.split("```")[1].strip()
                
                test_cases = json.loads(json_str)
                self.logger.info(f"Successfully parsed {len(test_cases.get('test_cases', []))} test cases")
                
                # Log the test cases for debugging
                for tc in test_cases.get('test_cases', []):
                    self.logger.info(f"Generated test case: {tc['id']} - {tc['name']} ({tc['type']})")
                
                return test_cases
            except json.JSONDecodeError:
                self.logger.error("Failed to parse JSON for test cases")
                self.logger.debug(f"Raw response: {result}")
                return {"test_cases": []}
                    
        except Exception as e:
            self.logger.error(f"Error generating test cases: {str(e)}")
            return {"test_cases": []}
    
    # def generate_selenium_script(self, test_case, base_url, username, password):
    #     """Generate Selenium script for a specific test case using LLM."""
    #     prompt = f"""
    #     Generate a Python Selenium script for the following test case:
        
    #     Test Case: {json.dumps(test_case, indent=2)}
    #     Base URL: {base_url}
    #     Username: {username}
    #     Password: {password}
        
    #     Create a complete, executable Python script that:
    #     1. Sets up the Selenium WebDriver (Chrome)
    #     2. Navigates to the URL
    #     3. Performs the login if needed
    #     4. Executes all test steps using proper waits and assertions
    #     5. Handles exceptions appropriately
    #     6. Prints test results
        
    #     Include detailed comments and make the script robust with appropriate waits and error handling.
    #     """
        
    #     try:
    #         response = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=[
    #                 {"role": "system", "content": "You are a Selenium automation expert. Generate complete, executable test scripts."},
    #                 {"role": "user", "content": prompt}
    #             ],
    #             max_tokens=2000
    #         )
            
    #         result = response.choices[0].message.content
    #         # Extract just the Python code if it's wrapped in markdown code blocks
    #         if "```python" in result:
    #             code = result.split("```python")[1].split("```")[0].strip()
    #         elif "```" in result:
    #             code = result.split("```")[1].strip()
    #         else:
    #             code = result.strip()
                
    #         return code
                
    #     except Exception as e:
    #         print(f"Error generating Selenium script: {str(e)}")
    #         return None

    # Update the generate_selenium_script method in the WebTestGenerator class

    def generate_selenium_script(self, test_case, base_url, username, password):
        """Generate Selenium script for a specific test case using LLM."""
        self.logger.info(f"Generating Selenium script for test case {test_case['id']} - {test_case['name']}")
        
        # Enhance the prompt with better guidance for reliable scripts
        prompt = f"""
        Generate a Python Selenium script for the following test case:
        
        Test Case: {json.dumps(test_case, indent=2)}
        Base URL: {base_url}
        Username: {username}
        Password: {password}
        
        Create a complete, executable Python script that:
        1. Sets up the Selenium WebDriver (Chrome)
        2. Navigates to the URL
        3. Performs the login if needed
        4. Executes all test steps using proper waits and assertions
        5. Handles exceptions appropriately
        6. Prints test results
        
        Follow these important guidelines:
        
        - Use WebDriverWait with appropriate wait conditions instead of time.sleep() when possible
        - Use try/except blocks to handle potential errors gracefully
        - Make selectors more robust by using more reliable selectors:
        - Prefer input[name='username'] over input#username for login fields
        - Use exact tag name and attribute for main elements (e.g., "button[type='submit']" is better than ".submit-button")
        - Include detailed comments throughout the script
        - Log important steps and status information
        - Ensure correct element targeting by adding explicit waits for each element interaction
        - Make the outcome clear with explicit pass/fail messages containing the test case ID
        
        For login, specifically use these selectors which are known to work with this application:
        - Username field: input[name='username']
        - Password field: input[name='password'] 
        - Login button: button[type='submit']
        
        Structure your code with clear function definitions and reusable components.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Selenium test automation expert. Generate robust, executable test scripts that handle edge cases and use reliable element selectors and proper waits."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            # Extract just the Python code if it's wrapped in markdown code blocks
            if "```python" in result:
                code = result.split("```python")[1].split("```")[0].strip()
            elif "```" in result:
                code = result.split("```")[1].strip()
            else:
                code = result.strip()
                
            # Post-process the code to make additional improvements
            # code = self.post_process_selenium_script(code, test_case)
                
            return code
                
        except Exception as e:
            self.logger.error(f"Error generating Selenium script: {str(e)}")
            return None
    def submit_form(self):
        """Submit form and handle errors."""
        try:
            submit_button = self.driver.find_element(By.ID, "submit")
            submit_button.click()

            # Wait for response or page change
            WebDriverWait(self.driver, 10).until(EC.url_changes(self.driver.current_url))
            self.logger.info("Form submitted successfully!")
        except TimeoutException:
            self.logger.error("Timeout while waiting for form submission.")
        except NoSuchElementException as e:
            self.logger.error(f"Submit button not found: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during form submission: {str(e)}")


    # Add this new method to post-process the generated scripts
    def post_process_selenium_script(self, code, test_case):
        """Post-process the generated Selenium script to enhance reliability."""
        
        # Add imports if they're missing
        required_imports = [
            "import time",
            "from selenium import webdriver",
            "from selenium.webdriver.common.by import By",
            "from selenium.webdriver.support.ui import WebDriverWait",
            "from selenium.webdriver.support import expected_conditions as EC",
            "from selenium.common.exceptions import TimeoutException, NoSuchElementException"
        ]
        
        # Check if imports are present, add them if not
        for imp in required_imports:
            if imp not in code:
                code = imp + "\n" + code
        
        # Add better error handling
        if "try:" not in code:
            # Wrap main execution in try/except if it's not already there
            lines = code.split("\n")
            main_fn_index = -1
            
            # Find the main function
            for i, line in enumerate(lines):
                if line.startswith("def main():") or "if __name__ == \"__main__\":" in line:
                    main_fn_index = i
                    break
            
            if main_fn_index >= 0:
                # Find where the function body starts
                body_start = main_fn_index + 1
                while body_start < len(lines) and (not lines[body_start].strip() or lines[body_start].startswith(" ") or lines[body_start].startswith("\t")):
                    body_start += 1
                
                # Insert try/except
                lines.insert(body_start, "    try:")
                
                # Find the end of the function to add except block
                i = body_start + 1
                while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                    i += 1
                
                # Add except block
                except_block = [
                    "    except Exception as e:",
                    f"        print(f\"Test case {test_case['id']} FAILED: {{e}}\")",
                    "    finally:",
                    "        # Ensure driver is quit even if test fails",
                    "        if 'driver' in locals():",
                    "            driver.quit()"
                ]
                
                for line in except_block:
                    lines.insert(i, line)
                    i += 1
                
                code = "\n".join(lines)
        
        # Add explicit test result output
        if "print(f\"Test case " not in code:
            # Add explicit test pass message before driver.quit()
            lines = code.split("\n")
            for i, line in enumerate(lines):
                if "driver.quit()" in line:
                    lines.insert(i, f"    print(f\"Test case {test_case['id']} PASSED: Successfully executed {test_case['name']}\")")
                    break
            code = "\n".join(lines)
        
        # Add timeout handling for element interactions
        if "TimeoutException" in code and "except TimeoutException" not in code:
            # Add timeout exception handling if it's imported but not used
            lines = code.split("\n")
            modified_lines = []
            
            for line in lines:
                modified_lines.append(line)
                # Add try/except around element finding operations
                if ".find_element(" in line and "try:" not in line and not line.strip().startswith("except") and not line.strip().startswith("#"):
                    indentation = line[:len(line) - len(line.lstrip())]
                    try_line = f"{indentation}try:"
                    except_line = f"{indentation}except TimeoutException:"
                    print_line = f"{indentation}    print(f\"TimeoutException: Unable to find element\")"
                    
                    # Find where to insert the except block
                    modified_lines[-1] = try_line
                    modified_lines.append(indentation + "    " + line.strip())
                    modified_lines.append(except_line)
                    modified_lines.append(print_line)
            
            code = "\n".join(modified_lines)
        
        return code  

    # Add this new method to the WebTestGenerator class after the post_process_selenium_script method
    def validate_selenium_script(self, script, test_case_id):
        """Validate the generated Selenium script for correctness."""
        self.logger.info(f"Validating Selenium script for test case {test_case_id}")
        
        try:
            # First, basic syntax check using Python's compile
            try:
                compile(script, f"test_script_{test_case_id}.py", 'exec')
                self.logger.info("Basic syntax check passed")
            except SyntaxError as e:
                self.logger.error(f"Syntax error in script: {str(e)}")
                return False, f"Syntax error: {str(e)}"
            
            # Then use LLM to check for logical errors and best practices
            prompt = f"""
            Validate this Selenium test script for correctness and quality. Look for:
            
            1. Indentation errors
            2. Logical errors in the test flow
            3. Proper use of waits and assertions
            4. Proper error handling
            5. Any other issues that might cause the script to fail
            
            Here's the script:
            ```python
            {script}
            ```
            
            Return your response as JSON with the following structure:
            {{
                "is_valid": true/false,
                "issues": [
                    {{
                        "type": "indentation|logical|wait|error_handling|other",
                        "description": "Description of the issue",
                        "line_number": 42,
                        "suggested_fix": "Suggested code to fix the issue"
                    }}
                ],
                "improved_script": "The complete fixed script if there are issues, otherwise null"
            }}
            
            If the script is valid with no issues, just return {{"is_valid": true}} with empty issues list.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Selenium testing expert who can identify and fix issues in test scripts. Focus on indentation errors, logical flows, proper waits, and error handling."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            
            # Parse the response
            try:
                # Extract JSON
                json_str = result
                if "```json" in result:
                    json_str = result.split("```json")[1].split("```")[0].strip()
                elif "```" in result:
                    json_str = result.split("```")[1].strip()
                
                validation_result = json.loads(json_str)
                
                is_valid = validation_result.get("is_valid", False)
                issues = validation_result.get("issues", [])
                
                if is_valid and not issues:
                    self.logger.info("Script validation passed with no issues")
                    return True, None
                else:
                    self.logger.warning(f"Script validation found {len(issues)} issues")
                    for issue in issues:
                        self.logger.warning(f"Issue type: {issue.get('type')}, Line: {issue.get('line_number')}, Description: {issue.get('description')}")
                    
                    # If improved script is provided, use it
                    improved_script = validation_result.get("improved_script")
                    if improved_script:
                        self.logger.info("Using improved script provided by validation")
                        return False, improved_script
                    else:
                        # Return the original script and let the caller decide
                        return False, None
                    
            except json.JSONDecodeError:
                self.logger.error("Failed to parse JSON from validation response")
                self.logger.debug(f"Raw response: {result}")
                return False, None
                
        except Exception as e:
            self.logger.error(f"Error validating script: {str(e)}")
            return False, None  
    
    # def execute_test_script(self, script, test_case_id):
    #     """Execute the generated Selenium script and capture results."""
    #     script_filename = f"test_script_{test_case_id}.py"
        
    #     # Save script to file
    #     with open(script_filename, "w") as f:
    #         f.write(script)
        
    #     print(f"Executing test case {test_case_id}...")
        
    #     try:
    #         # Execute the script and capture output
    #         import subprocess
    #         result = subprocess.run(["python", script_filename], capture_output=True, text=True)
            
    #         # MODIFY THIS PART - Improve status determination logic
    #         status = "FAIL"  # Default to FAIL
            
    #         # Check for error indicators in output
    #         if result.returncode == 0:
    #             # Even if return code is 0, check stdout for failure indicators
    #             error_indicators = ["error", "exception", "fail", "timeout", "unable to", "test failed"]
    #             if not any(indicator in result.stdout.lower() for indicator in error_indicators):
    #                 # No error indicators in stdout, check if there are positive indicators
    #                 success_indicators = ["test passed", "successfully"]
    #                 if any(indicator in result.stdout.lower() for indicator in success_indicators):
    #                     status = "PASS"
            
    #         execution_result = {
    #             "test_case_id": test_case_id,
    #             "exit_code": result.returncode,
    #             "stdout": result.stdout,
    #             "stderr": result.stderr,
    #             "status": status
    #         }
            
    #         return execution_result
                
    #     except Exception as e:
    #         print(f"Error executing test script: {str(e)}")
    #         return {
    #             "test_case_id": test_case_id,
    #             "exit_code": -1,
    #             "stdout": "",
    #             "stderr": str(e),
    #             "status": "ERROR"
    #         }

    # Update the execute_test_script method in the WebTestGenerator class

    def execute_test_script(self, script, test_case_id):
        """Execute the generated Selenium script and capture results."""
        script_filename = f"test_script_{test_case_id}.py"
        
        self.logger.info(f"Executing test script for test case {test_case_id}")
        
        # Save script to file
        with open(script_filename, "w") as f:
            f.write(script)
        
        # Save a copy of the script with timestamp for reference
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"scripts/test_script_{test_case_id}_{timestamp}.py"
        
        # Ensure scripts directory exists
        if not os.path.exists('scripts'):
            os.makedirs('scripts')
            
        with open(archive_filename, "w") as f:
            f.write(script)
        
        try:
            # Execute the script and capture output
            import subprocess
            self.logger.info(f"Running script: {script_filename}")
            
            result = subprocess.run(["python", script_filename], capture_output=True, text=True, timeout=60)
            
            # Analyze output for pass/fail indicators
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            self.logger.info(f"Script execution completed with exit code: {result.returncode}")
            self.logger.info(f"Standard output: {stdout}")
            
            if stderr:
                self.logger.warning(f"Standard error: {stderr}")
            
            # Determine status based on output content
            status = "FAIL"  # Default to FAIL
            
            # Check for explicit pass/fail messages
            if f"Test case {test_case_id} PASSED" in stdout:
                status = "PASS"
            elif f"Test case {test_case_id} FAILED" in stdout:
                status = "FAIL"
            # Otherwise check for error indicators
            elif result.returncode == 0:
                error_indicators = ["error", "exception", "fail", "unable to", "timeout"]
                if not any(indicator in stdout.lower() for indicator in error_indicators) and not stderr:
                    # No error indicators in stdout and no stderr
                    status = "PASS"
            
            execution_result = {
                "test_case_id": test_case_id,
                "exit_code": result.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "status": status,
                "script_file": archive_filename
            }
            
            return execution_result
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Test execution timed out after 60 seconds")
            return {
                "test_case_id": test_case_id,
                "exit_code": -1,
                "stdout": "",
                "stderr": "Test execution timed out after 60 seconds",
                "status": "TIMEOUT",
                "script_file": archive_filename
            }
        except Exception as e:
            self.logger.error(f"Error executing test script: {str(e)}")
            return {
                "test_case_id": test_case_id,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "status": "ERROR",
                "script_file": archive_filename
            }
    
    # def run_workflow(self, url, username, password):
    #     """Run the complete workflow: login, generate test cases, generate and execute scripts."""
    #     print(f"Starting test generation for URL: {url}")
        
    #     # Step 1: Login to website
    #     login_success, page_source, screenshot = self.login_to_website(url, username, password)
        
    #     if not login_success:
    #         print("Unable to proceed: Login failed")
    #         return
        
    #     # Step 2: Generate test cases
    #     print("Generating test cases...")
    #     test_cases_data = self.generate_test_cases(page_source, screenshot)
        
    #     if not test_cases_data or not test_cases_data.get("test_cases"):
    #         print("No test cases generated")
    #         return
        
    #     # Save test cases to file
    #     with open("test_cases.json", "w") as f:
    #         json.dump(test_cases_data, f, indent=2)
        
    #     print(f"Generated {len(test_cases_data['test_cases'])} test cases")
        
    #     # Step 3: For each test case, generate and execute Selenium script
    #     test_results = []
        
    #     for tc in test_cases_data["test_cases"]:
    #         print(f"\nProcessing test case: {tc['id']} - {tc['name']}")
            
    #         # Generate Selenium script
    #         selenium_script = self.generate_selenium_script(tc, url, username, password)
            
    #         if not selenium_script:
    #             print(f"Failed to generate script for test case {tc['id']}")
    #             continue
            
    #         # Save script to file
    #         script_filename = f"selenium_script_{tc['id']}.py"
    #         with open(script_filename, "w") as f:
    #             f.write(selenium_script)
            
    #         print(f"Script generated and saved to {script_filename}")
            
    #         # Execute script
    #         result = self.execute_test_script(selenium_script, tc['id'])
    #         test_results.append(result)
            
    #         print(f"Test case {tc['id']} execution status: {result['status']}")
        
    #     # Save test results to file
    #     with open("test_results.json", "w") as f:
    #         json.dump(test_results, f, indent=2)
        
    #     print("\nTest execution summary:")
    #     passed = sum(1 for r in test_results if r["status"] == "PASS")
    #     failed = sum(1 for r in test_results if r["status"] == "FAIL")
    #     error = sum(1 for r in test_results if r["status"] == "ERROR")
        
    #     print(f"Total test cases: {len(test_results)}")
    #     print(f"Passed: {passed}")
    #     print(f"Failed: {failed}")
    #     print(f"Errors: {error}")
        
    #     # Cleanup
    #     self.driver.quit()

    def run_workflow(self, url, username, password):
        """Run the complete workflow: login, generate test cases, generate and execute scripts."""
        self.logger.info(f"Starting test generation for URL: {url}")
    
        # Create results directory if it doesn't exist
        if not os.path.exists('results'):
            os.makedirs('results')
    
        # Step 1: Login to website
        login_success, page_source, screenshot = self.login_to_website(url, username, password)
    
        if not login_success:
            self.logger.error("Unable to proceed: Login failed")
    
            # Save the page source for debugging (if available)
            if page_source:
                with open("results/failed_login_page.html", "w", encoding="utf-8") as f:
                    f.write(page_source)
            
            return
    
        # Step 2: Generate test cases
        self.logger.info("Generating test cases...")
        test_cases_data = self.generate_test_cases(page_source, screenshot)
    
        if not test_cases_data or not test_cases_data.get("test_cases"):
            self.logger.error("No test cases generated")
            return
    
        # Save test cases to file
        test_cases_file = "results/test_cases.json"
        with open(test_cases_file, "w") as f:
            json.dump(test_cases_data, f, indent=2)
        
        self.logger.info(f"Generated {len(test_cases_data['test_cases'])} test cases, saved to {test_cases_file}")
    
        # Step 3: For each test case, generate and execute Selenium script
        test_results = []
    
        for tc in test_cases_data["test_cases"]:
            self.logger.info(f"\nProcessing test case: {tc['id']} - {tc['name']}")
    
            # Generate Selenium script
            selenium_script = self.generate_selenium_script(tc, url, username, password)
    
            if not selenium_script:
                self.logger.error(f"Failed to generate script for test case {tc['id']}")
                test_results.append({
                    "test_case_id": tc['id'],
                    "exit_code": -1,
                    "stdout": "",
                    "stderr": "Failed to generate script",
                    "status": "ERROR"
                })
                continue
    
            # Execute script
            result = self.execute_test_script(selenium_script, tc['id'])
            test_results.append(result)
            
            self.logger.info(f"Test case {tc['id']} execution status: {result['status']}")
    
        # Save test results to file
        results_file = "results/test_results.json"
        with open(results_file, "w") as f:
            json.dump(test_results, f, indent=2)
    
        # Generate test execution summary
        self.logger.info("\nTest execution summary:")
        passed = sum(1 for r in test_results if r["status"] == "PASS")
        failed = sum(1 for r in test_results if r["status"] == "FAIL")
        error = sum(1 for r in test_results if r["status"] == "ERROR")
        timeout = sum(1 for r in test_results if r["status"] == "TIMEOUT")
    
        summary = {
            "total": len(test_results),
            "passed": passed,
            "failed": failed,
            "error": error,
            "timeout": timeout,
            "pass_rate": f"{(passed / len(test_results) * 100) if test_results else 0:.2f}%"
        }
    
        self.logger.info(f"Total test cases: {summary['total']}")
        self.logger.info(f"Passed: {summary['passed']} ({summary['pass_rate']})")
        self.logger.info(f"Failed: {summary['failed']}")
        self.logger.info(f"Errors: {summary['error']}")
        self.logger.info(f"Timeouts: {summary['timeout']}")
    
        # Save summary to file
        with open("results/summary.json", "w") as f:
            json.dump(summary, f, indent=2)
    
        # Cleanup
        self.driver.quit()
    
        return summary
    


# def main():
#     parser = argparse.ArgumentParser(description="Web Test Generator using LLM")
#     parser.add_argument("--url", required=True, help="URL of the website to test")
#     parser.add_argument("--username", required=True, help="Username for login")
#     parser.add_argument("--password", required=True, help="Password for login")
    
#     args = parser.parse_args()
    
#     test_generator = WebTestGenerator()
#     test_generator.run_workflow(args.url, args.username, args.password)

# if __name__ == "__main__":
#     main()

def main():
    parser = argparse.ArgumentParser(description="Web Test Generator using LLM")
    parser.add_argument("--url", required=True, help="URL of the website to test")
    parser.add_argument("--username", required=True, help="Username for login")
    parser.add_argument("--password", required=True, help="Password for login")
    #parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--output", default="results", help="Output directory for results")
    
    args = parser.parse_args()
    
    try:
        # Check if API key is set
        if not os.getenv("GROQ_API_KEY"):
            print("ERROR: GROQ_API_KEY not found in environment. Please set it in your .env file.")
            return
        
        # Create output directory if specified
        if args.output != "results":
            os.makedirs(args.output, exist_ok=True)
        
        test_generator = WebTestGenerator()
        test_generator.run_workflow(args.url, args.username, args.password)
        
    except KeyboardInterrupt:
        print("\nTest generation interrupted by user.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {str(e)}")
        # Get traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()