#!/usr/bin/env python3
"""
🤖 CONTINUOUS BOSS AGENT ARMY - Single Try Per Agent
Automatically spawns boss agents one by one until PIN is found
Each agent does exactly 1 attempt with auto form fill
"""

import subprocess
import time
import os
import json
import sys
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Configuration
REAL_BOOKING_ID = "6160911170"
BOSS_SCRIPT = "boss_ai_playwright_1A.py"
WAIT_BETWEEN_AGENTS = 5  # seconds between agents
MAX_AGENTS = 10000  # Maximum number of agents to deploy
PYTHON_PATH = sys.executable

def check_success():
    """Check if PIN has been found by looking for success log"""
    try:
        # Check if any agent found success
        with open("multi_pin_manager_data.json", 'r') as f:
            data = json.load(f)
            if REAL_BOOKING_ID in data and "success_pin" in data[REAL_BOOKING_ID]:
                return True, data[REAL_BOOKING_ID]["success_pin"]
    except:
        pass
    return False, None

def get_total_attempts():
    """Get total number of PIN attempts made"""
    try:
        with open("multi_pin_manager_data.json", 'r') as f:
            data = json.load(f)
            if REAL_BOOKING_ID in data and "used_pins" in data[REAL_BOOKING_ID]:
                return len(data[REAL_BOOKING_ID]["used_pins"])
    except:
        pass
    return 0

def display_army_banner():
    """Display army deployment banner"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                🤖 CONTINUOUS BOSS AGENT ARMY 🤖                             ║
║                                                                              ║
║  Target Booking ID: {REAL_BOOKING_ID}                                        ║
║  Strategy: Single-try continuous deployment                                 ║
║  Agent limit: {MAX_AGENTS} agents                                            ║
║  Each agent: 1 attempt → Auto form fill → Return home                       ║
║  No duplicates: Thread-safe PIN management                                  ║
║  Browser: Visible (headless=False)                                          ║
║                                                                              ║
║                     🚀 BOSS ARMY DEPLOYMENT! 🚀                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def display_agent_launch(agent_num, total_attempts):
    """Display agent launch message"""
    print(f"\n{Fore.GREEN}🤖 DEPLOYING BOSS AGENT #{agent_num:04d}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Total attempts so far: {total_attempts}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   Agent mission: Try 1 random PIN, auto-fill form, return home{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}   Proxy: customer-1proxylabs_atNPR-cc-us@pr.oxylabs.io:7777{Style.RESET_ALL}")
    print(f"{Fore.BLUE}   {'='*60}{Style.RESET_ALL}")

def display_victory_summary(winning_pin):
    """Display victory summary"""
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🎉 BOSS ARMY MISSION ACCOMPLISHED! 🎉                      ║
║                                                                              ║
║  Target Booking ID: {REAL_BOOKING_ID}                                        ║
║  Winning PIN: {winning_pin}                                                  ║
║  Victory achieved by: BOSS AGENT                                            ║
║  Method: Automatic form filling                                             ║
║  Victory Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}               ║
║                                                                              ║
║                         🏆 BOSS ARMY VICTORY! 🏆                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)
    
    # Show total army effort
    total_attempts = get_total_attempts()
    print(f"{Fore.CYAN}📊 BOSS ARMY STATISTICS:")
    print(f"Total PIN attempts: {total_attempts}")
    print(f"Success rate: {(1/total_attempts)*100:.4f}%")
    print(f"Army efficiency: Found in {total_attempts} attempts out of 10,000 possible")
    print(f"Proxy used: customer-1proxylabs_atNPR-cc-us@pr.oxylabs.io:7777{Style.RESET_ALL}")

def main():
    """Main boss army deployment function"""
    print(f"{Fore.CYAN}🔍 Checking for existing success...{Style.RESET_ALL}")
    
    # Check if PIN already found
    success, winning_pin = check_success()
    if success:
        print(f"{Fore.GREEN}✅ PIN ALREADY FOUND!{Style.RESET_ALL}")
        display_victory_summary(winning_pin)
        return
    
    # Display army banner
    display_army_banner()
    
    # Deploy agents one by one
    agent_count = 0
    
    try:
        while agent_count < MAX_AGENTS:
            agent_count += 1
            
            # Check if success found before deploying new agent
            success, winning_pin = check_success()
            if success:
                print(f"{Fore.GREEN}🎉 SUCCESS DETECTED! Stopping army deployment...{Style.RESET_ALL}")
                display_victory_summary(winning_pin)
                break
            
            # Show agent launch info
            total_attempts = get_total_attempts()
            display_agent_launch(agent_count, total_attempts)
            
            # Launch boss agent
            try:
                print(f"{Fore.YELLOW}🚀 Launching boss agent #{agent_count:04d}...{Style.RESET_ALL}")
                
                # Run the boss agent script
                result = subprocess.run([PYTHON_PATH, BOSS_SCRIPT], 
                                      capture_output=False,
                                      text=True,
                                      timeout=120)  # 2 minute timeout per agent
                
                print(f"{Fore.BLUE}🏠 Boss agent #{agent_count:04d} returned home (Exit code: {result.returncode}){Style.RESET_ALL}")
                
                # Check if this agent found success
                success, winning_pin = check_success()
                if success:
                    print(f"{Fore.GREEN}🎉 VICTORY! Boss agent #{agent_count:04d} found the PIN!{Style.RESET_ALL}")
                    display_victory_summary(winning_pin)
                    break
                
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}⏰ Boss agent #{agent_count:04d} timed out{Style.RESET_ALL}")
                continue
                
            except Exception as e:
                print(f"{Fore.RED}❌ Error launching boss agent #{agent_count:04d}: {e}{Style.RESET_ALL}")
                continue
            
            # Wait before next agent
            if agent_count < MAX_AGENTS:
                print(f"{Fore.BLUE}⏱️ Waiting {WAIT_BETWEEN_AGENTS} seconds before next agent...{Style.RESET_ALL}")
                time.sleep(WAIT_BETWEEN_AGENTS)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Boss army deployment interrupted by user{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Agents deployed: {agent_count}")
        print(f"Total attempts: {get_total_attempts()}{Style.RESET_ALL}")
        return
    
    # Final results
    success, winning_pin = check_success()
    if success:
        display_victory_summary(winning_pin)
    else:
        print(f"\n{Fore.RED}💔 Boss army deployment complete - PIN not found{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Agents deployed: {agent_count}")
        print(f"Total attempts: {get_total_attempts()}")
        print(f"Consider increasing MAX_AGENTS or checking system{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
