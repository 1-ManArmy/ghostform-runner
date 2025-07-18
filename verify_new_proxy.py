#!/usr/bin/env python3
"""
✅ PROXY VERIFICATION SCRIPT
Verify all PIN hunter scripts have the new proxy configuration
"""

import os
import glob
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def verify_proxy_in_file(file_path):
    """Verify proxy configuration in a specific file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for new proxy credentials
        if 'phantomnet1_ONP6z' in content:
            print(f"{Fore.GREEN}✅ UPDATED: {file_path}{Style.RESET_ALL}")
            return True
        elif 'phantom1_rOHk6' in content:
            print(f"{Fore.RED}❌ OLD PROXY: {file_path}{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.YELLOW}⚠️  NO PROXY: {file_path}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ ERROR: {file_path} - {str(e)}{Style.RESET_ALL}")
        return False

def main():
    """Main function to verify proxy configuration"""
    print(f"{Fore.CYAN}{Style.BRIGHT}🔍 PROXY CONFIGURATION VERIFICATION{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Checking for: phantomnet1_ONP6z{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Server: pr.oxylabs.io:7777{Style.RESET_ALL}")
    print("-" * 60)
    
    # List of critical files to verify
    critical_files = [
        "real_pin_hunter_6160911170.py",
        "target_pin_hunter_5727559423.py",
        "targeted_pin_tester_5727559423.py",
        "auto_pin_hunter.py",
        "boss_ai_playwright_1A.py",
        "automation_system.py"
    ]
    
    print(f"{Fore.CYAN}{Style.BRIGHT}🎯 CRITICAL FILES:{Style.RESET_ALL}")
    updated_count = 0
    
    for file_name in critical_files:
        if os.path.exists(file_name):
            if verify_proxy_in_file(file_name):
                updated_count += 1
        else:
            print(f"{Fore.YELLOW}⚠️  File not found: {file_name}{Style.RESET_ALL}")
    
    print("-" * 60)
    print(f"{Fore.CYAN}{Style.BRIGHT}🔢 ALL BOSS AI FILES:{Style.RESET_ALL}")
    
    # Check all boss_ai_playwright files
    boss_ai_files = glob.glob("boss_ai_playwright_*.py")
    boss_updated = 0
    
    for file_name in sorted(boss_ai_files):
        if verify_proxy_in_file(file_name):
            boss_updated += 1
    
    print("-" * 60)
    print(f"{Fore.GREEN}{Style.BRIGHT}🎯 VERIFICATION COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Critical files updated: {updated_count}/{len(critical_files)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Boss AI files updated: {boss_updated}/{len(boss_ai_files)}{Style.RESET_ALL}")
    
    if updated_count == len(critical_files) and boss_updated == len(boss_ai_files):
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ ALL FILES SUCCESSFULLY UPDATED!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}New proxy: phantomnet1_ONP6z{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Ready for stealth PIN hunting! 🥷{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Some files may need manual update{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
