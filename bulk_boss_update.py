#!/usr/bin/env python3
"""
🔄 BULK BOSS AGENT UPDATE SCRIPT
Update all 105+ boss agent files with:
- New proxy credentials
- 5 attempts per agent
- 15s break between attempts
- 30s delay between agents
"""

import os
import glob
from colorama import init, Fore, Style

init()

def update_boss_agent_file(file_path):
    """Update a single boss agent file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update proxy configuration
        old_proxy_patterns = [
            '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}''',
            '''PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}''',
            '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}'''
        ]
        
        new_proxy = '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-1proxylabs_atNPR-cc-us",
    "password": "1proxylabs_atNPR1"
}'''
        
        # Replace proxy config
        proxy_updated = False
        for old_pattern in old_proxy_patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_proxy)
                proxy_updated = True
                break
        
        # Update attempts configuration
        if 'for _ in range(10):' in content:
            content = content.replace('for _ in range(10):', 'for _ in range(5):')
        
        # Update wait time configuration  
        if 'default=30' in content and 'wait time' in content.lower():
            content = content.replace('default=30', 'default=15')
        elif 'default=5' in content and 'wait time' in content.lower():
            content = content.replace('default=5', 'default=15')
        
        # Update HEADLESS setting to False
        if 'HEADLESS = args.headless' in content:
            content = content.replace('HEADLESS = args.headless', 'HEADLESS = False  # Always show browser')
        
        # Update agent name extraction from filename
        if 'AGENT_NAME = "' in content:
            # Extract agent name from filename
            base_name = os.path.basename(file_path).replace('.py', '').replace('boss_ai_playwright_', 'BOSS_')
            if base_name == 'boss_ai_playwright':
                base_name = 'BOSS_MAIN'
            content = content.replace(
                'AGENT_NAME = "1A"', f'AGENT_NAME = "{base_name}"'
            )
            content = content.replace(
                'AGENT_NAME = "BOSS_1A"', f'AGENT_NAME = "{base_name}"'
            )
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, proxy_updated
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error updating {file_path}: {e}{Style.RESET_ALL}")
        return False, False

def main():
    """Main update function"""
    print(f"{Fore.CYAN}{Style.BRIGHT}🔄 BULK BOSS AGENT UPDATE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}New proxy: customer-1proxylabs_atNPR-cc-us@pr.oxylabs.io:7777{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Configuration: 5 attempts, 15s breaks, 30s between agents{Style.RESET_ALL}")
    print("-" * 70)
    
    # Find all boss agent files
    boss_files = glob.glob("boss_ai_playwright*.py")
    
    updated_count = 0
    proxy_updated_count = 0
    
    for file_path in sorted(boss_files):
        success, proxy_updated = update_boss_agent_file(file_path)
        if success:
            updated_count += 1
            if proxy_updated:
                proxy_updated_count += 1
            print(f"{Fore.GREEN}✅ Updated: {file_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Failed: {file_path}{Style.RESET_ALL}")
    
    print("-" * 70)
    print(f"{Fore.GREEN}{Style.BRIGHT}🎯 BULK UPDATE COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total files processed: {len(boss_files)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Successfully updated: {updated_count}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Proxy updated: {proxy_updated_count}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}New settings:{Style.RESET_ALL}")
    print(f"  - Proxy: customer-1proxylabs_atNPR-cc-us@pr.oxylabs.io:7777")
    print(f"  - Attempts per agent: 5")
    print(f"  - Break between attempts: 15 seconds")
    print(f"  - Delay between agents: 30 seconds")
    print(f"  - Browser: Visible (headless=False)")

if __name__ == "__main__":
    main()
