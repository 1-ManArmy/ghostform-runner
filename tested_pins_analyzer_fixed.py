"""
PROFESSOR JOHNNY'S TESTED PINS ANALYZER
Creates 4 separate files - one for each agent's tested PINs
Perfect for tracking what each specialist has covered!
"""

import csv
import os
from collections import defaultdict
from datetime import datetime

def analyze_agent_tested_pins():
    """Analyze each agent's tested PINs and create separate files"""
    
    print("PROFESSOR JOHNNY'S PIN TRACKING SYSTEM")
    print("=" * 60)
    
    # Agent configurations
    agents = {
        "A": {
            "name": "ALPHA_SPECIALIST", 
            "booking_id": "6339614781",
            "target_pins": [
                "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
                "4039", "8652", "1790", "7943", "6005", "9102", "2384", 
                "7349", "8217", "9558", "1332", "4206", "7581", "3018", 
                "6440", "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
                "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
                "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
                "8479", "3724"
            ],
            "csv_file": "agent_A_results.csv"
        },
        "B": {
            "name": "BRAVO_SPECIALIST",
            "booking_id": "6860261353", 
            "target_pins": [
                "2540", "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
                "4039", "2745", "8652", "1790", "7943", "6005", "9102", "2384", 
                "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
                "6440", "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
                "5672", "7469", "2903", "1881", "4727", "3156", "9317",
                "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
                "8479", "3724"
            ],
            "csv_file": "agent_B_results.csv"
        },
        "C": {
            "name": "CHARLIE_SPECIALIST",
            "booking_id": "6160911170",
            "target_pins": [
                "2540", "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
                "4039", "2745", "8652", "1790", "7943", "6005", "9102", 
                "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
                "6440", "5421", "3975", "7033", "8751", "1094", 
                "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
                "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
                "8479"
            ],
            "csv_file": "agent_C_results.csv"
        },
        "D": {
            "name": "DELTA_SPECIALIST",
            "booking_id": "5830944764",
            "target_pins": [
                "2540", "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
                "4039", "2745", "8652", "1790", "7943", "6005", "9102", "2384", 
                "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
                "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
                "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
                "1517", "4490", "2586", "6048", "1394", "7635", "2981", 
                "8479", "3724"
            ],
            "csv_file": "agent_D_results.csv"
        }
    }
    
    # Analyze each agent
    for agent_letter, agent_info in agents.items():
        print(f"\nANALYZING AGENT {agent_letter} - {agent_info['name']}")
        print("-" * 50)
        
        tested_pins = set()
        success_pins = []
        total_tests = 0
        
        # Read agent's CSV file if it exists
        csv_file = agent_info['csv_file']
        if os.path.exists(csv_file):
            print(f"Reading: {csv_file}")
            try:
                with open(csv_file, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 4:
                            pin = row[3] if len(row) > 3 else ""
                            status = row[4] if len(row) > 4 else ""
                            booking_id = row[2] if len(row) > 2 else ""
                            
                            # Only count pins for this agent's booking ID
                            if booking_id == agent_info['booking_id'] and pin.isdigit() and len(pin) == 4:
                                tested_pins.add(pin)
                                total_tests += 1
                                if status == "SUCCESS":
                                    success_pins.append(pin)
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
        else:
            print(f"CSV file not found: {csv_file}")
        
        # Find which target pins were actually tested
        target_pins_set = set(agent_info['target_pins'])
        actually_tested = tested_pins.intersection(target_pins_set)
        not_tested_yet = target_pins_set - tested_pins
        
        print(f"Target booking ID: {agent_info['booking_id']}")
        print(f"Target PINs assigned: {len(agent_info['target_pins'])}")
        print(f"Actually tested: {len(actually_tested)}")
        print(f"Not tested yet: {len(not_tested_yet)}")
        print(f"Success PINs: {len(success_pins)}")
        
        # Create individual agent file
        filename = f"AGENT_{agent_letter}_TESTED_PINS.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"AGENT {agent_letter} - {agent_info['name']} TESTED PINS\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Target Booking ID: {agent_info['booking_id']}\n")
            f.write(f"Agent Mission: Test {len(agent_info['target_pins'])} strategic PINs\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("TESTING STATISTICS:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Target PINs assigned: {len(agent_info['target_pins'])}\n")
            f.write(f"Actually tested: {len(actually_tested)}\n")
            f.write(f"Not tested yet: {len(not_tested_yet)}\n")
            f.write(f"Success PINs found: {len(success_pins)}\n")
            f.write(f"Testing completion: {(len(actually_tested)/len(agent_info['target_pins'])*100):.1f}%\n\n")
            
            if success_pins:
                f.write("SUCCESS PINS FOUND:\n")
                f.write("-" * 20 + "\n")
                for pin in success_pins:
                    f.write(f"   SUCCESS: {pin}\n")
                f.write("\n")
            
            if actually_tested:
                f.write("TESTED PINS (sorted):\n")
                f.write("-" * 25 + "\n")
                sorted_tested = sorted(list(actually_tested))
                for i in range(0, len(sorted_tested), 10):
                    row_pins = sorted_tested[i:i+10]
                    f.write(f"   {', '.join(row_pins)}\n")
                f.write("\n")
            
            if not_tested_yet:
                f.write("NOT TESTED YET (remaining targets):\n")
                f.write("-" * 35 + "\n")
                sorted_remaining = sorted(list(not_tested_yet))
                for i in range(0, len(sorted_remaining), 10):
                    row_pins = sorted_remaining[i:i+10]
                    f.write(f"   {', '.join(row_pins)}\n")
                f.write("\n")
            
            f.write("ORIGINAL TARGET PIN LIST:\n")
            f.write("-" * 30 + "\n")
            target_pins = agent_info['target_pins']
            for i in range(0, len(target_pins), 10):
                row_pins = target_pins[i:i+10]
                f.write(f"   {', '.join(row_pins)}\n")
        
        print(f"Created: {filename}")
    
    print(f"\nANALYSIS COMPLETE!")
    print("Created 4 separate files:")
    print("   AGENT_A_TESTED_PINS.txt")
    print("   AGENT_B_TESTED_PINS.txt") 
    print("   AGENT_C_TESTED_PINS.txt")
    print("   AGENT_D_TESTED_PINS.txt")
    
    print(f"\nReady for Professor's LUCKY 50 PINS!")

if __name__ == "__main__":
    analyze_agent_tested_pins()
