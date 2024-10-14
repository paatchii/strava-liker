from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CHROMIUM_BIN = os.getenv("CHROMIUM_BIN") 
CHROMEDRIVER_BIN = os.getenv("CHROMEDRIVER_BIN")

options = Options()
options.add_argument("--start-maximized")
options.binary_location = CHROMIUM_BIN
service = Service(CHROMEDRIVER_BIN)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.strava.com/login")

time.sleep(2)

# Log into Strava
username = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'password')
username.send_keys(EMAIL)  # Replace with your email
password.send_keys(PASSWORD)  # Replace with your password

login_button = driver.find_element(By.ID, 'login-button')
login_button.click()

time.sleep(5)

driver.get("https://www.strava.com/dashboard?num_entries=100")

time.sleep(10)

while True:
    try:
        # Find all buttons with the unfilled kudos icon (not liked yet)
        unliked_buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-testid='kudos_button'] svg[data-testid='unfilled_kudos']")
        # Click each unliked button
        for button in unliked_buttons:
            button.click()
            time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    except Exception as e:
        print(f"Error: {e}")
        break

driver.quit()