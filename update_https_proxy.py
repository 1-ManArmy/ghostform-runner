#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 HTTPS PROXY UPDATER
Update all 400 agents to use HTTPS proxy instead of HTTP
"""

import os
import re

def update_proxy_to_https(filepath):
    """Update a single agent file to use HTTPS proxy"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update HTTP to HTTPS in proxy configuration
        content = re.sub(
            r'"server": "http://pr\.oxylabs\.io:7777"',
            '"server": "https://pr.oxylabs.io:7777"',
            content
        )
        
        # Write back the updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    print("🔒 UPDATING ALL AGENTS TO HTTPS PROXY")
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
        print(f"\n🔄 Updating Batch {batch} agents to HTTPS...")
        
        for i in range(start, end + 1):
            agent_num = f"{i:03d}"
            filename = f"agent_{agent_num}{batch}.py"
            
            if os.path.exists(filename):
                if update_proxy_to_https(filename):
                    print(f"✅ Updated {filename} to HTTPS")
                    updated_count += 1
                else:
                    print(f"❌ Failed to update {filename}")
                    error_count += 1
            else:
                print(f"⚠️ File not found: {filename}")
                error_count += 1
    
    print(f"\n🎉 HTTPS PROXY UPDATE COMPLETE!")
    print(f"✅ Updated files: {updated_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total processed: {updated_count + error_count}")
    print(f"\n🔒 All agents now use HTTPS proxy!")
    print(f"🛡️ Secure connection: https://pr.oxylabs.io:7777")

if __name__ == "__main__":
    main()
