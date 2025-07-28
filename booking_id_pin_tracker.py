"""
PROFESSOR JOHNNY'S BOOKING ID PIN TRACKER
Creates 4 lists named after booking IDs showing ALL tested PINs for each ID
"""

import csv
import os
import glob
from datetime import datetime

def analyze_pins_by_booking_id():
    """Create 4 lists based on booking IDs showing all tested PINs"""
    
    print("PROFESSOR JOHNNY'S BOOKING ID PIN TRACKER")
    print("=" * 60)
    
    # The 4 booking IDs Professor Johnny specified
    BOOKING_IDS = [
        "6339614781",
        "6860261353", 
        "6160911170",
        "5830944764"
    ]
    
    # Dictionary to store tested PINs for each booking ID
    booking_pins = {booking_id: set() for booking_id in BOOKING_IDS}
    booking_successes = {booking_id: [] for booking_id in BOOKING_IDS}
    booking_test_counts = {booking_id: 0 for booking_id in BOOKING_IDS}
    
    # Find all CSV files that might contain test results
    csv_files = glob.glob("*.csv")
    print(f"Found {len(csv_files)} CSV files to analyze:")
    for file in csv_files:
        print(f"  - {file}")
    
    print("\nAnalyzing all CSV files for tested PINs...")
    
    # Read all CSV files and extract PINs for our target booking IDs
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            print(f"Reading: {csv_file}")
            try:
                with open(csv_file, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 4:
                            booking_id = row[2] if len(row) > 2 else ""
                            pin = row[3] if len(row) > 3 else ""
                            status = row[4] if len(row) > 4 else ""
                            
                            # Check if this is one of our target booking IDs
                            if booking_id in BOOKING_IDS and pin.isdigit() and len(pin) == 4:
                                booking_pins[booking_id].add(pin)
                                booking_test_counts[booking_id] += 1
                                if status == "SUCCESS":
                                    booking_successes[booking_id].append(pin)
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
    
    # Create individual files for each booking ID
    print("\nCreating booking ID lists...")
    
    for booking_id in BOOKING_IDS:
        tested_pins = booking_pins[booking_id]
        success_pins = booking_successes[booking_id]
        test_count = booking_test_counts[booking_id]
        
        print(f"\nBooking ID {booking_id}:")
        print(f"  Total tests: {test_count}")
        print(f"  Unique PINs tested: {len(tested_pins)}")
        print(f"  Success PINs: {len(success_pins)}")
        
        # Create file named after booking ID
        filename = f"{booking_id}_TESTED_PINS.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"BOOKING ID: {booking_id} - ALL TESTED PINS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total tests conducted: {test_count}\n")
            f.write(f"Unique PINs tested: {len(tested_pins)}\n")
            f.write(f"Success PINs found: {len(success_pins)}\n\n")
            
            if success_pins:
                f.write("SUCCESS PINS FOUND:\n")
                f.write("-" * 20 + "\n")
                for pin in success_pins:
                    f.write(f"   SUCCESS: {pin}\n")
                f.write("\n")
            
            if tested_pins:
                f.write(f"ALL TESTED PINS FOR BOOKING {booking_id} (sorted):\n")
                f.write("-" * 40 + "\n")
                sorted_pins = sorted(list(tested_pins))
                
                # Display in rows of 10 for better readability
                for i in range(0, len(sorted_pins), 10):
                    row_pins = sorted_pins[i:i+10]
                    f.write(f"   {', '.join(row_pins)}\n")
                f.write("\n")
                
                f.write(f"PIN LIST (comma separated for copy/paste):\n")
                f.write("-" * 35 + "\n")
                f.write(f"{', '.join(sorted_pins)}\n")
            else:
                f.write("NO PINS TESTED YET FOR THIS BOOKING ID\n")
        
        print(f"  Created: {filename}")
    
    # Create summary file
    summary_filename = "ALL_BOOKING_IDS_SUMMARY.txt"
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write("PROFESSOR JOHNNY'S BOOKING IDS - COMPLETE SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        total_unique_pins = set()
        grand_total_tests = 0
        total_successes = 0
        
        for booking_id in BOOKING_IDS:
            tested_pins = booking_pins[booking_id]
            success_pins = booking_successes[booking_id]
            test_count = booking_test_counts[booking_id]
            
            f.write(f"BOOKING ID: {booking_id}\n")
            f.write(f"  Total tests: {test_count}\n")
            f.write(f"  Unique PINs: {len(tested_pins)}\n")
            f.write(f"  Successes: {len(success_pins)}\n")
            if success_pins:
                f.write(f"  Success PINs: {', '.join(success_pins)}\n")
            f.write("\n")
            
            total_unique_pins.update(tested_pins)
            grand_total_tests += test_count
            total_successes += len(success_pins)
        
        f.write("GRAND TOTALS:\n")
        f.write("-" * 15 + "\n")
        f.write(f"Total tests across all booking IDs: {grand_total_tests}\n")
        f.write(f"Total unique PINs tested: {len(total_unique_pins)}\n")
        f.write(f"Total successes found: {total_successes}\n")
        f.write(f"Overall success rate: {(total_successes/grand_total_tests*100):.2f}%\n" if grand_total_tests > 0 else "Overall success rate: 0.00%\n")
    
    print(f"\nCreated summary: {summary_filename}")
    
    print(f"\nANALYSIS COMPLETE!")
    print("Created files:")
    for booking_id in BOOKING_IDS:
        print(f"  - {booking_id}_TESTED_PINS.txt")
    print(f"  - {summary_filename}")
    
    print(f"\nReady for Professor's LUCKY 50 PINS!")
    return booking_pins

if __name__ == "__main__":
    analyze_pins_by_booking_id()
