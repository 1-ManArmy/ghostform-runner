#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 PIN SYNCHRONIZATION SYSTEM
Synchronize PINs across corresponding agents (A1-B1-C1-D1 same PINs, A2-B2-C2-D2 same PINs, etc.)
This ensures each PIN is tested against all 4 booking IDs for maximum coverage
"""

import os
import re
import json

def extract_pins_from_agent(filepath):
    """Extract PIN list from an agent file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the PINS line
        pin_pattern = r"PINS = \['(\d{4})', '(\d{4})', '(\d{4})', '(\d{4})', '(\d{4})'\]"
        match = re.search(pin_pattern, content)
        
        if match:
            return [match.group(i) for i in range(1, 6)]
        else:
            print(f"⚠️ Could not extract PINs from {filepath}")
            return None
            
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def update_pins_in_agent(filepath, new_pins, batch, agent_num):
    """Update PINs in an agent file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update PINS line
        old_pins_pattern = r"PINS = \['(\d{4})', '(\d{4})', '(\d{4})', '(\d{4})', '(\d{4})'\]"
        new_pins_line = f"PINS = ['{new_pins[0]}', '{new_pins[1]}', '{new_pins[2]}', '{new_pins[3]}', '{new_pins[4]}']"
        
        updated_content = re.sub(old_pins_pattern, new_pins_line, content)
        
        # Update the print statement with new PINs
        pins_str = ", ".join(new_pins)
        old_print_pattern = r'print\(f"🔑 Assigned PINs: [^"]+"\)'
        new_print_line = f'print(f"🔑 Assigned PINs: {pins_str}")'
        
        updated_content = re.sub(old_print_pattern, new_print_line, updated_content)
        
        # Write back updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    print("🔄 PIN SYNCHRONIZATION ACROSS CORRESPONDING AGENTS")
    print("📌 Making A1-B1-C1-D1 test same PINs, A2-B2-C2-D2 test same PINs, etc.")
    print("=" * 70)
    
    batches = ['A', 'B', 'C', 'D']
    pin_assignments = {}
    
    # First, extract PINs from all A batch agents (they will be the master)
    print("📋 Extracting PIN assignments from Batch A (master batch)...")
    for i in range(1, 101):
        agent_num = f"{i:03d}"
        filepath = f"agent_{agent_num}A.py"
        
        if os.path.exists(filepath):
            pins = extract_pins_from_agent(filepath)
            if pins:
                pin_assignments[agent_num] = pins
                print(f"📝 Agent {agent_num}: {', '.join(pins)}")
            else:
                print(f"❌ Failed to extract PINs from {filepath}")
        else:
            print(f"⚠️ File not found: {filepath}")
    
    print(f"\n✅ Extracted {len(pin_assignments)} PIN assignments from Batch A")
    
    # Now synchronize B, C, D batches with A batch PINs
    synchronized_count = 0
    error_count = 0
    
    for batch in ['B', 'C', 'D']:
        print(f"\n🔄 Synchronizing Batch {batch} with Batch A PINs...")
        
        for agent_num, pins in pin_assignments.items():
            filepath = f"agent_{agent_num}{batch}.py"
            
            if os.path.exists(filepath):
                if update_pins_in_agent(filepath, pins, batch, agent_num):
                    print(f"✅ Synchronized {filepath}: {', '.join(pins)}")
                    synchronized_count += 1
                else:
                    print(f"❌ Failed to synchronize {filepath}")
                    error_count += 1
            else:
                print(f"⚠️ File not found: {filepath}")
                error_count += 1
    
    print(f"\n🎉 PIN SYNCHRONIZATION COMPLETE!")
    print(f"✅ Synchronized agents: {synchronized_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total A batch agents: {len(pin_assignments)}")
    
    # Verify synchronization with sample check
    print(f"\n🔍 VERIFICATION SAMPLE:")
    sample_agents = ['001', '025', '050', '075', '100']
    
    for agent_num in sample_agents:
        pins_by_batch = {}
        for batch in batches:
            filepath = f"agent_{agent_num}{batch}.py"
            if os.path.exists(filepath):
                pins = extract_pins_from_agent(filepath)
                if pins:
                    pins_by_batch[batch] = pins
        
        if len(pins_by_batch) == 4:
            # Check if all batches have same PINs
            first_pins = list(pins_by_batch.values())[0]
            all_same = all(pins == first_pins for pins in pins_by_batch.values())
            
            if all_same:
                print(f"✅ Agent {agent_num}: {', '.join(first_pins)} (ALL BATCHES SYNCHRONIZED)")
            else:
                print(f"❌ Agent {agent_num}: MISMATCH DETECTED")
                for batch, pins in pins_by_batch.items():
                    print(f"   {batch}: {', '.join(pins)}")
        else:
            print(f"⚠️ Agent {agent_num}: Missing files")

if __name__ == "__main__":
    main()
