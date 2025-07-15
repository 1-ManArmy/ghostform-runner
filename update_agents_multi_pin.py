#!/usr/bin/env python3
"""
Update all agents to use multi_pin_manager
"""

import os
import glob

def update_agent_files():
    """Update all agent files to use multi_pin_manager"""
    
    # Get all agent files
    agent_files = glob.glob("boss_ai_playwright_*.py")
    
    for agent_file in agent_files:
        print(f"Updating {agent_file}...")
        
        # Read current content
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update imports
        content = content.replace(
            'from pin_manager import get_pin_manager',
            'from multi_pin_manager import PinManager'
        )
        
        # Update PIN manager usage
        content = content.replace(
            'pin_mgr = get_pin_manager(CONFIRMATION)',
            'pin_mgr = PinManager(CONFIRMATION)'
        )
        
        # Update method calls
        content = content.replace(
            'pin_mgr.get_random_pins(AGENT_NAME, 5)',
            '[pin_mgr.get_next_pin(AGENT_NAME) for _ in range(10) if pin_mgr.get_next_pin(AGENT_NAME)]'
        )
        
        # Write updated content
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {agent_file}")

if __name__ == "__main__":
    update_agent_files()
    print("\n🎯 All agent files updated to use multi_pin_manager!")
