#!/usr/bin/env python3
"""
🤖 AUTOMATIC PIN HUNTER ARMY - Booking ID: 5727559423
Automatically spawns agents one after another until PIN is found
Each agent does exactly 10 attempts with no duplicates
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
TARGET_BOOKING_ID = "5727559423"
SUCCESS_FILE = f"TARGET_SUCCESS_{TARGET_BOOKING_ID}.json"
GLOBAL_LOG_FILE = f"target_hunt_log_{TARGET_BOOKING_ID}.txt"
HUNTER_SCRIPT = "target_pin_hunter_5727559423.py"
WAIT_BETWEEN_AGENTS = 2  # seconds between agents
MAX_AGENTS = 1000  # Maximum number of agents to deploy
PYTHON_PATH = sys.executable

def check_success():
    """Check if PIN has been found"""
    return os.path.exists(SUCCESS_FILE)

def get_total_attempts():
    """Get total number of PIN attempts made"""
    count = 0
    if os.path.exists(GLOBAL_LOG_FILE):
        try:
            with open(GLOBAL_LOG_FILE, 'r', encoding='utf-8') as f:
                count = sum(1 for line in f if line.strip())
        except:
            pass
    return count

def display_army_banner():
    """Display army deployment banner"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎯 AUTOMATIC PIN HUNTER ARMY 🎯                          ║
║                                                                              ║
║  Target Booking ID: {TARGET_BOOKING_ID}                                      ║
║  Strategy: Continuous agent deployment                                      ║
║  Agent limit: {MAX_AGENTS} agents                                            ║
║  Each agent: 10 attempts → Return home                                      ║
║  No duplicates: Thread-safe PIN management                                  ║
║                                                                              ║
║                     🚀 ARMY DEPLOYMENT STARTING! 🚀                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def display_agent_launch(agent_num, total_attempts):
    """Display agent launch message"""
    print(f"\n{Fore.GREEN}🤖 DEPLOYING AGENT #{agent_num:03d}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Total attempts so far: {total_attempts}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   Agent mission: Try 10 random PINs, return home if failed{Style.RESET_ALL}")
    print(f"{Fore.BLUE}   {'='*60}{Style.RESET_ALL}")

def display_victory_summary():
    """Display victory summary"""
    try:
        with open(SUCCESS_FILE, 'r') as f:
            success_data = json.load(f)
        
        banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      🎉 ARMY MISSION ACCOMPLISHED! 🎉                       ║
║                                                                              ║
║  Target Booking ID: {TARGET_BOOKING_ID}                                      ║
║  Winning PIN: {success_data['success_pin']}                                  ║
║  Victorious Agent: {success_data['agent']}                                   ║
║  Agent's Attempt: {success_data['attempt_number']}/10                        ║
║  Victory Time: {success_data['timestamp']}                                   ║
║                                                                              ║
║                         🏆 MISSION COMPLETE! 🏆                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        
        # Show total army effort
        total_attempts = get_total_attempts()
        print(f"{Fore.CYAN}📊 ARMY STATISTICS:")
        print(f"Total PIN attempts: {total_attempts}")
        print(f"Success rate: {(1/total_attempts)*100:.4f}%")
        print(f"Army efficiency: Found in {total_attempts} attempts out of 10,000 possible{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading success file: {e}{Style.RESET_ALL}")

def main():
    """Main army deployment function"""
    print(f"{Fore.CYAN}🔍 Checking for existing success...{Style.RESET_ALL}")
    
    # Check if PIN already found
    if check_success():
        print(f"{Fore.GREEN}✅ PIN ALREADY FOUND!{Style.RESET_ALL}")
        display_victory_summary()
        return
    
    # Display army banner
    display_army_banner()
    
    # Deploy agents one by one
    agent_count = 0
    
    try:
        while agent_count < MAX_AGENTS:
            agent_count += 1
            
            # Check if success found before deploying new agent
            if check_success():
                print(f"{Fore.GREEN}🎉 SUCCESS DETECTED! Stopping army deployment...{Style.RESET_ALL}")
                break
            
            # Show agent launch info
            total_attempts = get_total_attempts()
            display_agent_launch(agent_count, total_attempts)
            
            # Launch agent
            try:
                print(f"{Fore.YELLOW}🚀 Launching agent #{agent_count:03d}...{Style.RESET_ALL}")
                
                # Run the hunter script
                result = subprocess.run([PYTHON_PATH, HUNTER_SCRIPT], 
                                      capture_output=False,
                                      text=True,
                                      timeout=300)  # 5 minute timeout per agent
                
                print(f"{Fore.BLUE}🏠 Agent #{agent_count:03d} returned home (Exit code: {result.returncode}){Style.RESET_ALL}")
                
                # Check if this agent found success
                if check_success():
                    print(f"{Fore.GREEN}🎉 VICTORY! Agent #{agent_count:03d} found the PIN!{Style.RESET_ALL}")
                    break
                
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}⏰ Agent #{agent_count:03d} timed out{Style.RESET_ALL}")
                continue
                
            except Exception as e:
                print(f"{Fore.RED}❌ Error launching agent #{agent_count:03d}: {e}{Style.RESET_ALL}")
                continue
            
            # Wait before next agent
            if agent_count < MAX_AGENTS:
                print(f"{Fore.BLUE}⏱️ Waiting {WAIT_BETWEEN_AGENTS} seconds before next agent...{Style.RESET_ALL}")
                time.sleep(WAIT_BETWEEN_AGENTS)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Army deployment interrupted by user{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Agents deployed: {agent_count}")
        print(f"Total attempts: {get_total_attempts()}{Style.RESET_ALL}")
        return
    
    # Final results
    if check_success():
        display_victory_summary()
    else:
        print(f"\n{Fore.RED}💔 Army deployment complete - PIN not found{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Agents deployed: {agent_count}")
        print(f"Total attempts: {get_total_attempts()}")
        print(f"Consider increasing MAX_AGENTS or checking system{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
