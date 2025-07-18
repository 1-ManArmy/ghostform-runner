#!/usr/bin/env python3
"""
Bulk update proxy configuration in all boss_ai_playwright files
"""

import os
import glob

def update_proxy_config(file_path):
    """Update proxy configuration in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the old proxy configuration
        old_config = '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "customer-Oxylab_WFqvh",
    "password": "Oxylab_WFqvh1"
}'''
        
        new_config = '''PROXY_CONFIG = {
    "server": "http://pr.oxylabs.io:7777",
    "username": "phantom1_rOHk6",
    "password": "phantom1_rOHk6"
}'''
        
        if old_config in content:
            content = content.replace(old_config, new_config)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⚠️  No old config found in: {file_path}")
            return False
    
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all boss_ai_playwright files"""
    print("🔄 Updating proxy configuration in all boss_ai_playwright files...")
    print("=" * 60)
    
    # Find all boss_ai_playwright files
    files = glob.glob("boss_ai_playwright*.py")
    
    updated_count = 0
    
    for file_path in files:
        if update_proxy_config(file_path):
            updated_count += 1
    
    print("=" * 60)
    print(f"🎯 Updated {updated_count} out of {len(files)} files")
    print("✅ Proxy configuration update complete!")

if __name__ == "__main__":
    main()
