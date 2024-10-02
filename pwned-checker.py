import csv
import logging
import re
import time  # Adding explicit time wait as a backup
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
EMAIL_LIST = ['email1@example.com', 'email2@example.com']  # Add more emails as needed
OUTPUT_FILE = 'pwned_results.csv'
LOG_FILE = 'script.log'
HEADLESS = True  # Set to False if you want to see the browser actions
TIMEOUT = 20  # Seconds to wait for elements (increased to 20s)
WAIT_TIME = 5  # Extra wait time before extracting information

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

def extract_pwned_info(text):
    """Extract pwned information (breaches and pastes) from the pwnCount text."""
    try:
        # Extract 'Pwned in X data breaches'
        breaches_match = re.search(r'Pwned in (\d+)', text)
        # Extract 'and found Y pastes'
        pastes_match = re.search(r'found (\d+)', text)

        # Default to 0 if no match found
        breaches = breaches_match.group(1) if breaches_match else '0'
        pastes = pastes_match.group(1) if pastes_match else '0'

        # Return the full phrases to match your requirements
        breaches_text = f"Pwned in {breaches} data breaches"
        pastes_text = f"and found {pastes} paste(s)"

        return breaches_text, pastes_text
    except Exception as e:
        logging.error(f"Error extracting pwned information: {e}")
        return "Error extracting breaches", "Error extracting pastes"

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
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pwnTitle'))
        )

        # Explicit wait for pwnCount element and additional wait time for data to load
        logging.info(f"Waiting for pwnCount element for {WAIT_TIME} seconds before extraction.")
        time.sleep(WAIT_TIME)  # Adding explicit sleep

        try:
            # Check if the pwnCount element exists on the page
            if len(driver.find_elements(By.ID, 'pwnCount')) > 0:
                # Locate the pwnCount element
                pwn_count_element = driver.find_element(By.ID, 'pwnCount')
                pwn_count_text = pwn_count_element.text.strip()

                # Log the pwnCount text for verification
                logging.info(f"pwnCount text for {email}: {pwn_count_text}")
                print(f"pwnCount text for {email}: {pwn_count_text}")

                # Extract "Pwned in X data breaches" and "found Y pastes"
                breaches_text, pastes_text = extract_pwned_info(pwn_count_text)

                logging.info(f"Oh no — {email} has been pwned!")
                logging.info(f"{breaches_text}, {pastes_text}")

                return {"email": email, "status": "Pwned", "breaches": breaches_text, "pastes": pastes_text}
            else:
                logging.warning(f"pwnCount element not found for {email}.")
                return {"email": email, "status": "Pwned", "breaches": "0", "pastes": "0"}

        except TimeoutException:
            logging.error(f"Timeout occurred while trying to locate pwnCount for {email}")
            return {"email": email, "status": "Pwned", "breaches": "0", "pastes": "0"}

    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error processing {email}: {e}")
        return {"email": email, "status": f"Error: {e}", "breaches": "0", "pastes": "0"}

def save_results(results, filename):
    """Save the results to a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Email', 'Status', 'Breaches', 'Pastes'])
            for result in results:
                writer.writerow([result['email'], result['status'], result['breaches'], result['pastes']])
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to {filename}: {e}")

def main():
    """Main function to execute the email pwnage check."""
    driver = setup_driver(headless=HEADLESS)
    results = []

    try:
        for email in EMAIL_LIST:
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
