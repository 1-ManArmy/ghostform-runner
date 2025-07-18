#!/usr/bin/env python3
"""
🧪 TEST BOSS AGENT SYSTEM
Simple test to verify boss agent is working properly
"""

import sys
import os
from colorama import init, Fore, Style

init()

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from multi_pin_manager import PinManager
        print(f"{Fore.GREEN}✅ PinManager imported successfully{Style.RESET_ALL}")
        
        from playwright.sync_api import sync_playwright
        print(f"{Fore.GREEN}✅ Playwright imported successfully{Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Import error: {e}{Style.RESET_ALL}")
        return False

def test_pin_manager():
    """Test PIN manager functionality"""
    try:
        pin_mgr = PinManager("6160911170")
        print(f"{Fore.GREEN}✅ PinManager created for booking 6160911170{Style.RESET_ALL}")
        
        # Test getting a PIN
        pin = pin_mgr.get_next_pin("TEST_AGENT")
        if pin:
            print(f"{Fore.GREEN}✅ Got PIN: {pin}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ No PIN available (maybe success found?){Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ PinManager error: {e}{Style.RESET_ALL}")
        return False

def test_boss_agent():
    """Test boss agent script"""
    try:
        print(f"{Fore.YELLOW}🚀 Testing boss agent script...{Style.RESET_ALL}")
        
        # Import and test the boss agent
        import subprocess
        result = subprocess.run([sys.executable, "boss_ai_playwright_1A.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}✅ Boss agent script is working{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ Boss agent script error: {result.stderr}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Boss agent test error: {e}{Style.RESET_ALL}")
        return False

def main():
    """Main test function"""
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🧪 BOSS AGENT SYSTEM TEST 🧪                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    
    tests = [
        ("Import Test", test_imports),
        ("PIN Manager Test", test_pin_manager),
        ("Boss Agent Test", test_boss_agent)
    ]
    
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n{Fore.CYAN}🔍 Running {test_name}...{Style.RESET_ALL}")
        if test_func():
            passed += 1
            print(f"{Fore.GREEN}✅ {test_name} PASSED{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ {test_name} FAILED{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}📊 TEST RESULTS: {passed}/{len(tests)} tests passed{Style.RESET_ALL}")
    
    if passed == len(tests):
        print(f"{Fore.GREEN}{Style.BRIGHT}🎉 ALL TESTS PASSED! System is ready!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}❌ Some tests failed. Check errors above.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
