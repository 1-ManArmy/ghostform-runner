#!/usr/bin/env python3
"""
🔄 FINAL PROXY UPDATE - NEW CREDENTIALS
Update all files with the latest proxy configuration
"""

import os
import glob
from colorama import init, Fore, Style

init()

def update_proxy_bulk():
    """Update proxy in all relevant files"""
    files_to_update = [
        "real_pin_hunter_6160911170.py",
        "boss_ai_playwright_1A.py",
        "auto_pin_hunter.py",
        "target_pin_hunter_5727559423.py",
        "targeted_pin_tester_5727559423.py",
        "automation_system.py"
    ]
    
    # Add all boss_ai_playwright files
    boss_files = glob.glob("boss_ai_playwright_*.py")
    files_to_update.extend(boss_files)
    
    old_configs = [
        '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}''',
        '''PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}'''
    ]
    
    new_config = '''PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}'''
    
    updated_count = 0
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                updated = False
                for old_config in old_configs:
                    if old_config in content:
                        content = content.replace(old_config, new_config)
                        updated = True
                        break
                
                if updated:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"{Fore.GREEN}✅ Updated: {file_path}{Style.RESET_ALL}")
                    updated_count += 1
                else:
                    print(f"{Fore.YELLOW}⚠️ No match: {file_path}{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {file_path} - {e}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎯 FINAL PROXY UPDATE COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Updated {updated_count} files{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}New proxy: customer-phantomnet1_ONP6z@us-pr.oxylabs.io:10000{Style.RESET_ALL}")

if __name__ == "__main__":
    update_proxy_bulk()
