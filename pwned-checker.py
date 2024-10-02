import csv
import logging
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configuration Variables
URL = 'https://haveibeenpwned.com/'
HEADLESS = True  # Set to False if you want to see the browser actions
TIMEOUT = 20  # Seconds to wait for elements
WAIT_TIME = 5  # Extra wait time before extracting information

# Input and Output directories
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

# Input file containing emails
INPUT_FILE = f'{INPUT_FOLDER}/emails.txt'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Filename based on the current date
current_date = datetime.now().strftime("%Y-%m-%d")
OUTPUT_FILE = f'{OUTPUT_FOLDER}/pwned_results_{current_date}.csv'

# Setup Logging
LOG_FILE = 'script.log'
logging.basicConfig(
    filename=LOG_FILE,
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
        logging.info(f"Navigated to {URL}")

        wait = WebDriverWait(driver, TIMEOUT)

        # Wait for the email input field to be present
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, 'Account'))
        )
        email_input.clear()
        email_input.send_keys(email)
        logging.info(f"Entered email: {email}")

        # Locate and click the 'pwned?' button
        search_button = driver.find_element(By.ID, 'searchPwnage')
        search_button.click()
        logging.info(f"Clicked the 'pwned?' button for {email}")

        # Wait for the pwned title to appear
        pwned_title = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pwnTitle'))
        )

        # Wait for the result to load
        logging.info(f"Waiting {WAIT_TIME} seconds for the page to load before extraction.")
        time.sleep(WAIT_TIME)

        # Check if pwned
        pwned_result_text = pwned_title.text.strip()

        # Determine if email is pwned or not
        if "no pwnage found" in pwned_result_text.lower():
            logging.info(f"Good news for {email} — no pwnage found!")
            return {"email": email, "status": "Good news — no pwnage found!", "date": current_date}
        else:
            logging.info(f"Oh no — {email} has been pwned!")
            return {"email": email, "status": "Pwned", "date": current_date}

    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error processing {email}: {e}")
        return {"email": email, "status": f"Error: {e}", "date": current_date}

def read_emails_from_file(input_file):
    """Read emails from a text file where each line is an email address."""
    emails = []
    try:
        with open(input_file, 'r') as file:
            emails = [line.strip() for line in file.readlines() if line.strip()]
        logging.info(f"Successfully read {len(emails)} email(s) from {input_file}.")
    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
    return emails

def save_results(results, filename):
    """Save the results to a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Email', 'Status', 'Date'])
            for result in results:
                writer.writerow([result['email'], result['status'], result['date']])
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to {filename}: {e}")

def main():
    """Main function to execute the email pwnage check."""
    # Read emails from input file
    emails = read_emails_from_file(INPUT_FILE)

    if not emails:
        logging.error(f"No emails to process. Please check the input file at {INPUT_FILE}.")
        return

    driver = setup_driver(headless=HEADLESS)
    results = []

    try:
        for email in emails:
            result = check_email_pwned(driver, email)
            results.append(result)
            # Optional: Add a short delay to avoid overwhelming the server
            # time.sleep(1)
    finally:
        driver.quit()
        logging.info("Browser closed.")

    save_results(results, OUTPUT_FILE)

if __name__ == "__main__":
    main()
