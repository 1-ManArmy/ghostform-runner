#!/usr/bin/env python3
"""
🔍 AGENT VERIFICATION - Check All 106 Agents
Verifies that all agents are properly configured and ready for deployment
"""

import os
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

BASE_DIR = Path(".")
MAX_AGENTS = 106

def verify_agent(agent_num):
    """Verify a single agent configuration"""
    agent_dir = BASE_DIR / f"agent_{agent_num:03d}"
    main_py_path = agent_dir / "main.py"
    
    if not agent_dir.exists():
        return False, "Folder missing"
    
    if not main_py_path.exists():
        return False, "main.py missing"
    
    # Check main.py content
    try:
        with open(main_py_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check for required components
        checks = {
            "Booking ID": 'BOOKING_ID = "5724349472"' in content,
            "PIN Variable": "ASSIGNED_PIN =" in content,
            "Playwright": "from playwright.sync_api import sync_playwright" in content,
            "Proxy Setup": "PROXY_CONFIG" in content,
        }
        
        failed_checks = [check for check, passed in checks.items() if not passed]
        
        if failed_checks:
            return False, f"Missing: {', '.join(failed_checks)}"
        
        # Extract PIN for verification
        for line in content.split('\n'):
            if line.strip().startswith('ASSIGNED_PIN = "') and line.strip().endswith('"'):
                pin = line.strip().split('"')[1]
                return True, f"PIN {pin}"
        
        return False, "PIN extraction failed"
        
    except Exception as e:
        return False, f"Read error: {e}"

def main():
    """Main verification function"""
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
🔍 AGENT ARMY VERIFICATION
============================
Checking all 106 agents for proper configuration...
{Style.RESET_ALL}
""")
    
    verified_agents = 0
    failed_agents = 0
    pin_list = []
    
    for i in range(1, MAX_AGENTS + 1):
        success, details = verify_agent(i)
        
        if success:
            verified_agents += 1
            pin = details.split("PIN ")[1]
            pin_list.append(pin)
            print(f"{Fore.GREEN}✅ Agent #{i:03d}: {details}{Style.RESET_ALL}")
        else:
            failed_agents += 1
            print(f"{Fore.RED}❌ Agent #{i:03d}: {details}{Style.RESET_ALL}")
    
    # Summary
    print(f"\n{Fore.CYAN}📊 VERIFICATION SUMMARY:")
    print(f"• Total agents: {MAX_AGENTS}")
    print(f"• Verified agents: {Fore.GREEN}{verified_agents}{Fore.CYAN}")
    print(f"• Failed agents: {Fore.RED}{failed_agents}{Fore.CYAN}")
    print(f"• Success rate: {verified_agents/MAX_AGENTS*100:.1f}%")
    print(f"• Unique PINs: {len(set(pin_list))}")
    print(f"• Booking ID: 5724349472{Style.RESET_ALL}")
    
    if verified_agents == MAX_AGENTS:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 ALL AGENTS READY FOR DEPLOYMENT!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Run 'python launch_army.py' to deploy the army{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}⚠️  Some agents need fixing before deployment{Style.RESET_ALL}")
    
    # Show first 10 PINs as sample
    if pin_list:
        print(f"\n{Fore.CYAN}📋 Sample PINs (first 10):")
        for i, pin in enumerate(pin_list[:10]):
            print(f"   Agent #{i+1:03d}: {pin}")
        if len(pin_list) > 10:
            print(f"   ... and {len(pin_list)-10} more")
        print(f"{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
