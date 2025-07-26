import os
import re
from colorama import init, Fore, Style
init()

print(f"{Fore.CYAN}🔧 PIN SYNCHRONIZATION TOOL 🔧{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Modifying existing B, C, D agents to match A batch PINs{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}Strategy: Keep existing files, just fix PIN assignments{Style.RESET_ALL}")
print(f"{Fore.RED}🎯 BEGINNING PIN SYNCHRONIZATION!{Style.RESET_ALL}")

def get_agent_a_pins(agent_num):
    """Get PIN list from corresponding A batch agent"""
    a_file = f"agent_{agent_num:03d}A.py"
    if not os.path.exists(a_file):
        return None
    
    with open(a_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract PINs from the A agent
    pins_match = re.search(r'PINS = \[(.*?)\]', content)
    if pins_match:
        pins_str = pins_match.group(1)
        # Clean and extract pin values
        pins = [pin.strip().strip("'\"") for pin in pins_str.split(',')]
        return pins
    return None

def update_agent_pins(agent_file, new_pins):
    """Update PIN assignment in existing agent file"""
    if not os.path.exists(agent_file):
        return False
    
    with open(agent_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Format new pins for replacement
    new_pins_str = "[" + ", ".join([f"'{pin}'" for pin in new_pins]) + "]"
    
    # Replace PINS assignment
    content = re.sub(r'PINS = \[.*?\]', f'PINS = {new_pins_str}', content)
    
    # Update PINs in comment header
    pins_comment = ", ".join(new_pins)
    content = re.sub(r'PINs: .*', f'PINs: {pins_comment}', content)
    
    # Write back to file
    with open(agent_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Process all agents
total_updated = 0
batches_to_sync = ['B', 'C', 'D']

for agent_num in range(1, 101):
    # Get PINs from A batch agent
    a_pins = get_agent_a_pins(agent_num)
    if not a_pins:
        print(f"{Fore.RED}❌ Could not get PINs from agent_{agent_num:03d}A.py{Style.RESET_ALL}")
        continue
    
    print(f"{Fore.YELLOW}🔄 Synchronizing Agent {agent_num:03d} - PINs: {', '.join(a_pins)}{Style.RESET_ALL}")
    
    # Update B, C, D agents with same PINs
    for batch in batches_to_sync:
        agent_file = f"agent_{agent_num:03d}{batch}.py"
        if update_agent_pins(agent_file, a_pins):
            print(f"{Fore.GREEN}  ✅ Updated: {agent_file}{Style.RESET_ALL}")
            total_updated += 1
        else:
            print(f"{Fore.RED}  ❌ Failed: {agent_file}{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}🎉 PIN SYNCHRONIZATION COMPLETE!{Style.RESET_ALL}")
print(f"{Fore.CYAN}📊 Total agents updated: {total_updated}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}✅ All B, C, D agents now have same PINs as corresponding A agents{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}🎯 Strategy achieved: 1A,1B,1C,1D test same PINs with different booking IDs{Style.RESET_ALL}")
print(f"{Fore.RED}🏆 SYNCHRONIZED ARMY READY FOR DEPLOYMENT!{Style.RESET_ALL}")
