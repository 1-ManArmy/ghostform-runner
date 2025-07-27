from playwright.sync_api import sync_playwright
import time

# Test the EXACT known success combination
BOOKING_ID = "5727559423"
TEST_PIN = "2390"  # Known working PIN from agent-log.txt

print(f"🧪 TESTING CONFIRMED SUCCESS: Booking {BOOKING_ID} with PIN {TEST_PIN}")

with sync_playwright() as p:
    proxy_config = {
        "server": "https://pr.oxylabs.io:7777",
        "username": "customer-oxy1p_hnzsA",
        "password": "oxy1p_hnzsA1"
    }
    
    browser = p.chromium.launch(headless=False, proxy=proxy_config)
    page = browser.new_page()
    
    print("🌐 Opening booking.com...")
    page.goto("https://secure.booking.com/help/confirmation_pin_auth")
    page.wait_for_load_state("networkidle")
    
    print(f"📝 Filling booking ID: {BOOKING_ID}")
    page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
    
    print(f"🔐 Filling PIN: {TEST_PIN}")
    page.fill('input[placeholder="e.g. 1234"]', TEST_PIN)
    
    print("✅ Clicking Continue...")
    page.click('button:has-text("Continue")')
    
    time.sleep(5)
    
    current_url = page.url
    print(f"🔍 Result URL: {current_url}")
    
    if "unique_order_id" in current_url:
        print("🎉 SUCCESS CONFIRMED!")
    elif "help/confirmation_pin_auth" in current_url:
        print("❌ Back to help page - this combination no longer works")
    else:
        print(f"❓ Unknown result: {current_url}")
    
    page.screenshot(path="test_known_success.png")
    input("Press Enter to close browser...")
    browser.close()
