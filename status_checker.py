import os
import json
from datetime import datetime

CONFIRMATION = "6339614781"

def check_status():
    """Check the current status of the PIN hunting"""
    print("🔍 PIN HUNTER STATUS CHECK")
    print("="*50)
    
    # Check if success found
    if os.path.exists(f"SUCCESS_FOUND_{CONFIRMATION}.json"):
        with open(f"SUCCESS_FOUND_{CONFIRMATION}.json", 'r') as f:
            success_data = json.load(f)
        print("🎉 SUCCESS FOUND!")
        print(f"✅ Correct PIN: {success_data['success_pin']}")
        print(f"🤖 Found by: {success_data['agent']}")
        print(f"⏱️ Timestamp: {success_data['timestamp']}")
        print(f"📊 Attempt number: {success_data['attempt_number']}")
        return True
    
    # Check log file for progress
    log_file = f"auto_hunt_log_{CONFIRMATION}.txt"
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        total_attempts = len(lines)
        print(f"📊 Total attempts so far: {total_attempts}")
        
        if lines:
            # Show last few attempts
            print("\n🔄 Recent attempts:")
            for line in lines[-5:]:
                parts = line.strip().split(',')
                if len(parts) >= 7:
                    timestamp = parts[0]
                    pin = parts[3]
                    result = parts[4]
                    attempt = parts[6]
                    print(f"  {timestamp} - {attempt} - PIN {pin}: {result}")
        
        # Check if still running
        if lines:
            last_line = lines[-1]
            parts = last_line.strip().split(',')
            if len(parts) >= 1:
                last_timestamp = parts[0]
                print(f"\n⏰ Last activity: {last_timestamp}")
    else:
        print("❌ No log file found - hunter may not have started yet")
    
    print("\n🎯 Status: HUNTING IN PROGRESS...")
    return False

if __name__ == "__main__":
    check_status()
