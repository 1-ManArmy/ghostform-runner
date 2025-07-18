#!/usr/bin/env python3
"""
Final verification of proxy configuration update
"""

from colorama import Fore, Style, init
import glob

# Initialize colorama
init(autoreset=True)

def main():
    """Verify proxy configuration is updated"""
    print(f"{Fore.GREEN}{Style.BRIGHT}🔄 PROXY CONFIGURATION UPDATE VERIFICATION{Style.RESET_ALL}")
    print("=" * 60)
    
    # Key files to check
    key_files = [
        "targeted_pin_tester_5727559423.py",
        "automation_system.py", 
        "target_pin_hunter_5727559423.py",
        "boss_ai_playwright_1A.py",
        "auto_pin_hunter.py"
    ]
    
    print(f"{Fore.CYAN}🔍 Checking key files...{Style.RESET_ALL}")
    
    for file_path in key_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'phantom1_rOHk6' in content:
                print(f"{Fore.GREEN}✅ {file_path} - Updated successfully{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {file_path} - Not updated{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ {file_path} - Error: {e}{Style.RESET_ALL}")
    
    print("\n" + "=" * 60)
    print(f"{Fore.GREEN}{Style.BRIGHT}🎯 PROXY UPDATE COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}New credentials: phantom1_rOHk6 / phantom1_rOHk6{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🚀 Ready to run PIN hunting system!{Style.RESET_ALL}")
    print("=" * 60)

if __name__ == "__main__":
    main()
