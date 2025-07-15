#!/usr/bin/env python3
"""
Test PIN distribution script - ensures PIN 1965 is assigned to agent C or D
"""
import json
import random
import os
from pin_manager import get_pin_manager

def setup_test_pins():
    """Set up test scenario with 54 unique PINs, ensuring 1965 goes to agent C or D"""
    booking_id = "5871858498"
    
    # Clear any existing data
    pin_mgr = get_pin_manager(booking_id)
    if os.path.exists(pin_mgr.data_file):
        os.remove(pin_mgr.data_file)
    if os.path.exists(pin_mgr.log_file):
        os.remove(pin_mgr.log_file)
    
    # Recreate pin manager
    pin_mgr = get_pin_manager(booking_id)
    
    # Generate 54 unique random PINs (excluding 1965 for now)
    all_pins = [f"{i:04d}" for i in range(0, 10000) if i != 1965]
    test_pins = random.sample(all_pins, 53)  # 53 random + 1965 = 54 total
    
    # Add 1965 to the list
    test_pins.append("1965")
    
    # Shuffle to randomize
    random.shuffle(test_pins)
    
    # Agents list
    agents = ["PRIMARY"] + [chr(65 + i) for i in range(26)]  # PRIMARY, A, B, C, ..., Z
    
    # Distribute PINs: 2 per agent
    agent_pins = {}
    for i, agent in enumerate(agents):
        start_idx = i * 2
        end_idx = start_idx + 2
        agent_pins[agent] = test_pins[start_idx:end_idx]
    
    # Ensure 1965 is in agent C or D
    pin_1965_agent = None
    for agent, pins in agent_pins.items():
        if "1965" in pins:
            pin_1965_agent = agent
            break
    
    # If 1965 is not in C or D, swap it
    if pin_1965_agent not in ["C", "D"]:
        # Find agent C or D and swap one of their PINs with 1965
        target_agent = "C" if random.choice([True, False]) else "D"
        
        # Swap first PIN of target agent with 1965
        other_agent_pins = agent_pins[pin_1965_agent]
        target_agent_pins = agent_pins[target_agent]
        
        # Find 1965 in other agent and swap
        pin_1965_idx = other_agent_pins.index("1965")
        pin_to_swap = target_agent_pins[0]
        
        other_agent_pins[pin_1965_idx] = pin_to_swap
        target_agent_pins[0] = "1965"
        
        pin_1965_agent = target_agent
    
    print(f"🎯 Test Setup Complete!")
    print(f"📋 Booking ID: {booking_id}")
    print(f"🔢 Total PINs: 54 (27 agents × 2 PINs each)")
    print(f"✅ Correct PIN '1965' assigned to Agent {pin_1965_agent}")
    print(f"📊 PIN distribution:")
    
    for agent, pins in agent_pins.items():
        indicator = "🎯" if "1965" in pins else "  "
        print(f"  {indicator} Agent {agent:8}: {pins}")
    
    return agent_pins, pin_1965_agent

def create_test_pin_manager(agent_pins):
    """Create a custom PIN manager with pre-assigned PINs"""
    booking_id = "5871858498"
    
    class TestPinManager:
        def __init__(self):
            self.booking_id = booking_id
            self.data_file = f"pin_manager_{booking_id}.json"
            self.log_file = f"unified_log_{booking_id}.txt"
            self.agent_pins = agent_pins
            self.used_agents = set()
            self.success_found = False
            self.success_pin = None
            self.data = {
                "booking_id": booking_id,
                "tried_pins": [],
                "success_pin": None,
                "total_attempts": 0,
                "agents_used": []
            }
        
        def get_random_pins(self, agent_name, count=2):
            """Get pre-assigned PINs for the agent"""
            if self.success_found:
                return []
            
            if agent_name in self.used_agents:
                return []  # Agent already used
            
            if agent_name not in self.agent_pins:
                return []  # Agent not in test
            
            pins = self.agent_pins[agent_name]
            self.used_agents.add(agent_name)
            
            # Add to tried pins
            self.data["tried_pins"].extend(pins)
            self.data["agents_used"].append({
                "agent": agent_name,
                "pins": pins,
                "timestamp": "TEST_RUN"
            })
            
            return pins
        
        def log_result(self, agent_name, pin, result, url):
            """Log result and check for success"""
            timestamp = "2025-07-15 TEST_RUN"
            log_entry = f"{timestamp},{self.booking_id},{agent_name},{pin},{result},{url}\n"
            
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
            
            self.data["total_attempts"] += 1
            
            if result == "SUCCESS":
                self.success_found = True
                self.success_pin = pin
                self.data["success_pin"] = pin
                print(f"🎉 SUCCESS! PIN {pin} found by Agent {agent_name}")
        
        def is_success_found(self):
            """Check if success was found"""
            return self.success_found
        
        def get_stats(self):
            """Get current statistics"""
            return {
                "booking_id": self.booking_id,
                "total_pins_tried": len(self.data["tried_pins"]),
                "total_attempts": self.data["total_attempts"],
                "success_pin": self.success_pin,
                "agents_used": len(self.data["agents_used"]),
                "remaining_pins": 54 - len(self.data["tried_pins"])
            }
    
    return TestPinManager()

if __name__ == "__main__":
    agent_pins, pin_1965_agent = setup_test_pins()
    
    # Create test configuration file
    test_config = {
        "booking_id": "5871858498",
        "agent_pins": agent_pins,
        "correct_pin_agent": pin_1965_agent,
        "total_pins": 54,
        "pins_per_agent": 2
    }
    
    with open("test_config.json", "w") as f:
        json.dump(test_config, f, indent=2)
    
    print(f"\n📁 Test configuration saved to: test_config.json")
    print(f"🚀 Ready to run test with: python run_test.py")
