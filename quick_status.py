#!/usr/bin/env python3
"""
Quick Status Display
"""

import json
import os
from datetime import datetime

def quick_status():
    """Get quick status of the production system"""
    booking_id = "6160911170"
    
    # Read PIN manager data
    data_file = f"pin_manager_{booking_id}.json"
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
            pins_tried = len(data.get('used_pins', []))
            remaining = 10000 - pins_tried
            progress = (pins_tried / 10000) * 100
            
            print(f"📊 QUICK STATUS - Booking: {booking_id}")
            print(f"🎯 PINs Tried: {pins_tried:,}")
            print(f"📋 Remaining: {remaining:,}")
            print(f"📈 Progress: {progress:.2f}%")
            print(f"🕐 Last Check: {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 50)
            
            # Check for success PIN
            if data.get('success_pin'):
                print(f"✅ SUCCESS PIN FOUND: {data['success_pin']}")
            else:
                print("🔍 Still searching...")
    else:
        print(f"❌ No data file found for booking: {booking_id}")

if __name__ == "__main__":
    quick_status()
