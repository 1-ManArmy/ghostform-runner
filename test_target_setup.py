# Double-click this file:
complete_pin_system.bat#!/usr/bin/env python3
"""
Test script to verify the target PIN hunter setup
"""

import sys
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def test_setup():
    """Test the basic setup"""
    print(f"{Fore.CYAN}🧪 Testing Target PIN Hunter Setup{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Target Booking ID: 5727559423{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Colorama imported successfully{Style.RESET_ALL}")
    
    # Test playwright import
    try:
        from playwright.sync_api import sync_playwright
        print(f"{Fore.GREEN}✅ Playwright imported successfully{Style.RESET_ALL}")
    except ImportError as e:
        print(f"{Fore.RED}❌ Playwright import failed: {e}{Style.RESET_ALL}")
        return False
    
    # Test file creation
    try:
        test_file = "test_target_setup.txt"
        with open(test_file, 'w') as f:
            f.write("Test file for target PIN hunter")
        print(f"{Fore.GREEN}✅ File operations working{Style.RESET_ALL}")
        os.remove(test_file)
    except Exception as e:
        print(f"{Fore.RED}❌ File operations failed: {e}{Style.RESET_ALL}")
        return False
    
    print(f"{Fore.GREEN}{Style.BRIGHT}🎯 All tests passed! Ready for PIN hunting!{Style.RESET_ALL}")
    return True

if __name__ == "__main__":
    test_setup()
