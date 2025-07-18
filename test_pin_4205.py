from playwright.sync_api import sync_playwright
import os
import time

# Test PIN 4205 with the exact same logic as the original agent
CONFIRMATION = "6339614781"
PIN = "4205"
HEADLESS = True

# --- Proxy configuration ---
PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-Oxylab_WFqvh",
    "password": "Oxylab_WFqvh1"
}

print(f"Testing PIN {PIN} for booking {CONFIRMATION}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=HEADLESS, proxy=PROXY_CONFIG)
    page = browser.new_page()

    try:
        print("Going to booking.com PIN auth page...")
        page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load")

        # Wait for the confirmation number input using placeholder
        page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
        page.fill('input[placeholder="e.g. 1234567890"]', CONFIRMATION)
        page.fill('input[placeholder="e.g. 1234"]', PIN)

        # Wait for the Continue button to be visible, then click
        try:
            page.wait_for_selector('button:has-text("Continue")', timeout=5000)
            page.click('button:has-text("Continue")')
        except Exception:
            page.wait_for_selector('button[type="submit"]', timeout=5000)
            page.click('button[type="submit"]')

        # Now wait for either result: success or error banner
        page.wait_for_function(
            """
            () => {
                return location.href.includes('unique_order_id') ||
                       document.querySelector('.bui-alert--error') !== null
            }
            """,
            timeout=45000  # only if nothing happens at all in 45s
        )

        current_url = page.url
        print(f"Final URL: {current_url}")
        
        if "unique_order_id=" in current_url:
            print(f"✅ SUCCESS! PIN {PIN} works for booking {CONFIRMATION}")
            page.screenshot(path=f"screenshots/test_{CONFIRMATION}_{PIN}_success.png")
            result = "SUCCESS"
        elif page.query_selector('.bui-alert--error'):
            print(f"❌ FAILURE! PIN {PIN} is incorrect")
            page.screenshot(path=f"screenshots/test_{CONFIRMATION}_{PIN}_fail.png")
            result = "FAILURE"
        else:
            print(f"❓ UNKNOWN result for PIN {PIN}")
            page.screenshot(path=f"screenshots/test_{CONFIRMATION}_{PIN}_unknown.png")
            result = "UNKNOWN"

        # Also check page content for more details
        page_content = page.content()
        print(f"Page contains 'unique_order_id': {'unique_order_id' in page_content}")
        print(f"Page contains error alert: {page.query_selector('.bui-alert--error') is not None}")
        
        browser.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        page.screenshot(path=f"screenshots/test_{CONFIRMATION}_{PIN}_exception.png")
        result = "EXCEPTION"
        browser.close()

print(f"Final result: {result}")
