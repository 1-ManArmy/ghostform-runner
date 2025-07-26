import os
import re
from colorama import init, Fore, Style
init()

print(f"{Fore.CYAN}🔧 SYNTAX ERROR FIX TOOL 🔧{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Fixing missing quotes in agent print statements{Style.RESET_ALL}")
print(f"{Fore.RED}🎯 BEGINNING SYNTAX REPAIR!{Style.RESET_ALL}")

def fix_agent_syntax(filename):
    """Fix syntax errors in agent file"""
    if not os.path.exists(filename):
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix missing closing quote in print statement
        # Pattern: print(f"🔑 Assigned PINs: 1435, 1436, 1437, 1438, 1439
        # Should be: print(f"🔑 Assigned PINs: {PINS}")
        
        # Find lines with missing quotes
        fixed_content = re.sub(
            r'print\(f"🔑 Assigned PINs: [0-9, ]+\n',
            'print(f"🔑 Assigned PINs: {PINS}")\n',
            content
        )
        
        # Also fix the variable reference
        fixed_content = re.sub(
            r'print\(f"🔑 Assigned PINs: \{PINS\}"\)',
            'print(f"🔑 Assigned PINs: {PINS}")',
            fixed_content
        )
        
        # Write back if changes were made
        if fixed_content != content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error fixing {filename}: {e}{Style.RESET_ALL}")
        return False

# Fix all agent files
total_fixed = 0
batches = ['A', 'B', 'C', 'D']

for agent_num in range(1, 101):
    for batch in batches:
        filename = f"agent_{agent_num:03d}{batch}.py"
        if os.path.exists(filename):
            if fix_agent_syntax(filename):
                print(f"{Fore.GREEN}✅ Fixed: {filename}{Style.RESET_ALL}")
                total_fixed += 1
            else:
                print(f"{Fore.BLUE}⚪ No fix needed: {filename}{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}🎉 SYNTAX REPAIR COMPLETE!{Style.RESET_ALL}")
print(f"{Fore.CYAN}📊 Total files fixed: {total_fixed}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}✅ All agent files should now have correct syntax{Style.RESET_ALL}")
print(f"{Fore.RED}🏆 400-AGENT ARMY READY FOR DEPLOYMENT!{Style.RESET_ALL}")
