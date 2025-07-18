#!/usr/bin/env python3
"""
🎯 ULTIMATE BOSS ARMY - 105+ Agents Deployment
Each agent: 5 attempts with 15s breaks
Between agents: 30s delay
Continue until PIN found for booking ID: 6160911170
"""

import subprocess
import time
import os
import json
import sys
import random
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Configuration
REAL_BOOKING_ID = "6160911170"
WAIT_BETWEEN_AGENTS = 30  # 30 seconds between agents
MAX_AGENTS = 10000  # Maximum number of agents to deploy
PYTHON_PATH = sys.executable

# List of all boss agent scripts
BOSS_AGENTS = [
    "boss_ai_playwright_1A.py", "boss_ai_playwright_1B.py", "boss_ai_playwright_1C.py",
    "boss_ai_playwright_1D.py", "boss_ai_playwright_1E.py", "boss_ai_playwright_1F.py",
    "boss_ai_playwright_1G.py", "boss_ai_playwright_1H.py", "boss_ai_playwright_1I.py",
    "boss_ai_playwright_1J.py", "boss_ai_playwright_1K.py", "boss_ai_playwright_1L.py",
    "boss_ai_playwright_1M.py", "boss_ai_playwright_1N.py", "boss_ai_playwright_1O.py",
    "boss_ai_playwright_1P.py", "boss_ai_playwright_1Q.py", "boss_ai_playwright_1R.py",
    "boss_ai_playwright_1S.py", "boss_ai_playwright_1T.py", "boss_ai_playwright_1U.py",
    "boss_ai_playwright_1V.py", "boss_ai_playwright_1W.py", "boss_ai_playwright_1X.py",
    "boss_ai_playwright_1Y.py", "boss_ai_playwright_1Z.py", "boss_ai_playwright_2A.py",
    "boss_ai_playwright_2B.py", "boss_ai_playwright_2C.py", "boss_ai_playwright_2D.py",
    "boss_ai_playwright_2E.py", "boss_ai_playwright_2F.py", "boss_ai_playwright_2G.py",
    "boss_ai_playwright_2H.py", "boss_ai_playwright_2I.py", "boss_ai_playwright_2J.py",
    "boss_ai_playwright_2K.py", "boss_ai_playwright_2L.py", "boss_ai_playwright_2M.py",
    "boss_ai_playwright_2N.py", "boss_ai_playwright_2O.py", "boss_ai_playwright_2P.py",
    "boss_ai_playwright_2Q.py", "boss_ai_playwright_2R.py", "boss_ai_playwright_2S.py",
    "boss_ai_playwright_2T.py", "boss_ai_playwright_2U.py", "boss_ai_playwright_2V.py",
    "boss_ai_playwright_2W.py", "boss_ai_playwright_2X.py", "boss_ai_playwright_2Y.py",
    "boss_ai_playwright_2Z.py", "boss_ai_playwright_3A.py", "boss_ai_playwright_3B.py",
    "boss_ai_playwright_3C.py", "boss_ai_playwright_3D.py", "boss_ai_playwright_3E.py",
    "boss_ai_playwright_3F.py", "boss_ai_playwright_3G.py", "boss_ai_playwright_3H.py",
    "boss_ai_playwright_3I.py", "boss_ai_playwright_3J.py", "boss_ai_playwright_3K.py",
    "boss_ai_playwright_3L.py", "boss_ai_playwright_3M.py", "boss_ai_playwright_3N.py",
    "boss_ai_playwright_3O.py", "boss_ai_playwright_3P.py", "boss_ai_playwright_3Q.py",
    "boss_ai_playwright_3R.py", "boss_ai_playwright_3S.py", "boss_ai_playwright_3T.py",
    "boss_ai_playwright_3U.py", "boss_ai_playwright_3V.py", "boss_ai_playwright_3W.py",
    "boss_ai_playwright_3X.py", "boss_ai_playwright_3Y.py", "boss_ai_playwright_3Z.py",
    "boss_ai_playwright_A.py", "boss_ai_playwright_B.py", "boss_ai_playwright_C.py",
    "boss_ai_playwright_D.py", "boss_ai_playwright_E.py", "boss_ai_playwright_F.py",
    "boss_ai_playwright_G.py", "boss_ai_playwright_H.py", "boss_ai_playwright_I.py",
    "boss_ai_playwright_J.py", "boss_ai_playwright_K.py", "boss_ai_playwright_L.py",
    "boss_ai_playwright_M.py", "boss_ai_playwright_N.py", "boss_ai_playwright_O.py",
    "boss_ai_playwright_P.py", "boss_ai_playwright_Q.py", "boss_ai_playwright_R.py",
    "boss_ai_playwright_S.py", "boss_ai_playwright_T.py", "boss_ai_playwright_U.py",
    "boss_ai_playwright_V.py", "boss_ai_playwright_W.py", "boss_ai_playwright_X.py",
    "boss_ai_playwright_Y.py", "boss_ai_playwright_Z.py"
]

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
║                🎯 ULTIMATE BOSS ARMY - 105+ AGENTS 🎯                       ║
║                                                                              ║
║  Target Booking ID: {REAL_BOOKING_ID}                                        ║
║  Total Boss Agents: {len(BOSS_AGENTS)} unique agents                         ║
║  Each agent: 5 attempts with 15s breaks                                     ║
║  Between agents: 30s delay                                                  ║
║  Proxy: customer-1proxylabs_atNPR-cc-us@pr.oxylabs.io:7777                 ║
║  Browser: Visible (headless=False)                                          ║
║                                                                              ║
║                     🚀 ULTIMATE ARMY DEPLOYMENT! 🚀                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def display_agent_launch(agent_num, agent_script, total_attempts):
    """Display agent launch message"""
    agent_name = agent_script.replace('.py', '').replace('boss_ai_playwright_', 'BOSS_')
    print(f"\n{Fore.GREEN}🎯 DEPLOYING {agent_name} (Agent #{agent_num:04d}){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Script: {agent_script}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   Total attempts so far: {total_attempts}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}   Mission: Try 5 random PINs, 15s breaks, return home{Style.RESET_ALL}")
    print(f"{Fore.BLUE}   {'='*65}{Style.RESET_ALL}")

def display_victory_summary(winning_pin, agent_script):
    """Display victory summary"""
    agent_name = agent_script.replace('.py', '').replace('boss_ai_playwright_', 'BOSS_')
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🎉 ULTIMATE ARMY VICTORY! 🎉                               ║
║                                                                              ║
║  Target Booking ID: {REAL_BOOKING_ID}                                        ║
║  Winning PIN: {winning_pin}                                                  ║
║  Victorious Agent: {agent_name}                                              ║
║  Victory Script: {agent_script}                                              ║
║  Victory Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}               ║
║                                                                              ║
║                         🏆 MISSION ACCOMPLISHED! 🏆                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)
    
    # Show total army effort
    total_attempts = get_total_attempts()
    print(f"{Fore.CYAN}📊 ULTIMATE ARMY STATISTICS:")
    print(f"Total PIN attempts: {total_attempts}")
    print(f"Success rate: {(1/total_attempts)*100:.4f}%")
    print(f"Army efficiency: Found in {total_attempts} attempts out of 10,000 possible")
    print(f"Proxy used: customer-1proxylabs_atNPR-cc-us@pr.oxylabs.io:7777{Style.RESET_ALL}")

def main():
    """Main ultimate army deployment function"""
    print(f"{Fore.CYAN}🔍 Checking for existing success...{Style.RESET_ALL}")
    
    # Check if PIN already found
    success, winning_pin = check_success()
    if success:
        print(f"{Fore.GREEN}✅ PIN ALREADY FOUND!{Style.RESET_ALL}")
        display_victory_summary(winning_pin, "UNKNOWN")
        return
    
    # Display army banner
    display_army_banner()
    
    # Deploy agents one by one in cycle
    agent_count = 0
    cycle_count = 0
    
    try:
        while agent_count < MAX_AGENTS:
            # Cycle through all boss agents
            for agent_script in BOSS_AGENTS:
                agent_count += 1
                
                # Check if success found before deploying new agent
                success, winning_pin = check_success()
                if success:
                    print(f"{Fore.GREEN}🎉 SUCCESS DETECTED! Stopping army deployment...{Style.RESET_ALL}")
                    display_victory_summary(winning_pin, agent_script)
                    return
                
                # Check if agent script exists
                if not os.path.exists(agent_script):
                    print(f"{Fore.RED}❌ Agent script not found: {agent_script}{Style.RESET_ALL}")
                    continue
                
                # Show agent launch info
                total_attempts = get_total_attempts()
                display_agent_launch(agent_count, agent_script, total_attempts)
                
                # Launch boss agent
                try:
                    print(f"{Fore.YELLOW}🚀 Launching {agent_script}...{Style.RESET_ALL}")
                    
                    # Run the boss agent script
                    result = subprocess.run([PYTHON_PATH, agent_script], 
                                          capture_output=False,
                                          text=True,
                                          timeout=300)  # 5 minute timeout per agent
                    
                    print(f"{Fore.BLUE}🏠 {agent_script} returned home (Exit code: {result.returncode}){Style.RESET_ALL}")
                    
                    # Check if this agent found success
                    success, winning_pin = check_success()
                    if success:
                        print(f"{Fore.GREEN}🎉 VICTORY! {agent_script} found the PIN!{Style.RESET_ALL}")
                        display_victory_summary(winning_pin, agent_script)
                        return
                    
                except subprocess.TimeoutExpired:
                    print(f"{Fore.RED}⏰ {agent_script} timed out{Style.RESET_ALL}")
                    continue
                    
                except Exception as e:
                    print(f"{Fore.RED}❌ Error launching {agent_script}: {e}{Style.RESET_ALL}")
                    continue
                
                # Wait 30 seconds before next agent
                if agent_count < MAX_AGENTS:
                    print(f"{Fore.BLUE}⏱️ Waiting 30 seconds before next agent...{Style.RESET_ALL}")
                    time.sleep(WAIT_BETWEEN_AGENTS)
                
                # Break if max agents reached
                if agent_count >= MAX_AGENTS:
                    break
            
            cycle_count += 1
            print(f"{Fore.MAGENTA}🔄 Completed cycle #{cycle_count} through all {len(BOSS_AGENTS)} agents{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Ultimate army deployment interrupted by user{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Agents deployed: {agent_count}")
        print(f"Cycles completed: {cycle_count}")
        print(f"Total attempts: {get_total_attempts()}{Style.RESET_ALL}")
        return
    
    # Final results
    success, winning_pin = check_success()
    if success:
        display_victory_summary(winning_pin, "FINAL_AGENT")
    else:
        print(f"\n{Fore.RED}💔 Ultimate army deployment complete - PIN not found{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Agents deployed: {agent_count}")
        print(f"Cycles completed: {cycle_count}")
        print(f"Total attempts: {get_total_attempts()}")
        print(f"Consider checking system or extending deployment{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
