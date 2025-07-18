#!/usr/bin/env python3
"""
🔄 PROXY UPDATE SCRIPT - NEW CREDENTIALS
Update all PIN hunter scripts with new proxy configuration
"""

import os
import glob
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def update_proxy_in_file(file_path):
    """Update proxy configuration in a specific file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Define the old proxy configuration to replace
        old_config = '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "phantom1_rOHk6",
    "password": "phantom1_rOHk6"
}'''
        
        # Define the new proxy configuration
        new_config = '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}'''
        
        # Replace the configuration
        if old_config in content:
            content = content.replace(old_config, new_config)
            
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"{Fore.GREEN}✅ Updated: {file_path}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  No match found in: {file_path}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Error updating {file_path}: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    """Main function to update proxy configuration"""
    print(f"{Fore.CYAN}{Style.BRIGHT}🔄 UPDATING PROXY CONFIGURATION{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Old credentials: phantom1_rOHk6{Style.RESET_ALL}")
    print(f"{Fore.GREEN}New credentials: phantomnet1_ONP6z{Style.RESET_ALL}")
    print("-" * 60)
    
    # List of files to update
    files_to_update = [
        "auto_pin_hunter.py",
        "boss_ai_playwright.py",
        "boss_ai_playwright_1A.py",
        "target_pin_hunter_5727559423.py",
        "targeted_pin_tester_5727559423.py",
        "automation_system.py",
        "real_pin_hunter_6160911170.py"
    ]
    
    # Also find all boss_ai_playwright_* files
    boss_ai_files = glob.glob("boss_ai_playwright_*.py")
    files_to_update.extend(boss_ai_files)
    
    # Remove duplicates
    files_to_update = list(set(files_to_update))
    
    updated_count = 0
    
    for file_name in files_to_update:
        if os.path.exists(file_name):
            if update_proxy_in_file(file_name):
                updated_count += 1
        else:
            print(f"{Fore.YELLOW}⚠️  File not found: {file_name}{Style.RESET_ALL}")
    
    print("-" * 60)
    print(f"{Fore.GREEN}{Style.BRIGHT}🎯 PROXY UPDATE COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Updated {updated_count} files with new proxy configuration{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}New proxy: phantomnet1_ONP6z / phantomnet1_ONP6z{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Server: pr.oxylabs.io:7777{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
