#!/usr/bin/env python3
"""
Update all agent files for production with booking ID 6160911170 and 5 attempts per agent
"""

import os
import glob

def update_agent_file(filepath):
    """Update a single agent file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update booking ID
        content = content.replace(
            'parser.add_argument(\'--confirmation\', type=str, default="1234567890", help=\'Confirmation number\')',
            'parser.add_argument(\'--confirmation\', type=str, default="6160911170", help=\'Confirmation number\')'
        )
        
        # Update PIN count to 5
        content = content.replace(
            'PINS = pin_mgr.get_random_pins(AGENT_NAME, 2)',
            'PINS = pin_mgr.get_random_pins(AGENT_NAME, 5)'
        )
        
        # Save updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated: {os.path.basename(filepath)}")
        return True
    
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Update all agent files"""
    print("🚀 Updating all agent files for production...")
    print("📋 Booking ID: 6160911170")
    print("🎯 PINs per agent: 5")
    print("-" * 50)
    
    # Find all agent files
    agent_files = glob.glob("boss_ai_playwright_*.py")
    
    # Also include the main file
    if os.path.exists("boss_ai_playwright.py"):
        agent_files.append("boss_ai_playwright.py")
    
    updated_count = 0
    total_count = len(agent_files)
    
    for filepath in sorted(agent_files):
        if update_agent_file(filepath):
            updated_count += 1
    
    print("-" * 50)
    print(f"📊 Results: {updated_count}/{total_count} files updated successfully")
    
    if updated_count == total_count:
        print("🎉 All agent files updated successfully!")
        print("\n🚀 Production Commands:")
        print("• Start automation: python master_automation.py --confirmation 6160911170 --headless")
        print("• Check status: python check_status.py --confirmation 6160911170")
        print("• Manual test: python boss_ai_playwright_A.py --confirmation 6160911170")
    else:
        print(f"⚠️ {total_count - updated_count} files failed to update")

if __name__ == "__main__":
    main()
