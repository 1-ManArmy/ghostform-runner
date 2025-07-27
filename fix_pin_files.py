#!/usr/bin/env python3
"""
🔧 PIN File Updater - Fix encoding and update agent files with assigned PINs
"""

import json
import re
import os

def update_agent_files_fixed():
    """Update all agent files with UTF-8 encoding"""
    print("🔧 Starting PIN file updates with proper encoding...")
    
    # Load the PIN allocation
    with open("pin_allocation_master.json", 'r', encoding='utf-8') as f:
        allocation = json.load(f)
    
    updated_count = 0
    error_count = 0
    
    for agent_num in range(1, 1001):  # 1 to 1000
        agent_file = f"boss_ai_playwright_pin{agent_num}.py"
        agent_key = f"agent_{agent_num}"
        
        if os.path.exists(agent_file) and agent_key in allocation["agent_pins"]:
            agent_pins = allocation["agent_pins"][agent_key]["pins"]
            pins_string = ",".join(agent_pins)
            
            try:
                # Read the file with UTF-8 encoding
                with open(agent_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Update the default pins argument
                # Look for the pattern: default="XXXX,YYYY"
                pattern = r'default="[^"]*"'
                replacement = f'default="{pins_string}"'
                
                updated_content = re.sub(pattern, replacement, content)
                
                # Write back to file with UTF-8 encoding
                with open(agent_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                updated_count += 1
                
                if agent_num <= 5 or agent_num % 100 == 0:  # Show progress
                    print(f"✅ Updated {agent_file} with PINs: {pins_string}")
            
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Show first 5 errors
                    print(f"❌ Error updating {agent_file}: {e}")
    
    print(f"\n🎉 PIN UPDATE COMPLETE!")
    print(f"✅ Successfully updated: {updated_count} files")
    print(f"❌ Errors encountered: {error_count} files")
    
    return updated_count

if __name__ == "__main__":
    update_agent_files_fixed()
