import csv
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ###############################################
# Configuration
# ###############################################

# File paths
date_str = datetime.now().strftime('%Y-%m-%d')
input_file_path = f'input/emails.txt'
output_file_path = f'output/pwned_results_{date_str}.csv'
error_log_file_path = f'output/errors_{date_str}.log'

# Website URL
URL = 'https://haveibeenpwned.com/'

# Settings
HEADLESS = True  # Set to False if you want to see the browser actions
TIMEOUT = 10  # Seconds to wait for elements

# Setup Logging
logging.basicConfig(
    filename=error_log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_driver(headless=True):
    """Setup Chrome WebDriver with optional headless mode."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    # Initialize WebDriver using webdriver-manager for automatic driver management
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def check_email_pwned(driver, email):
    """Check if the provided email has been pwned."""
    try:
        driver.get(URL)

        wait = WebDriverWait(driver, TIMEOUT)

        # Wait for the email input field to be present
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, 'Account'))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Locate and click the 'pwned?' button
        search_button = driver.find_element(By.ID, 'searchPwnage')
        search_button.click()

        # Wait for the result to appear
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pwnTitle'))
        )

        # Extract the result text
        pwned_result_element = driver.find_element(By.CLASS_NAME, 'pwnTitle')
        pwned_result_text = pwned_result_element.text

        if "no pwnage found" in pwned_result_text.lower():
            print(f"-----------------------------\ncheck email: {email}\nGood news — no pwnage found!\n-----------------------------")
            return {"email": email, "status": "Good news — no pwnage found"}
        else:
            print(f"-----------------------------\ncheck email: {email}\nOh no — pwned!\n-----------------------------")
            return {"email": email, "status": "Oh no — pwned!"}

    except Exception as e:
        logging.error(f"Error processing {email}: {e}")
        print(f"-----------------------------\ncheck email: {email}\nError processing this email.\n-----------------------------")
        return {"email": email, "status": f"Error: {e}"}

def read_emails(file_path):
    """Read emails from the input file."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return []

def save_results(results, filename):
    """Save the results to a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Email', 'Status'])
            for result in results:
                writer.writerow([result['email'], result['status']])
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to {filename}: {e}")

def main():
    """Main function to execute the email pwnage check."""
    emails = read_emails(input_file_path)
    if not emails:
        logging.error("No emails to process.")
        return

    driver = setup_driver(headless=HEADLESS)
    results = []
    good_news_count = 0
    pwned_count = 0

    try:
        for email in emails:
            result = check_email_pwned(driver, email)
            results.append(result)
            if "Good news" in result["status"]:
                good_news_count += 1
            elif "Oh no" in result["status"]:
                pwned_count += 1
            # Optional: Add a short delay to avoid overwhelming the server
            # time.sleep(1)
    finally:
        driver.quit()

    # Save results to output CSV
    save_results(results, output_file_path)

    # Print the summary
    print("-----------------------------")
    print("Result:")
    print("-----------------------------")
    print(f"{good_news_count} Good news — no pwnage found")
    print(f"{pwned_count} Oh no — pwned!")
    print("-----------------------------")
    print("------------ END ------------")

if __name__ == "__main__":
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    main()
