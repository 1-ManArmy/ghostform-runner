#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DEBUG AGENT - Find the Detection Issue
Let's see exactly what's happening on the page
"""

from playwright.sync_api import sync_playwright
import time

# Agent Configuration
AGENT_ID = "DEBUG"
BOOKING_ID = "5871858498"  # Same as agent_001A
TEST_PIN = "2847"  # Test just one PIN

print(f"🔍 DEBUG AGENT STARTING...")
print(f"🎯 Target: {BOOKING_ID}")
print(f"🔑 Test PIN: {TEST_PIN}")

with sync_playwright() as p:
    # PROXY CONFIGURATION
    proxy_config = {
        "server": "https://pr.oxylabs.io:7777",
        "username": "customer-oxy1p_hnzsA",
        "password": "oxy1p_hnzsA1"
    }
    
    browser = p.chromium.launch(
        headless=False,
        proxy=proxy_config
    )
    page = browser.new_page()

    print("🌐 Opening booking.com...")
    page.goto("https://secure.booking.com/help/confirmation_pin_auth")
    page.wait_for_load_state("networkidle")
    print("✅ Page loaded!")

    print("📝 Filling booking ID and PIN...")
    page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
    page.fill('input[placeholder="e.g. 1234"]', TEST_PIN)
    
    print("🔍 Clicking Continue...")
    page.click('button:has-text("Continue")')
    
    # Wait a bit for response
    print("⏳ Waiting for response...")
    time.sleep(5)
    
    # Debug: Check everything on the page
    current_url = page.url
    print(f"🔍 Current URL: {current_url}")
    
    # Check for error elements
    print("\n🔍 DEBUGGING PAGE ELEMENTS:")
    
    # Check if error banner exists
    error_banner = page.locator("div.bui-alert__content")
    if error_banner.is_visible():
        error_text = error_banner.text_content()
        print(f"❌ Error banner found: '{error_text}'")
    else:
        print("ℹ️ No error banner visible")
    
    # Check for other error indicators
    error_elements = page.locator('.bui-alert--error')
    if error_elements.is_visible():
        print("❌ Error alert found")
    else:
        print("ℹ️ No error alert found")
    
    # Check page title
    title = page.title()
    print(f"📄 Page title: {title}")
    
    # Check if page contains specific text
    page_content = page.content()
    if "We couldn't find a booking" in page_content:
        print("❌ 'We couldn't find a booking' text found in page")
    elif "PIN is incorrect" in page_content:
        print("❌ 'PIN is incorrect' text found in page")
    elif "confirmed" in page_content.lower():
        print("✅ 'confirmed' text found in page")
    elif "success" in page_content.lower():
        print("✅ 'success' text found in page")
    else:
        print("ℹ️ No clear success/failure text found")
    
    # Check for any alerts or messages
    all_alerts = page.locator('[role="alert"]')
    alert_count = all_alerts.count()
    print(f"🚨 Found {alert_count} alert elements")
    
    if alert_count > 0:
        for i in range(alert_count):
            alert_text = all_alerts.nth(i).text_content()
            print(f"🚨 Alert {i+1}: '{alert_text}'")
    
    # Take screenshot for analysis
    page.screenshot(path=f"DEBUG_{BOOKING_ID}_{TEST_PIN}_analysis.png")
    print(f"📸 Screenshot saved: DEBUG_{BOOKING_ID}_{TEST_PIN}_analysis.png")
    
    # Wait to see the page
    print("\n⏸️ Pausing for 10 seconds to analyze page...")
    time.sleep(10)
    
    browser.close()
    print("🔍 Debug complete!")
