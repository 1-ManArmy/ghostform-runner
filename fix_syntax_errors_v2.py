#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SYNTAX ERROR FIXER V2
Fix missing quote syntax error on line ~50 across all 400 agent files
"""

import os
import re

def fix_syntax_error_in_file(filepath):
    """Fix the missing quote syntax error in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the specific syntax error pattern
        # Look for lines like: print(f"🔑 Assigned PINs: xxxx, xxxx, xxxx, xxxx, xxxx
        # And add the missing closing quote
        pattern = r'print\(f"🔑 Assigned PINs: ([^"]+)$'
        replacement = r'print(f"🔑 Assigned PINs: \1")'
        
        # Apply the fix using multiline mode to catch the line ending
        fixed_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # Write back the fixed content only if we made changes
        if fixed_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True, "FIXED"
        else:
            return True, "NO_CHANGE"
        
    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False, f"ERROR: {e}"

def main():
    print("🔧 FIXING SYNTAX ERRORS ACROSS ALL AGENT FILES (V2)")
    print("=" * 50)
    
    # Define all batches and their ranges
    batches = [
        ('A', 1, 100),
        ('B', 1, 100),
        ('C', 1, 100),
        ('D', 1, 100)
    ]
    
    fixed_count = 0
    no_change_count = 0
    error_count = 0
    not_found_count = 0
    
    for batch, start, end in batches:
        print(f"\n🔧 Fixing Batch {batch} agents...")
        
        for i in range(start, end + 1):
            agent_num = f"{i:03d}"
            filename = f"agent_{agent_num}{batch}.py"
            filepath = filename
            
            if os.path.exists(filepath):
                success, result = fix_syntax_error_in_file(filepath)
                if success:
                    if result == "FIXED":
                        print(f"✅ Fixed {filename}")
                        fixed_count += 1
                    else:
                        print(f"✔️ OK {filename}")
                        no_change_count += 1
                else:
                    print(f"❌ Failed to fix {filename}: {result}")
                    error_count += 1
            else:
                print(f"⚠️ File not found: {filename}")
                not_found_count += 1
    
    print(f"\n🎉 SYNTAX FIX COMPLETE!")
    print(f"✅ Fixed files: {fixed_count}")
    print(f"✔️ Already OK: {no_change_count}")
    print(f"❌ Errors: {error_count}")
    print(f"⚠️ Not found: {not_found_count}")
    print(f"📊 Total processed: {fixed_count + no_change_count + error_count + not_found_count}")

if __name__ == "__main__":
    main()
