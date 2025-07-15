#!/usr/bin/env python3
"""
Fix all agent files to work properly with multi_pin_manager
"""

import os
import glob

def fix_agent_files():
    """Fix all agent files to work with multi_pin_manager"""
    
    # Get all agent files
    agent_files = glob.glob("boss_ai_playwright_*.py")
    
    print(f"🔧 FIXING ALL AGENT FILES")
    print(f"📁 Found {len(agent_files)} agent files")
    print("="*60)
    
    for agent_file in agent_files:
        print(f"Fixing {agent_file}...")
        
        # Read current content
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the PIN generation logic
        old_pin_logic = """# Get PIN manager and random PINs
pin_mgr = PinManager(CONFIRMATION)
PINS = [pin_mgr.get_next_pin(AGENT_NAME) for _ in range(10) if pin_mgr.get_next_pin(AGENT_NAME)]"""
        
        new_pin_logic = """# Get PIN manager and PINs
pin_mgr = PinManager(CONFIRMATION)
PINS = []
for _ in range(10):
    pin = pin_mgr.get_next_pin(AGENT_NAME)
    if pin:
        PINS.append(pin)"""
        
        content = content.replace(old_pin_logic, new_pin_logic)
        
        # Fix the log_result method call
        old_log_method = """def log_result(pin, result, url):
    pin_mgr.log_result(AGENT_NAME, pin, result, url)"""
        
        new_log_method = """def log_result(pin, result, url):
    pin_mgr.record_result(AGENT_NAME, pin, result)"""
        
        content = content.replace(old_log_method, new_log_method)
        
        # Fix the success check
        old_success_check = """# Check if success already found
if pin_mgr.is_success_found():
    print(f"Success already found! PIN: {pin_mgr.data['success_pin']}")
    exit(0)"""
        
        new_success_check = """# Check if success already found
if pin_mgr.get_success_pin():
    print(f"Success already found! PIN: {pin_mgr.get_success_pin()}")
    exit(0)"""
        
        content = content.replace(old_success_check, new_success_check)
        
        # Write updated content
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {agent_file}")
    
    print(f"\n🎯 ALL AGENT FILES FIXED!")
    print(f"📊 Total agents: {len(agent_files)}")

if __name__ == "__main__":
    fix_agent_files()
