#!/usr/bin/env python3
"""
🔧 Fix Booking ID - Set correct booking ID 6160911170 in all agent files
"""

import re
import os

def fix_booking_id_in_all_files():
    """Fix booking ID to be 6160911170 in all agent files"""
    print("🔧 Fixing booking ID to 6160911170 in all agent files...")
    
    correct_booking_id = "6160911170"
    updated_count = 0
    error_count = 0
    
    for agent_num in range(1, 1001):  # 1 to 1000
        agent_file = f"boss_ai_playwright_pin{agent_num}.py"
        
        if os.path.exists(agent_file):
            try:
                # Read the file
                with open(agent_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Fix the confirmation argument - replace whatever is there with the correct booking ID
                pattern = r"parser\.add_argument\('--confirmation', type=str, default=\"[^\"]*\""
                replacement = f'parser.add_argument(\'--confirmation\', type=str, default="{correct_booking_id}"'
                
                updated_content = re.sub(pattern, replacement, content)
                
                # Write back to file
                with open(agent_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                updated_count += 1
                
                if agent_num <= 5 or agent_num % 100 == 0:  # Show progress
                    print(f"✅ Fixed booking ID in {agent_file}")
            
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Show first 5 errors
                    print(f"❌ Error fixing {agent_file}: {e}")
    
    print(f"\n🎉 BOOKING ID FIX COMPLETE!")
    print(f"✅ Successfully updated: {updated_count} files")
    print(f"❌ Errors encountered: {error_count} files")
    print(f"📋 All files now use booking ID: {correct_booking_id}")
    
    return updated_count

if __name__ == "__main__":
    fix_booking_id_in_all_files()
