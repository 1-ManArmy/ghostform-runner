"""
🎯 BOSS'S COMPREHENSIVE PIN TESTING STATUS REPORT
Analysis of tested PINs across 4 booking IDs from CSV logs
"""

import csv
import glob
from datetime import datetime

# Boss's 4 booking IDs
BOOKING_IDS = {
    "A": "6339614781",  # Boss's ID #1
    "B": "6860261353",  # Boss's ID #2  
    "C": "6160911170",  # Boss's ID #3
    "D": "5830944764"   # Boss's ID #4
}

# 🔢 MASTER PIN LIST - 50 PINs to test for each booking ID
MASTER_PIN_LIST = [
    "2540", "1476", "6704", "9921", "2390", "5167", "7098", "3816", 
    "4039", "2745", "8652", "1790", "7943", "6005", "9102", "2384", 
    "7349", "1860", "8217", "9558", "1332", "4206", "7581", "3018", 
    "6440", "9224", "5421", "3975", "6876", "7033", "8751", "1094", 
    "5672", "8348", "7469", "2903", "1881", "4727", "3156", "9317",
    "1517", "4490", "2586", "6048", "7025", "1394", "7635", "2981", 
    "8479", "3724"  # Boss's 50 target PINs
]

def analyze_tested_pins():
    """Analyze all CSV files to extract tested PINs for each booking ID"""
    
    # Track tested PINs for each booking ID
    tested_pins = {id_val: set() for id_val in BOOKING_IDS.values()}
    success_pins = {id_val: set() for id_val in BOOKING_IDS.values()}
    
    # Read all CSV files
    csv_files = glob.glob('*.csv')
    
    for csv_file in csv_files:
        try:
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 5:
                        booking_id = row[2]
                        pin = row[3]
                        status = row[4]
                        
                        if booking_id in tested_pins:
                            tested_pins[booking_id].add(pin)
                            if status == "SUCCESS":
                                success_pins[booking_id].add(pin)
        except:
            continue
    
    return tested_pins, success_pins

def generate_comprehensive_report():
    """Generate comprehensive status report"""
    
    print("🎯 BOSS'S COMPREHENSIVE PIN TESTING STATUS REPORT")
    print("=" * 80)
    print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target Booking IDs: 4")
    print(f"🔢 Master PIN List: {len(MASTER_PIN_LIST)} PINs")
    print()
    
    tested_pins, success_pins = analyze_tested_pins()
    
    total_tests = 0
    total_successes = 0
    
    for letter, booking_id in BOOKING_IDS.items():
        pins_tested = tested_pins[booking_id]
        pins_success = success_pins[booking_id]
        
        # Check which of Boss's 50 target PINs have been tested
        master_tested = [pin for pin in MASTER_PIN_LIST if pin in pins_tested]
        master_untested = [pin for pin in MASTER_PIN_LIST if pin not in pins_tested]
        
        print(f"🎯 BOOKING {letter}: {booking_id}")
        print(f"   📊 Total PINs tested (all): {len(pins_tested)}")
        print(f"   🎯 Master list PINs tested: {len(master_tested)}/50")
        print(f"   🌟 SUCCESS PINs found: {len(pins_success)} - {sorted(list(pins_success))}")
        print(f"   ✅ Master tested: {master_tested[:10]}..." if len(master_tested) > 10 else f"   ✅ Master tested: {master_tested}")
        print(f"   ❌ Master untested: {master_untested[:10]}..." if len(master_untested) > 10 else f"   ❌ Master untested: {master_untested}")
        
        completion_pct = (len(master_tested) / 50) * 100
        if completion_pct == 100:
            status = "✅ COMPLETED"
        elif completion_pct > 0:
            status = f"🔄 IN PROGRESS ({completion_pct:.1f}%)"
        else:
            status = "🆕 NOT STARTED"
        print(f"   📋 Status: {status}")
        print()
        
        total_tests += len(pins_tested)
        total_successes += len(pins_success)
    
    print(f"🏆 OVERALL SUMMARY:")
    print(f"   📊 Total tests across all IDs: {total_tests}")
    print(f"   🌟 Total SUCCESS PINs found: {total_successes}")
    print(f"   🎯 Master list completion: {sum(len([p for p in MASTER_PIN_LIST if p in tested_pins[bid]]) for bid in BOOKING_IDS.values())}/200 total")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    for letter, booking_id in BOOKING_IDS.items():
        pins_tested = tested_pins[booking_id]
        master_untested = [pin for pin in MASTER_PIN_LIST if pin not in pins_tested]
        
        if master_untested:
            print(f"   🎯 Booking {letter}: Test {len(master_untested)} remaining master PINs")
        else:
            print(f"   ✅ Booking {letter}: Master PIN list COMPLETE!")

if __name__ == "__main__":
    generate_comprehensive_report()
