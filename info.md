# ##############################
# author: MiiShell
# created: 02.10.2024
# modified: 02.10.2024
# ##############################

## Version 3.1 - 02.10.2024

### Key Changes:


fix output









## Version 3 - 02.10.2024

### Key Changes:



following


## Version 2 - 02.10.2024

### Key Changes:

#### Explicit Wait:

Used WebDriverWait with expected_conditions to wait for elements to be available instead of fixed time.sleep(). This is more efficient and reduces unnecessary delays.
Example:

'''python
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'Account')))
'''


#### Headless Mode:

Added Chrome options to run in headless mode for performance improvements, especially in automated environments like CI/CD pipelines.
Example:

'''python
chrome_options = Options()
chrome_options.add_argument("--headless")
'''


#### Logging:

Replaced print() statements with logging. Logging allows you to easily control the verbosity of the output and store logs for future analysis.

#### Example:

'''python
logging.info("Opened the Have I Been Pwned website.")
'''


#### Specific Exception Handling:

Used more specific exceptions (WebDriverException, NoSuchElementException, etc.) instead of a generic Exception. This allows for better error identification and debugging.
Graceful Browser Closing:

The finally block ensures that the browser is properly closed even if an error occurs during execution, preventing resource leaks.
By improving the code with these features, you ensure more robust, efficient, and production-friendly automation that can handle errors and run faster.