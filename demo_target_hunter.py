#!/usr/bin/env python3
"""
DEMO: Target PIN Hunter System
Shows how the system works without actual web testing
"""

import time
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def demo_startup_banner():
    """Demo startup banner"""
    print(f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      🎯 TARGET PIN HUNTER DEMO 🎯                           ║
║                                                                              ║
║  Target Booking ID: 5727559423                                              ║
║  Agent: DEMO_AGENT                                                          ║
║  Attempts per agent: 10                                                     ║
║  Wait time: 1 second (demo speed)                                          ║
║  PIN Range: 0000-9999                                                       ║
║                                                                              ║
║                        🚀 DEMO STARTING! 🚀                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")

def demo_victory_banner(pin, attempt_num):
    """Demo victory banner"""
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                          🎉 VICTORY ACHIEVED! 🎉                            ║
║                                                                              ║
║  Target Booking ID: 5727559423                                              ║
║  Winning PIN: {pin}                                                        ║
║  Agent: DEMO_AGENT                                                          ║
║  Attempt Number: {attempt_num}                                               ║
║  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}                            ║
║                                                                              ║
║                      🚀 MISSION ACCOMPLISHED! 🚀                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def demo_return_home():
    """Demo return home banner"""
    print(f"""
{Fore.YELLOW}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        🏠 RETURNING HOME 🏠                                  ║
║                                                                              ║
║  Agent: DEMO_AGENT                                                          ║
║  Attempts made: 10                                                          ║
║  Status: No success, mission continues...                                   ║
║                                                                              ║
║  Another agent will take over the hunt!                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")

def demo_pin_hunting():
    """Demo PIN hunting process"""
    demo_startup_banner()
    time.sleep(1)
    
    # Simulate 10 attempts
    for attempt in range(1, 11):
        pin = f"{random.randint(0, 9999):04d}"
        
        print(f"{Fore.YELLOW}[DEMO_AGENT] Attempt {attempt}/10 - Testing PIN: {pin}{Style.RESET_ALL}")
        
        # Simulate testing delay
        time.sleep(1)
        
        # Random chance of success (10% chance for demo)
        if random.random() < 0.1:  # 10% chance
            print(f"{Fore.GREEN}🎉 SUCCESS! PIN {pin} is correct!{Style.RESET_ALL}")
            demo_victory_banner(pin, attempt)
            return
        else:
            print(f"{Fore.RED}❌ PIN {pin} failed{Style.RESET_ALL}")
        
        # Wait before next attempt
        if attempt < 10:
            print(f"{Fore.BLUE}⏱️ Waiting 1 second before next attempt...{Style.RESET_ALL}")
            time.sleep(1)
    
    # No success - return home
    demo_return_home()

def main():
    """Main demo function"""
    print(f"{Fore.CYAN}{Style.BRIGHT}🎬 TARGET PIN HUNTER DEMO{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This demo shows how the real system works{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop anytime{Style.RESET_ALL}")
    print()
    
    try:
        demo_pin_hunting()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Demo stopped by user{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Demo complete! Ready to run the real hunter? 🎯{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
