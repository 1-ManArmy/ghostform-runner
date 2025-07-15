#!/usr/bin/env python3
"""
Update all agents to use single booking ID 6339614781 with 30s timing
"""

import os
import glob

def update_all_agents():
    """Update all agent files to use single booking ID"""
    
    booking_id = "6339614781"
    
    # Get all agent files
    agent_files = glob.glob("boss_ai_playwright_*.py")
    
    print(f"🎯 UPDATING ALL AGENTS TO BOOKING ID: {booking_id}")
    print(f"⏱️ Setting timing to 30 seconds")
    print(f"📁 Found {len(agent_files)} agent files")
    print("="*60)
    
    for agent_file in agent_files:
        print(f"Updating {agent_file}...")
        
        # Read current content
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update booking ID in default argument
        content = content.replace(
            'default="6160911170"',
            f'default="{booking_id}"'
        )
        
        # Update any hardcoded booking IDs
        content = content.replace(
            'BOOKING_CONFIRMATION = "6160911170"',
            f'BOOKING_CONFIRMATION = "{booking_id}"'
        )
        content = content.replace(
            'BOOKING_CONFIRMATION = "6763779197"',
            f'BOOKING_CONFIRMATION = "{booking_id}"'
        )
        content = content.replace(
            'BOOKING_CONFIRMATION = "6763734263"',
            f'BOOKING_CONFIRMATION = "{booking_id}"'
        )
        
        # Update timing to 30 seconds
        content = content.replace(
            'DELAY_BETWEEN_ATTEMPTS = 45',
            'DELAY_BETWEEN_ATTEMPTS = 30'
        )
        content = content.replace(
            'default=60',
            'default=30'
        )
        
        # Write updated content
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {agent_file}")
    
    print(f"\n🎯 ALL AGENTS UPDATED!")
    print(f"📋 Booking ID: {booking_id}")
    print(f"⏱️ Timing: 30 seconds")
    print(f"📊 Total agents: {len(agent_files)}")

if __name__ == "__main__":
    update_all_agents()
