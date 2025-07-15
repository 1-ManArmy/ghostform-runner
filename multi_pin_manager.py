#!/usr/bin/env python3
"""
Multi-Booking PIN Manager - Handles multiple booking IDs with smart distribution
"""

import json
import os
import random
import threading
from datetime import datetime

class MultiBookingPinManager:
    def __init__(self):
        self.booking_ids = [
            "6339614781",
            "6763779197", 
            "6763734263"
        ]
        self.managers = {}
        self.lock = threading.Lock()
        
        # Initialize individual PIN managers
        for booking_id in self.booking_ids:
            self.managers[booking_id] = PinManager(booking_id)
    
    def get_manager(self, booking_id):
        """Get PIN manager for specific booking ID"""
        return self.managers.get(booking_id)
    
    def get_combined_stats(self):
        """Get combined statistics across all booking IDs"""
        combined_stats = {
            'total_pins_tried': 0,
            'total_attempts': 0,
            'success_bookings': [],
            'active_bookings': [],
            'booking_stats': {}
        }
        
        for booking_id, manager in self.managers.items():
            stats = manager.get_stats()
            pins_tried = len(stats.get('used_pins', []))
            attempts = stats.get('total_attempts', 0)
            
            combined_stats['total_pins_tried'] += pins_tried
            combined_stats['total_attempts'] += attempts
            
            combined_stats['booking_stats'][booking_id] = {
                'pins_tried': pins_tried,
                'attempts': attempts,
                'success_pin': manager.get_success_pin()
            }
            
            if manager.get_success_pin():
                combined_stats['success_bookings'].append(booking_id)
            else:
                combined_stats['active_bookings'].append(booking_id)
        
        return combined_stats
    
    def check_any_success(self):
        """Check if any booking ID has found success"""
        for manager in self.managers.values():
            if manager.get_success_pin():
                return True
        return False
    
    def get_success_results(self):
        """Get all successful results"""
        results = {}
        for booking_id, manager in self.managers.items():
            success_pin = manager.get_success_pin()
            if success_pin:
                results[booking_id] = success_pin
        return results

class PinManager:
    def __init__(self, booking_id):
        self.booking_id = booking_id
        self.data_file = f"pin_manager_{booking_id}.json"
        self.log_file = f"unified_log_{booking_id}.txt"
        self.lock = threading.Lock()
        
        # Load existing data
        self.data = self._load_data()
    
    def _load_data(self):
        """Load existing PIN data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'used_pins': [],
            'success_pin': None,
            'total_attempts': 0,
            'agents_used': [],
            'last_updated': None
        }
    
    def _save_data(self):
        """Save PIN data"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_next_pin(self, agent_name):
        """Get next available PIN for agent"""
        with self.lock:
            # Check if already found success
            if self.data.get('success_pin'):
                return None
            
            # Generate random PIN not in used list
            used_pins = set(self.data['used_pins'])
            
            # Try to get a random PIN
            max_attempts = 100
            for _ in range(max_attempts):
                pin = f"{random.randint(0, 9999):04d}"
                if pin not in used_pins:
                    self.data['used_pins'].append(pin)
                    if agent_name not in self.data['agents_used']:
                        self.data['agents_used'].append(agent_name)
                    self._save_data()
                    return pin
            
            return None
    
    def record_result(self, agent_name, pin, result):
        """Record PIN attempt result"""
        with self.lock:
            self.data['total_attempts'] += 1
            
            # Log to unified log file
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp},{self.booking_id},{agent_name},{pin},{result},https://secure.booking.com/help/confirmation_pin_auth\n"
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            # If success, record it
            if result == 'SUCCESS':
                self.data['success_pin'] = pin
                print(f"🎉 SUCCESS! PIN {pin} found for booking {self.booking_id} by agent {agent_name}")
            
            self._save_data()
    
    def get_success_pin(self):
        """Get success PIN if found"""
        return self.data.get('success_pin')
    
    def get_stats(self):
        """Get statistics"""
        return {
            'used_pins': self.data['used_pins'],
            'success_pin': self.data.get('success_pin'),
            'total_attempts': self.data['total_attempts'],
            'agents_used': self.data['agents_used'],
            'pins_tried': len(self.data['used_pins']),
            'remaining_pins': 10000 - len(self.data['used_pins'])
        }

def get_pin_manager(booking_id=None):
    """Get PIN manager instance"""
    if booking_id:
        return PinManager(booking_id)
    else:
        return MultiBookingPinManager()

if __name__ == "__main__":
    # Test multi-booking manager
    multi_manager = MultiBookingPinManager()
    stats = multi_manager.get_combined_stats()
    
    print("📊 MULTI-BOOKING PIN MANAGER STATUS")
    print("="*50)
    
    for booking_id, booking_stats in stats['booking_stats'].items():
        print(f"📋 Booking {booking_id}:")
        print(f"   🎯 PINs tried: {booking_stats['pins_tried']}")
        print(f"   📊 Attempts: {booking_stats['attempts']}")
        if booking_stats['success_pin']:
            print(f"   ✅ SUCCESS PIN: {booking_stats['success_pin']}")
        else:
            print(f"   🔍 Still searching...")
        print()
    
    print(f"🎯 TOTAL PINS TRIED: {stats['total_pins_tried']}")
    print(f"📊 TOTAL ATTEMPTS: {stats['total_attempts']}")
    print(f"✅ SUCCESS BOOKINGS: {len(stats['success_bookings'])}")
    print(f"🔍 ACTIVE BOOKINGS: {len(stats['active_bookings'])}")
