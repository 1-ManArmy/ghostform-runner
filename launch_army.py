#!/usr/bin/env python3
"""
🚀 AGENT ARMY LAUNCHER - Deploy All 106 Agents
Launches all independent agents simultaneously for maximum efficiency
"""

import subprocess
import os
import time
import sys
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Configuration
BOOKING_ID = "5724349472"
PYTHON_PATH = sys.executable
BASE_DIR = Path(".")
MAX_AGENTS = 106

def display_army_banner():
    """Display the army deployment banner"""
    banner = f"""
{Fore.RED}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🚀 INDEPENDENT AGENT ARMY DEPLOY 🚀                      ║
║                                                                              ║
║  Target Booking ID: {BOOKING_ID}                                             ║
║  Strategy: 106 INDEPENDENT AGENTS SIMULTANEOUS                              ║
║  Each agent: Own browser + Own proxy + Own PIN                              ║
║  Expected result: ONE AGENT WILL FIND SUCCESS!                              ║
║                                                                              ║
║                      🔥 DEPLOYING ARMY NOW! 🔥                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def launch_single_agent(agent_num):
    """Launch a single agent"""
    agent_dir = BASE_DIR / f"agent_{agent_num:03d}"
    main_py_path = agent_dir / "main.py"
    
    if not main_py_path.exists():
        print(f"{Fore.RED}❌ Agent #{agent_num:03d}: main.py not found{Style.RESET_ALL}")
        return None
    
    try:
        # Change to agent directory and run main.py
        process = subprocess.Popen(
            [PYTHON_PATH, "main.py"],
            cwd=agent_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"{Fore.GREEN}🚀 Agent #{agent_num:03d}: Launched successfully{Style.RESET_ALL}")
        return process
        
    except Exception as e:
        print(f"{Fore.RED}❌ Agent #{agent_num:03d}: Launch failed - {e}{Style.RESET_ALL}")
        return None

def monitor_agents(processes):
    """Monitor all agents and check for success"""
    print(f"\n{Fore.CYAN}📊 Monitoring {len(processes)} agents...{Style.RESET_ALL}")
    
    completed = 0
    success_found = False
    winning_agent = None
    
    while completed < len(processes) and not success_found:
        # Check if SUCCESS_FOUND.txt exists
        success_file = BASE_DIR / "SUCCESS_FOUND.txt"
        if success_file.exists():
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 SUCCESS DETECTED!{Style.RESET_ALL}")
            try:
                with open(success_file, "r") as f:
                    success_data = f.read().strip()
                    print(f"{Fore.GREEN}📋 Success Details: {success_data}{Style.RESET_ALL}")
            except:
                pass
            success_found = True
            break
        
        # Check completed agents
        for i, (agent_num, process) in enumerate(processes):
            if process and process.poll() is not None:
                stdout, stderr = process.communicate()
                completed += 1
                
                if "SUCCESS" in stdout:
                    success_found = True
                    winning_agent = agent_num
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 Agent #{agent_num:03d} FOUND SUCCESS!{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.BLUE}Agent #{agent_num:03d}: Completed (PIN failed){Style.RESET_ALL}")
                
                # Remove from monitoring
                processes[i] = (agent_num, None)
        
        time.sleep(2)  # Check every 2 seconds
    
    # Terminate remaining agents if success found
    if success_found:
        print(f"\n{Fore.YELLOW}🛑 Terminating remaining agents...{Style.RESET_ALL}")
        for agent_num, process in processes:
            if process and process.poll() is None:
                try:
                    process.terminate()
                    print(f"{Fore.YELLOW}🛑 Agent #{agent_num:03d}: Terminated{Style.RESET_ALL}")
                except:
                    pass
    
    return success_found, winning_agent

def main():
    """Main army deployment function"""
    display_army_banner()
    
    print(f"{Fore.CYAN}📋 DEPLOYMENT PLAN:{Style.RESET_ALL}")
    print(f"   • Launch all 106 agents simultaneously")
    print(f"   • Each agent opens its own browser")
    print(f"   • Each agent tests exactly 1 PIN")
    print(f"   • All agents use proxy rotation")
    print(f"   • First success stops all agents")
    print()
    
    # Check if agents exist
    agent_count = 0
    for i in range(1, MAX_AGENTS + 1):
        agent_dir = BASE_DIR / f"agent_{i:03d}"
        if agent_dir.exists() and (agent_dir / "main.py").exists():
            agent_count += 1
    
    if agent_count == 0:
        print(f"{Fore.RED}❌ No agents found! Run 'python create_agents.py' first{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✅ Found {agent_count} agents ready for deployment{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}Press ENTER to deploy the army...{Style.RESET_ALL}")
    
    # Launch all agents
    print(f"\n{Fore.RED}🔥 DEPLOYING ARMY...{Style.RESET_ALL}")
    processes = []
    start_time = time.time()
    
    for i in range(1, agent_count + 1):
        process = launch_single_agent(i)
        processes.append((i, process))
        time.sleep(0.5)  # Small delay between launches
    
    launched_count = len([p for _, p in processes if p is not None])
    print(f"\n{Fore.GREEN}✅ ARMY DEPLOYED: {launched_count}/{agent_count} agents launched{Style.RESET_ALL}")
    
    # Monitor for results
    success_found, winning_agent = monitor_agents(processes)
    
    # Final results
    end_time = time.time()
    total_time = end_time - start_time
    
    if success_found:
        victory_banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 ARMY MISSION ACCOMPLISHED! 🎉                         ║
║                                                                              ║
║  Booking ID: {BOOKING_ID}                                                    ║
║  Victorious Agent: #{winning_agent or 'DETECTED'}                           ║
║  Total deployment time: {total_time:.1f} seconds                             ║
║  Agents launched: {launched_count}                                           ║
║                                                                              ║
║                     🏆 INDEPENDENT ARMY VICTORY! 🏆                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(victory_banner)
    else:
        print(f"\n{Fore.RED}💔 Army deployment completed - no success found{Style.RESET_ALL}")
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Agents launched: {launched_count}")
    
    print(f"\n{Fore.CYAN}📊 ARMY STATISTICS:")
    print(f"• Booking ID tested: {BOOKING_ID}")
    print(f"• Agents deployed: {launched_count}")
    print(f"• Success rate: {'100%' if success_found else '0%'}")
    print(f"• Average time per agent: {total_time/launched_count:.2f} seconds")
    print(f"• Independent browsers: {launched_count}")
    print(f"• Proxy IPs used: {launched_count}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
