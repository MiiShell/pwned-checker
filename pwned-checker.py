from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Paths
input_file_path = 'input/emails.txt'  # Input email list file
output_file_path = 'output/pwned_results.txt'  # Output results file
error_log_file_path = 'output/errors.log'  # Error log file

# Website URL
website_url = 'https://haveibeenpwned.com/'

# Delay times
DELAY_PAGE_LOAD = 2  # Time to wait for the page to load
DELAY_RESULT_LOAD = 5  # Time to wait for the result to appear

def setup_driver():
    """Setup the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)  # Ensure the path to ChromeDriver is set if needed
    return driver

def check_email_pwned(driver, email):
    """Check if the email is pwned on the website."""
    driver.get(website_url)
    time.sleep(DELAY_PAGE_LOAD)  # Wait for the page to load

    # Find the email input field and the "pwned?" button
    email_input = driver.find_element(By.ID, 'Account')
    email_input.clear()
    email_input.send_keys(email)
    
    # Submit the form by clicking the button
    search_button = driver.find_element(By.ID, 'searchPwnage')
    search_button.click()
    
    # Wait for the result to load
    time.sleep(DELAY_RESULT_LOAD)
    
    # Get result
    try:
        pwn_title = driver.find_element(By.CLASS_NAME, 'pwnTitle').text
        if "Good news" in pwn_title:
            return "No pwnage found"
        elif "Oh no" in pwn_title:
            breach_info = driver.find_element(By.ID, 'pwnCount').text
            return f"Pwned! {breach_info}"
        else:
            return "Unexpected result"
    except Exception as e:
        raise Exception(f"Error: Unable to locate result for {email}. Details: {str(e)}")

def read_emails(file_path):
    """Read emails from the input file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def save_results(file_path, results):
    """Save the results to the output file."""
    with open(file_path, 'w') as file:
        for email, result in results.items():
            file.write(f"{email}: {result}\n")

def log_error(file_path, error_message):
    """Log errors to the error log file."""
    with open(file_path, 'a') as error_log:
        error_log.write(f"{error_message}\n")

def main():
    """Main function to run the email pwned checker."""
    if not os.path.exists(input_file_path):
        print(f"Input file not found: {input_file_path}")
        return
    
    emails = read_emails(input_file_path)
    if not emails:
        print("No emails found in the input file.")
        return
    
    # Set up WebDriver
    driver = setup_driver()
    
    # Store results
    results = {}
    for email in emails:
        print(f"Checking: {email}")
        try:
            result = check_email_pwned(driver, email)
            print(f"Result for {email}: {result}")
            results[email] = result
        except Exception as e:
            error_message = f"Error for {email}: {str(e)}"
            print(error_message)
            log_error(error_log_file_path, error_message)
            results[email] = "Error occurred, check error log"
        time.sleep(1)  # Add a short delay between checks

    # Close WebDriver
    driver.quit()
    
    # Save results to output file
    save_results(output_file_path, results)
    print(f"Results saved to: {output_file_path}")

if __name__ == "__main__":
    main()
