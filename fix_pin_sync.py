import os
import re
from colorama import init, Fore, Style
init()

print(f"{Fore.CYAN}🔧 PIN SYNCHRONIZATION TOOL 🔧{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Modifying existing B, C, D agents to match A agent PIN ranges{Style.RESET_ALL}")
print(f"{Fore.GREEN}Strategy: Agent 1B, 1C, 1D will have same PINs as 1A{Style.RESET_ALL}")
print(f"{Fore.RED}🎯 SYNCHRONIZING EXISTING AGENTS!{Style.RESET_ALL}")

def get_pins_from_agent_a(agent_num):
    """Get the PIN range from the corresponding A agent"""
    start_pin = 1000 + (agent_num - 1) * 5
    return [str(start_pin + j) for j in range(5)]

def update_agent_pins(agent_file, new_pins):
    """Update the PINS line in an agent file"""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the PINS line
        pins_str = str(new_pins).replace("'", '"')
        content = re.sub(r'PINS = \[.*?\]', f'PINS = {pins_str}', content)
        
        # Update the header comment PINs line
        pins_comment = ', '.join(new_pins)
        content = re.sub(r'PINs: [\d, ]+', f'PINs: {pins_comment}', content)
        
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error updating {agent_file}: {e}{Style.RESET_ALL}")
        return False

# Process all agents
for agent_num in range(1, 101):
    # Get the correct PIN range from A agent logic
    correct_pins = get_pins_from_agent_a(agent_num)
    
    print(f"{Fore.YELLOW}🔧 Synchronizing Agent {agent_num:03d} (PINs: {', '.join(correct_pins)})...{Style.RESET_ALL}")
    
    # Update B, C, D agents to match A agent
    for batch_letter in ['B', 'C', 'D']:
        agent_file = f"agent_{agent_num:03d}{batch_letter}.py"
        
        if os.path.exists(agent_file):
            if update_agent_pins(agent_file, correct_pins):
                print(f"{Fore.GREEN}  ✅ Updated {agent_file} PINs: {', '.join(correct_pins)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ❌ Failed to update {agent_file}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}  ⚠️ File not found: {agent_file}{Style.RESET_ALL}")

print(f"{Fore.GREEN}🎉 PIN SYNCHRONIZATION COMPLETE!{Style.RESET_ALL}")
print(f"{Fore.CYAN}📊 Result: All agent numbers now test the same PINs across A, B, C, D batches{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}🎯 Example: 001A, 001B, 001C, 001D all test PINs 1000-1004{Style.RESET_ALL}")
print(f"{Fore.BLUE}🔄 Coverage: Each PIN set tested against all 4 booking IDs{Style.RESET_ALL}")
print(f"{Fore.GREEN}✅ SYNCHRONIZED ARMY READY FOR DEPLOYMENT!{Style.RESET_ALL}")
