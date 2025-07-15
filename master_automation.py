import subprocess
import os
import time
import argparse
import sys
from pathlib import Path
from pin_manager import get_pin_manager

# --- Configurable parameters ---
parser = argparse.ArgumentParser(description="Master automation for Booking.com PIN testing")
parser.add_argument('--confirmation', type=str, default="6160911170", help='Confirmation number')
parser.add_argument('--pins', type=str, default="1,2,3,4", help='Comma-separated PINs (IGNORED - now uses random PINs)')
parser.add_argument('--wait', type=int, default=60, help='Wait time between attempts (seconds)')
parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
parser.add_argument('--delay', type=int, default=30, help='Delay between switching files (seconds)')
args = parser.parse_args()

CONFIRMATION = args.confirmation
WAIT_TIME = args.wait
HEADLESS = args.headless
DELAY_BETWEEN_FILES = args.delay
MASTER_LOG_FILE = f"master-automation-log_{CONFIRMATION}.txt"

# Get PIN manager
pin_mgr = get_pin_manager(CONFIRMATION)

# List of all files to run in sequence
FILES_TO_RUN = [
    "boss_ai_playwright.py",  # Primary file
    "boss_ai_playwright_A.py",
    "boss_ai_playwright_B.py",
    "boss_ai_playwright_C.py",
    "boss_ai_playwright_D.py",
    "boss_ai_playwright_E.py",
    "boss_ai_playwright_F.py",
    "boss_ai_playwright_G.py",
    "boss_ai_playwright_H.py",
    "boss_ai_playwright_I.py",
    "boss_ai_playwright_J.py",
    "boss_ai_playwright_K.py",
    "boss_ai_playwright_L.py",
    "boss_ai_playwright_M.py",
    "boss_ai_playwright_N.py",
    "boss_ai_playwright_O.py",
    "boss_ai_playwright_P.py",
    "boss_ai_playwright_Q.py",
    "boss_ai_playwright_R.py",
    "boss_ai_playwright_S.py",
    "boss_ai_playwright_T.py",
    "boss_ai_playwright_U.py",
    "boss_ai_playwright_V.py",
    "boss_ai_playwright_W.py",
    "boss_ai_playwright_X.py",
    "boss_ai_playwright_Y.py",
    "boss_ai_playwright_Z.py"
]

def log_master_activity(message):
    """Log master automation activity"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - MASTER: {message}"
    print(log_message)
    with open(MASTER_LOG_FILE, "a") as f:
        f.write(log_message + "\n")

def check_success_in_log():
    """Check if any SUCCESS was found in the PIN manager"""
    return pin_mgr.is_success_found()

def run_agent_file(filename):
    """Run a specific agent file with the provided parameters"""
    log_master_activity(f"Starting agent: {filename}")
    
    # Build command with parameters
    cmd = [sys.executable, filename, 
           "--confirmation", CONFIRMATION,
           "--wait", str(WAIT_TIME)]
    
    if HEADLESS:
        cmd.append("--headless")
    
    try:
        # Run the agent file
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
        
        log_master_activity(f"Agent {filename} completed with return code: {result.returncode}")
        
        # Log output for debugging
        if result.stdout:
            log_master_activity(f"Agent {filename} stdout: {result.stdout[-500:]}")  # Last 500 chars
        if result.stderr:
            log_master_activity(f"Agent {filename} stderr: {result.stderr[-500:]}")  # Last 500 chars
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        log_master_activity(f"Agent {filename} timed out after 1 hour")
        return False
    except Exception as e:
        log_master_activity(f"Error running agent {filename}: {e}")
        return False

def main():
    log_master_activity("=== MASTER AUTOMATION STARTED ===")
    log_master_activity(f"Configuration: Confirmation={CONFIRMATION}, Wait={WAIT_TIME}s, Headless={HEADLESS}")
    log_master_activity(f"Total files to process: {len(FILES_TO_RUN)}")
    
    # Show initial stats
    stats = pin_mgr.get_stats()
    log_master_activity(f"Initial stats: {stats['total_pins_tried']} PINs tried, {stats['remaining_pins']} remaining")
    
    success_found = False
    
    for i, filename in enumerate(FILES_TO_RUN, 1):
        # Check if file exists
        if not os.path.exists(filename):
            log_master_activity(f"WARNING: File {filename} not found, skipping...")
            continue
        
        log_master_activity(f"[{i}/{len(FILES_TO_RUN)}] Processing: {filename}")
        
        # Run the agent file
        agent_success = run_agent_file(filename)
        
        # Check if PIN was found (SUCCESS in PIN manager)
        if check_success_in_log():
            success_pin = pin_mgr.data['success_pin']
            log_master_activity(f"🎉 SUCCESS! PIN found: {success_pin} by agent: {filename}")
            log_master_activity("Stopping all other agents...")
            success_found = True
            break
        else:
            log_master_activity(f"Agent {filename} completed without finding PIN")
        
        # If not the last file, wait before next agent
        if i < len(FILES_TO_RUN):
            log_master_activity(f"Waiting {DELAY_BETWEEN_FILES}s before next agent...")
            time.sleep(DELAY_BETWEEN_FILES)
    
    # Final summary
    log_master_activity("=== MASTER AUTOMATION COMPLETED ===")
    if success_found:
        log_master_activity("✅ PIN FOUND! Check unified log for details.")
    else:
        log_master_activity("❌ No PIN found after testing all agents.")
    
    # Display final stats
    final_stats = pin_mgr.get_stats()
    log_master_activity("=== FINAL STATISTICS ===")
    log_master_activity(f"Total PINs tried: {final_stats['total_pins_tried']}")
    log_master_activity(f"Total attempts: {final_stats['total_attempts']}")
    log_master_activity(f"Agents used: {final_stats['agents_used']}")
    log_master_activity(f"Success PIN: {final_stats['success_pin']}")
    log_master_activity(f"Remaining PINs: {final_stats['remaining_pins']}")
    log_master_activity(f"Unified log file: {pin_mgr.log_file}")
    log_master_activity(f"PIN data file: {pin_mgr.data_file}")

if __name__ == "__main__":
    main()
