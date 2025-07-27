import re

# Extract PINs from the terminal output that were generated but failed due to errors
skipped_pins = []

# From the terminal output, I can see these PINs were generated but failed due to errors:

# Cycle 3 - Agent A (failed on first PIN)
skipped_pins.extend(['2271', '1871', '0474', '1075', '5730'])  # Only 2271 tested, rest skipped

# Cycle 3 - Agent B (failed early)  
skipped_pins.extend(['8348', '5647', '0083', '5611', '7964'])  # Only 8348, 5647 tested, rest skipped

# Cycle 3 - Agent C (failed on first PIN)
skipped_pins.extend(['1906', '1329', '8052', '7027', '7836'])  # Only 1906 mentioned, rest skipped

# Cycle 3 - Agent D (failed on first PIN)
skipped_pins.extend(['6723', '4282', '5103', '7288', '1133'])  # Only 6723 mentioned, rest skipped

# Cycle 4 - Agent A (failed on first PIN)
skipped_pins.extend(['1389', '6215', '8002', '4170', '4073'])  # Only 1389 mentioned, rest skipped

# Cycle 4 - Agent B (failed on first PIN)
skipped_pins.extend(['4718', '2727', '9725', '0515', '0330'])  # Only 4718 mentioned, rest skipped

# Cycle 4 - Agent C (first PIN worked, second failed)
skipped_pins.extend(['8168', '5734', '4093', '8343'])  # 8281 tested, 8168 mentioned, rest skipped

# Cycle 4 - Agent D (failed on first PIN)
skipped_pins.extend(['2421', '6923', '9058', '5096', '5449'])  # Only 2421 mentioned, rest skipped

# Cycle 5 - Agent A (failed on first PIN)
skipped_pins.extend(['2290', '0056', '9116', '8649', '2284'])  # Only 2290 mentioned, rest skipped

# Cycle 5 - Agent B (failed on first PIN)
skipped_pins.extend(['3825', '3876', '8289', '3780', '2931'])  # Only 3825 mentioned, rest skipped

# Cycle 5 - Agent C (failed on first PIN)
skipped_pins.extend(['5540', '0378', '3002', '2556', '9343'])  # Only 5540 mentioned, rest skipped

# Cycle 5 - Agent D (failed on first PIN)
skipped_pins.extend(['1310', '8622', '2377', '7463', '9877'])  # Only 1310 mentioned, rest skipped

# Remove duplicates and filter out the ones that were actually tested
tested_pins_from_logs = set()

# Read tested PINs from mission logs
log_files = ['mission_log_A.csv', 'mission_log_B.csv', 'mission_log_C.csv', 'mission_log_D.csv']

for log_file in log_files:
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        pin = parts[3]
                        tested_pins_from_logs.add(pin)
    except FileNotFoundError:
        print(f"Log file {log_file} not found")

# Filter out already tested PINs
actual_skipped_pins = [pin for pin in skipped_pins if pin not in tested_pins_from_logs]

# Remove duplicates
actual_skipped_pins = list(set(actual_skipped_pins))
actual_skipped_pins.sort()

print(f"📊 SKIPPED PIN ANALYSIS:")
print(f"🔢 Total PINs generated but skipped due to errors: {len(actual_skipped_pins)}")
print(f"🔢 Total PINs tested in logs: {len(tested_pins_from_logs)}")
print(f"")
print(f"🎯 SKIPPED PINs to test:")
print(','.join(actual_skipped_pins))
print(f"")
print(f"📋 For boss_ai_playwright-booking-pin.py:")
print(f"--pins \"{','.join(actual_skipped_pins)}\"")
