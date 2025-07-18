#!/usr/bin/env python3
"""
Update all agents to use single booking ID: 6339614781
"""

import os
import glob

def update_all_agents_single_booking():
    """Update all agents to use single booking ID"""
    
    booking_id = "6339614781"
    
    # Get all agent files
    agent_files = glob.glob("boss_ai_playwright_*.py")
    
    print(f"🎯 UPDATING ALL AGENTS TO SINGLE BOOKING ID: {booking_id}")
    print(f"📁 Found {len(agent_files)} agent files")
    print("="*60)
    
    for agent_file in agent_files:
        try:
            # Read current content
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update default booking ID
            content = content.replace(
                'default="6160911170"',
                f'default="{booking_id}"'
            )
            content = content.replace(
                'default="6763779197"',
                f'default="{booking_id}"'
            )
            content = content.replace(
                'default="6763734263"',
                f'default="{booking_id}"'
            )
            
            # Update hardcoded booking IDs
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
            
            # Update delay timings to 30 seconds
            content = content.replace(
                'DELAY_BETWEEN_ATTEMPTS = 45',
                'DELAY_BETWEEN_ATTEMPTS = 30'
            )
            content = content.replace(
                'DELAY_BETWEEN_ATTEMPTS = 60',
                'DELAY_BETWEEN_ATTEMPTS = 30'
            )
            
            # Write updated content
            with open(agent_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated {agent_file}")
            
        except Exception as e:
            print(f"❌ Error updating {agent_file}: {e}")
    
    print(f"\n🎯 ALL AGENTS UPDATED!")
    print(f"📋 Booking ID: {booking_id}")
    print(f"⏱️ Delay: 30 seconds between attempts")
    print(f"🚀 Ready to deploy the ARMY!")

if __name__ == "__main__":
    update_all_agents_single_booking()
