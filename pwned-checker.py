import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ###############################################
# Version 2 -> There is a new Version available##
# ###############################################


# Configuration Variables
URL = 'https://haveibeenpwned.com/'
EMAIL_LIST = ['email1@example.com', 'email2@example.com']  # Add more emails as needed
OUTPUT_FILE = 'pwned_results.csv'
LOG_FILE = 'script.log'
HEADLESS = True  # Set to False if you want to see the browser actions
TIMEOUT = 10  # Seconds to wait for elements

# Setup Logging
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

        # Wait for the result to appear
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pwnTitle'))
        )

        # Extract the result text
        pwned_result_element = driver.find_element(By.CLASS_NAME, 'pwnTitle')
        pwned_result_text = pwned_result_element.text.lower()

        if "no pwnage found" in pwned_result_text:
            logging.info(f"Good news for {email} — no pwnage found!")
            return "No pwnage found"
        else:
            logging.info(f"Oh no — {email} has been pwned!")
            return "Pwned"

    except Exception as e:
        logging.error(f"Error processing {email}: {e}")
        return f"Error: {e}"

def save_results(results, filename):
    """Save the results to a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Email', 'Status'])
            for email, status in results.items():
                writer.writerow([email, status])
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to {filename}: {e}")

def main():
    """Main function to execute the email pwnage check."""
    driver = setup_driver(headless=HEADLESS)
    results = {}

    try:
        for email in EMAIL_LIST:
            status = check_email_pwned(driver, email)
            results[email] = status
            # Optional: Add a short delay to avoid overwhelming the server
            # time.sleep(1)
    finally:
        driver.quit()
        logging.info("Browser closed.")

    save_results(results, OUTPUT_FILE)

if __name__ == "__main__":
    main()
