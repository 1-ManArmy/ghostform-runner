import json
import random
import os
import time
from pathlib import Path

# Central PIN management system
class PinManager:
    def __init__(self, booking_id):
        self.booking_id = booking_id
        self.data_file = f"pin_manager_{booking_id}.json"
        self.log_file = f"unified_log_{booking_id}.txt"
        self.data = self.load_data()
    
    def load_data(self):
        """Load existing data or create new"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "booking_id": self.booking_id,
            "tried_pins": [],
            "success_pin": None,
            "total_attempts": 0,
            "agents_used": []
        }
    
    def save_data(self):
        """Save data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_random_pins(self, agent_name, count=5):
        """Get 5 random unique PINs that haven't been tried"""
        if self.data["success_pin"]:
            return []  # Already found success
        
        # Generate all possible 4-digit PINs
        all_pins = [f"{i:04d}" for i in range(0, 10000)]
        tried_pins = set(self.data["tried_pins"])
        available_pins = [pin for pin in all_pins if pin not in tried_pins]
        
        if len(available_pins) < count:
            count = len(available_pins)
        
        if count == 0:
            return []
        
        # Get random PINs
        selected_pins = random.sample(available_pins, count)
        
        # Mark as tried
        self.data["tried_pins"].extend(selected_pins)
        self.data["agents_used"].append({
            "agent": agent_name,
            "pins": selected_pins,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        self.save_data()
        return selected_pins
    
    def log_result(self, agent_name, pin, result, url):
        """Log result to unified log file"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp},{self.booking_id},{agent_name},{pin},{result},{url}\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        # Update data
        self.data["total_attempts"] += 1
        if result == "SUCCESS":
            self.data["success_pin"] = pin
        
        self.save_data()
    
    def is_success_found(self):
        """Check if success was already found"""
        return self.data["success_pin"] is not None
    
    def get_stats(self):
        """Get current statistics"""
        return {
            "booking_id": self.booking_id,
            "total_pins_tried": len(self.data["tried_pins"]),
            "total_attempts": self.data["total_attempts"],
            "success_pin": self.data["success_pin"],
            "agents_used": len(self.data["agents_used"]),
            "remaining_pins": 10000 - len(self.data["tried_pins"])
        }

# Global PIN manager instance
pin_manager = None

def get_pin_manager(booking_id):
    """Get or create PIN manager for booking ID"""
    global pin_manager
    if pin_manager is None or pin_manager.booking_id != booking_id:
        pin_manager = PinManager(booking_id)
    return pin_manager
