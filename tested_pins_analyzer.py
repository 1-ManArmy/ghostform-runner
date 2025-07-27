"""
🎯 TESTED PINS ANALYZER
Collecting all PINs tested by our 4 specialist agents
Professor Johnny wants to see what we've covered before trying LUCK! 🍀
"""

import csv
import os
from collections import defaultdict
import glob

def analyze_tested_pins():
    """Analyze all CSV files to extract tested PINs by booking ID"""
    
    # Our 4 target booking IDs
    BOOKING_IDS = {
        "A": "6339614781",  # Agent A target  
        "B": "6860261353",  # Agent B target
        "C": "6160911170",  # Agent C target  
        "D": "5830944764"   # Agent D target
    }
    
    # Files to check
    result_files = [
        'agent_A_results.csv',
        'agent_B_results.csv', 
        'agent_C_results.csv',
        'agent_D_results.csv',
        'mission_log_A.csv',
        'mission_log_B.csv',
        'mission_log_C.csv', 
        'mission_log_D.csv',
        'skipped_pins_recovery.csv',
        'mission_results.csv',
        'auto_army_results.csv'
    ]
    
    # Also check for any CSV files in directory
    all_csv_files = glob.glob("*.csv")
    result_files.extend(all_csv_files)
    result_files = list(set(result_files))  # Remove duplicates
    
    tested_pins = defaultdict(set)
    success_pins = defaultdict(list)
    total_tests = defaultdict(int)
    all_tested_pins = set()
    
    print("🔍 ANALYZING ALL TEST RESULTS...")
    print("=" * 60)
    
    # Read all CSV files
    for filename in result_files:
        if os.path.exists(filename):
            print(f"📊 Reading: {filename}")
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                    reader = csv.reader(file)
                    row_count = 0
                    for row in reader:
                        row_count += 1
                        if len(row) >= 3:
                            # Try different column positions for PIN data
                            for i, cell in enumerate(row):
                                if cell.isdigit() and len(cell) == 4:
                                    pin = cell
                                    all_tested_pins.add(pin)
                                    
                                    # Try to find booking ID in same row
                                    booking_id = ""
                                    for j, booking_cell in enumerate(row):
                                        if booking_cell.isdigit() and len(booking_cell) >= 8:
                                            booking_id = booking_cell
                                            break
                                    
                                    # Match to our target booking IDs
                                    for agent, target_id in BOOKING_IDS.items():
                                        if booking_id == target_id:
                                            tested_pins[agent].add(pin)
                                            total_tests[agent] += 1
                                            
                                            # Check for success status
                                            if len(row) > i+1 and "SUCCESS" in str(row[i+1]).upper():
                                                success_pins[agent].append(pin)
                                    break
                    
                    print(f"   📄 Processed {row_count} rows")
                    
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
        else:
            print(f"⚠️ File not found: {filename}")
    
    return tested_pins, success_pins, total_tests, BOOKING_IDS, all_tested_pins

def get_predefined_tested_pins():
    """Get PINs we know were tested from our agent configurations"""
    
    # From our agent specialist files - these are the PINs each agent tested
    agent_pins = {
        "A": [  # Agent A tested these 47 PINs
            "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
            "4039", "8652", "1790", "7943", "6005", "9102", "2384", 
            "7349", "8217", "9558", "1332", "4206", "7581", "3018", 
            "6440", "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
            "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
            "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
            "8479", "3724"
        ],
        "B": [  # Agent B tested these 49 PINs
            "2540", "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
            "4039", "2745", "8652", "1790", "7943", "6005", "9102", "2384", 
            "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
            "6440", "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
            "5672", "7469", "2903", "1881", "4727", "3156", "9317",
            "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
            "8479", "3724"
        ],
        "C": [  # Agent C tested these 46 PINs
            "2540", "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
            "4039", "2745", "8652", "1790", "7943", "6005", "9102", 
            "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
            "6440", "5421", "3975", "7033", "8751", "1094", 
            "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
            "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
            "8479"
        ],
        "D": [  # Agent D tested these 48 PINs
            "2540", "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
            "4039", "2745", "8652", "1790", "7943", "6005", "9102", "2384", 
            "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
            "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
            "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
            "1517", "4490", "2586", "6048", "1394", "7635", "2981", 
            "8479", "3724"
        ]
    }
    
    # Combine all tested PINs
    all_tested = set()
    for agent, pins in agent_pins.items():
        all_tested.update(pins)
    
    return agent_pins, all_tested

def display_comprehensive_report():
    """Display comprehensive analysis of tested PINs"""
    
    # Get data from CSV files
    tested_pins, success_pins, total_tests, booking_ids, csv_tested = analyze_tested_pins()
    
    # Get predefined tested PINs from our agent configurations
    agent_pins, predefined_tested = get_predefined_tested_pins()
    
    # Combine all tested PINs
    all_tested_pins = csv_tested.union(predefined_tested)
    
    print("\n🎯 COMPREHENSIVE PIN TESTING ANALYSIS")
    print("=" * 80)
    
    total_unique_pins = set()
    grand_total_tests = 0
    total_successes = 0
    
    for agent in ["A", "B", "C", "D"]:
        booking_id = booking_ids[agent]
        csv_pins = tested_pins[agent]
        predefined_pins = set(agent_pins[agent])
        combined_pins = csv_pins.union(predefined_pins)
        
        successes = success_pins[agent]
        tests = total_tests[agent] if total_tests[agent] > 0 else len(predefined_pins)
        
        print(f"\n🎯 AGENT {agent} - BOOKING {booking_id}:")
        print(f"   📊 Configured to test: {len(predefined_pins)} PINs")
        print(f"   📄 Found in CSV logs: {len(csv_pins)} PINs") 
        print(f"   🔢 Total unique PINs: {len(combined_pins)}")
        print(f"   🌟 SUCCESS PINs found: {len(successes)}")
        
        if successes:
            print(f"   🎉 WINNING PINs: {', '.join(successes)}")
        
        if combined_pins:
            sorted_pins = sorted(list(combined_pins))
            print(f"   📝 Sample tested PINs: {', '.join(sorted_pins[:15])}{'...' if len(sorted_pins) > 15 else ''}")
        
        total_unique_pins.update(combined_pins)
        grand_total_tests += tests
        total_successes += len(successes)
    
    print(f"\n📊 GRAND TOTALS:")
    print("=" * 40)
    print(f"🎯 Total tests conducted: {grand_total_tests}")
    print(f"🔢 Total unique PINs tested: {len(all_tested_pins)}")
    print(f"🌟 Total SUCCESS PINs found: {total_successes}")
    print(f"📈 Overall success rate: {(total_successes/grand_total_tests*100):.2f}%" if grand_total_tests > 0 else "0.00%")
    
    # Create master tested pins list
    print(f"\n📋 MASTER TESTED PINS LIST ({len(all_tested_pins)} PINs):")
    print("=" * 50)
    
    if all_tested_pins:
        sorted_all_pins = sorted(list(all_tested_pins))
        
        # Group pins in rows of 15 for better readability
        for i in range(0, len(sorted_all_pins), 15):
            row_pins = sorted_all_pins[i:i+15]
            print(f"   {', '.join(row_pins)}")
    
    # Save to file for Professor Johnny
    with open('TESTED_PINS_MASTER_LIST.txt', 'w') as f:
        f.write("🎯 PROFESSOR JOHNNY'S TESTED PINS MASTER LIST\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total unique PINs tested: {len(all_tested_pins)}\n")
        f.write(f"Total tests conducted: {grand_total_tests}\n")
        f.write(f"Total successes found: {total_successes}\n\n")
        
        f.write("TESTED PINS (sorted):\n")
        if all_tested_pins:
            sorted_all_pins = sorted(list(all_tested_pins))
            for i in range(0, len(sorted_all_pins), 15):
                row_pins = sorted_all_pins[i:i+15]
                f.write(f"{', '.join(row_pins)}\n")
    
    print(f"\n💾 Master list saved to: TESTED_PINS_MASTER_LIST.txt")
    
    # Show what's available for fresh testing
    print(f"\n🍀 READY FOR PROFESSOR'S LUCKY 50 PINS!")
    print(f"🎯 We've systematically tested {len(all_tested_pins)} unique PINs")
    print(f"🎲 Any PIN not in this list has a FRESH CHANCE of being the winner!")
    print(f"🤣 Let's see if Professor's intuition beats our systematic approach!")
    
    return all_tested_pins

if __name__ == "__main__":
    print("🎓 PROFESSOR JOHNNY'S PIN ANALYSIS SYSTEM")
    print("🔍 Analyzing 4-agent historical strike results...")
    print("🤣 Sorry for the gossip delay Professor! 😅")
    
    tested_pins = display_comprehensive_report()
    
    print(f"\n🎊 ANALYSIS COMPLETE!")
    print(f"🍀 Ready for your LUCKY 50 PINS, Professor!")
    print("🎯 Drop them on me and let's see what happens! 😎")
