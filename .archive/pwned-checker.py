from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

# ###############################################
# Version 1 -> There is a new Version available##
# ###############################################


# List of emails to check
email_list = ['email1@example.com', 'email2@example.com']  # Add more emails as needed

# Path to your chromedriver
driver_path = '/path/to/chromedriver'  # Adjust path accordingly
service = Service(driver_path)

# Create a new instance of Chrome browser
driver = webdriver.Chrome(service=service)

# Open Have I Been Pwned website
driver.get('https://haveibeenpwned.com/')

# Wait for the page to fully load
time.sleep(3)

# Iterate over each email in the list
for email in email_list:
    try:
        # Locate the email input field
        email_input = driver.find_element(By.ID, 'Account')

        # Enter the email into the input field
        email_input.clear()
        email_input.send_keys(email)

        # Locate and click the 'pwned?' button
        search_button = driver.find_element(By.ID, 'searchPwnage')
        search_button.click()

        # Wait for the result to appear
        time.sleep(3)

        # Check the result by looking for pwnTitle element
        pwned_result = driver.find_element(By.CLASS_NAME, 'pwnTitle').text

        if "no pwnage found" in pwned_result.lower():
            print(f"Good news for {email} — no pwnage found!")
        else:
            print(f"Oh no — {email} has been pwned!")

        # Wait before processing the next email
        time.sleep(2)

    except Exception as e:
        print(f"Error processing {email}: {e}")

# Close the browser when done
driver.quit()
