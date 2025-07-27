#!/usr/bin/env python3
"""
🎯 PIN Manager - Generate and Distribute 2000 Unique PINs
Assigns 2 unique PINs to each of 1000 agents with tracking
"""

import json
import random
import os
import re

class PINManager:
    def __init__(self):
        self.pin_allocation_file = "pin_allocation_master.json"
        self.used_pins_file = "used_pins_tracker.json"
        self.agent_count = 1000
        self.pins_per_agent = 2
        self.total_pins_needed = self.agent_count * self.pins_per_agent  # 2000
        
    def generate_unique_pins(self, count=2000):
        """Generate unique 4-digit PIN codes"""
        print(f"🎯 Generating {count} unique PIN codes...")
        
        # Generate all possible 4-digit PINs (0000-9999)
        all_possible_pins = [f"{i:04d}" for i in range(10000)]
        
        # Randomly select unique PINs
        unique_pins = random.sample(all_possible_pins, count)
        
        print(f"✅ Generated {len(unique_pins)} unique PINs")
        return sorted(unique_pins)
    
    def create_pin_allocation(self):
        """Create PIN allocation for all 1000 agents"""
        print("🔧 Creating PIN allocation for 1000 agents...")
        
        # Generate 2000 unique PINs
        all_pins = self.generate_unique_pins(self.total_pins_needed)
        
        # Create allocation structure
        allocation = {
            "metadata": {
                "total_agents": self.agent_count,
                "pins_per_agent": self.pins_per_agent,
                "total_pins": len(all_pins),
                "generated_at": "2025-07-21",
                "booking_id": "6160911170"
            },
            "agent_pins": {},
            "all_pins_list": all_pins,
            "used_pins": [],
            "remaining_pins": all_pins.copy()
        }
        
        # Assign 2 PINs to each agent
        pin_index = 0
        for agent_num in range(1, self.agent_count + 1):
            agent_pins = [all_pins[pin_index], all_pins[pin_index + 1]]
            allocation["agent_pins"][f"agent_{agent_num}"] = {
                "agent_file": f"boss_ai_playwright_pin{agent_num}.py",
                "pins": agent_pins,
                "status": "assigned",
                "tested": False,
                "results": {}
            }
            pin_index += 2
        
        # Save allocation
        with open(self.pin_allocation_file, 'w') as f:
            json.dump(allocation, f, indent=2)
        
        print(f"✅ PIN allocation saved to {self.pin_allocation_file}")
        return allocation
    
    def update_agent_files(self, allocation):
        """Update all agent files with their assigned PINs"""
        print("🔄 Updating agent files with assigned PINs...")
        
        updated_count = 0
        for agent_num in range(1, self.agent_count + 1):
            agent_file = f"boss_ai_playwright_pin{agent_num}.py"
            agent_key = f"agent_{agent_num}"
            
            if os.path.exists(agent_file) and agent_key in allocation["agent_pins"]:
                agent_pins = allocation["agent_pins"][agent_key]["pins"]
                pins_string = ",".join(agent_pins)
                
                try:
                    # Read the file
                    with open(agent_file, 'r') as f:
                        content = f.read()
                    
                    # Update the default pins argument
                    # Look for the pattern: default="2847,1965"
                    pattern = r'default="[^"]*"'
                    replacement = f'default="{pins_string}"'
                    
                    updated_content = re.sub(pattern, replacement, content)
                    
                    # Write back to file
                    with open(agent_file, 'w') as f:
                        f.write(updated_content)
                    
                    updated_count += 1
                    
                    if agent_num <= 5 or agent_num % 100 == 0:  # Show progress for first 5 and every 100th
                        print(f"✅ Updated {agent_file} with PINs: {pins_string}")
                
                except Exception as e:
                    print(f"❌ Error updating {agent_file}: {e}")
        
        print(f"🎉 Successfully updated {updated_count} agent files!")
        return updated_count
    
    def create_pin_summary(self, allocation):
        """Create a summary file for easy reference"""
        summary = {
            "summary": {
                "total_agents": len(allocation["agent_pins"]),
                "total_pins": len(allocation["all_pins_list"]),
                "pins_per_agent": self.pins_per_agent,
                "booking_id": allocation["metadata"]["booking_id"]
            },
            "pin_ranges": {
                "first_10_pins": allocation["all_pins_list"][:10],
                "last_10_pins": allocation["all_pins_list"][-10:],
                "sample_agents": {}
            }
        }
        
        # Add sample of first 10 agents
        for i in range(1, 11):
            agent_key = f"agent_{i}"
            if agent_key in allocation["agent_pins"]:
                summary["pin_ranges"]["sample_agents"][f"agent_{i}"] = allocation["agent_pins"][agent_key]["pins"]
        
        with open("pin_allocation_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("✅ PIN allocation summary saved to pin_allocation_summary.json")
    
    def verify_allocation(self, allocation):
        """Verify the PIN allocation is correct"""
        print("🔍 Verifying PIN allocation...")
        
        all_assigned_pins = []
        for agent_key, agent_data in allocation["agent_pins"].items():
            all_assigned_pins.extend(agent_data["pins"])
        
        # Check for duplicates
        unique_assigned = set(all_assigned_pins)
        
        print(f"📊 Verification Results:")
        print(f"   Total agents: {len(allocation['agent_pins'])}")
        print(f"   Total assigned PINs: {len(all_assigned_pins)}")
        print(f"   Unique assigned PINs: {len(unique_assigned)}")
        print(f"   Expected total: {self.total_pins_needed}")
        
        if len(all_assigned_pins) == len(unique_assigned) == self.total_pins_needed:
            print("✅ VERIFICATION PASSED! No duplicates found.")
            return True
        else:
            print("❌ VERIFICATION FAILED! Duplicates or missing PINs detected.")
            return False
    
    def run_complete_setup(self):
        """Run the complete PIN allocation setup"""
        print("🚀 Starting Complete PIN Allocation Setup")
        print("=" * 60)
        
        # Step 1: Create allocation
        allocation = self.create_pin_allocation()
        
        # Step 2: Verify allocation
        if not self.verify_allocation(allocation):
            print("❌ Setup failed - allocation verification failed")
            return False
        
        # Step 3: Update agent files
        updated_count = self.update_agent_files(allocation)
        
        # Step 4: Create summary
        self.create_pin_summary(allocation)
        
        print("=" * 60)
        print("🎉 PIN ALLOCATION SETUP COMPLETE!")
        print(f"✅ {updated_count} agent files updated")
        print(f"✅ 2000 unique PINs allocated")
        print(f"✅ No duplicates guaranteed")
        print(f"✅ Tracking files created")
        print("=" * 60)
        
        return True

if __name__ == "__main__":
    manager = PINManager()
    manager.run_complete_setup()
