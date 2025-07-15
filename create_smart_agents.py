#!/usr/bin/env python3
"""
Smart Agent Generator - Creates distributed agent files for multiple booking IDs
"""

import os
import shutil

def create_agent_files():
    """Create all agent files with smart distribution"""
    
    # Booking IDs and their assigned agent ranges
    booking_assignments = {
        "6339614781": {"range": "A-Z", "prefix": ""},
        "6763779197": {"range": "A-Z", "prefix": "1"},
        "6763734263": {"range": "A-Z", "prefix": "2"},
        "6339614781": {"range": "A-Z", "prefix": "3"}  # Second round for first booking
    }
    
    # Read the original file
    with open('boss_ai_playwright.py', 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    agents_created = 0
    
    # Create A-Z agents for first booking ID
    booking_id = "6339614781"
    for i in range(26):
        letter = chr(ord('A') + i)
        filename = f"boss_ai_playwright_{letter}.py"
        
        # Modify content for this agent
        modified_content = original_content.replace(
            'BOOKING_CONFIRMATION = "6160911170"',
            f'BOOKING_CONFIRMATION = "{booking_id}"'
        ).replace(
            'AGENT_NAME = "PRIMARY"',
            f'AGENT_NAME = "{letter}"'
        ).replace(
            'MAX_ATTEMPTS = 5',
            'MAX_ATTEMPTS = 10'
        ).replace(
            'DELAY_BETWEEN_ATTEMPTS = 5',
            'DELAY_BETWEEN_ATTEMPTS = 45'  # 45 seconds between attempts
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        agents_created += 1
        print(f"Created {filename} for booking {booking_id}")
    
    # Create 1A-1Z agents for second booking ID
    booking_id = "6763779197"
    for i in range(26):
        letter = chr(ord('A') + i)
        filename = f"boss_ai_playwright_1{letter}.py"
        
        modified_content = original_content.replace(
            'BOOKING_CONFIRMATION = "6160911170"',
            f'BOOKING_CONFIRMATION = "{booking_id}"'
        ).replace(
            'AGENT_NAME = "PRIMARY"',
            f'AGENT_NAME = "1{letter}"'
        ).replace(
            'MAX_ATTEMPTS = 5',
            'MAX_ATTEMPTS = 10'
        ).replace(
            'DELAY_BETWEEN_ATTEMPTS = 5',
            'DELAY_BETWEEN_ATTEMPTS = 45'
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        agents_created += 1
        print(f"Created {filename} for booking {booking_id}")
    
    # Create 2A-2Z agents for third booking ID
    booking_id = "6763734263"
    for i in range(26):
        letter = chr(ord('A') + i)
        filename = f"boss_ai_playwright_2{letter}.py"
        
        modified_content = original_content.replace(
            'BOOKING_CONFIRMATION = "6160911170"',
            f'BOOKING_CONFIRMATION = "{booking_id}"'
        ).replace(
            'AGENT_NAME = "PRIMARY"',
            f'AGENT_NAME = "2{letter}"'
        ).replace(
            'MAX_ATTEMPTS = 5',
            'MAX_ATTEMPTS = 10'
        ).replace(
            'DELAY_BETWEEN_ATTEMPTS = 5',
            'DELAY_BETWEEN_ATTEMPTS = 45'
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        agents_created += 1
        print(f"Created {filename} for booking {booking_id}")
    
    # Create 3A-3Z agents for first booking ID (second round)
    booking_id = "6339614781"
    for i in range(26):
        letter = chr(ord('A') + i)
        filename = f"boss_ai_playwright_3{letter}.py"
        
        modified_content = original_content.replace(
            'BOOKING_CONFIRMATION = "6160911170"',
            f'BOOKING_CONFIRMATION = "{booking_id}"'
        ).replace(
            'AGENT_NAME = "PRIMARY"',
            f'AGENT_NAME = "3{letter}"'
        ).replace(
            'MAX_ATTEMPTS = 5',
            'MAX_ATTEMPTS = 10'
        ).replace(
            'DELAY_BETWEEN_ATTEMPTS = 5',
            'DELAY_BETWEEN_ATTEMPTS = 45'
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        agents_created += 1
        print(f"Created {filename} for booking {booking_id}")
    
    print(f"\n🎯 SMART AGENT CREATION COMPLETE!")
    print(f"📊 Total agents created: {agents_created}")
    print(f"📋 Distribution:")
    print(f"   • A-Z: 6339614781 (26 agents)")
    print(f"   • 1A-1Z: 6763779197 (26 agents)")
    print(f"   • 2A-2Z: 6763734263 (26 agents)")
    print(f"   • 3A-3Z: 6339614781 (26 agents)")
    print(f"📈 Total capacity: {agents_created * 10} PIN attempts")
    print(f"⏱️ Timing: 45 seconds between attempts per agent")
    print(f"🎯 Strategy: Distributed load, human-like timing")

if __name__ == "__main__":
    create_agent_files()
