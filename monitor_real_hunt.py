#!/usr/bin/env python3
"""
Real-time progress monitor for booking ID 6160911170
Shows live statistics and progress updates
"""

import os
import time
import json
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

REAL_BOOKING_ID = "6160911170"
LOG_FILE = f"real_hunt_log_{REAL_BOOKING_ID}.txt"
SUCCESS_FILE = f"REAL_SUCCESS_{REAL_BOOKING_ID}.json"

def get_hunt_stats():
    """Get current hunt statistics"""
    stats = {
        'total_attempts': 0,
        'success_found': False,
        'success_pin': None,
        'agents_active': set(),
        'recent_attempts': [],
        'progress_percent': 0
    }
    
    # Check for success
    if os.path.exists(SUCCESS_FILE):
        try:
            with open(SUCCESS_FILE, 'r') as f:
                success_data = json.load(f)
            stats['success_found'] = True
            stats['success_pin'] = success_data['success_pin']
        except:
            pass
    
    # Read log file
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            stats['total_attempts'] = len(lines)
            stats['progress_percent'] = (len(lines) / 10000) * 100
            
            # Get recent attempts (last 10)
            for line in lines[-10:]:
                parts = line.strip().split(',')
                if len(parts) >= 6:
                    stats['recent_attempts'].append({
                        'timestamp': parts[0],
                        'agent': parts[2],
                        'pin': parts[3],
                        'result': parts[4]
                    })
            
            # Count unique agents
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    stats['agents_active'].add(parts[2])
        except:
            pass
    
    return stats

def display_progress():
    """Display current progress"""
    stats = get_hunt_stats()
    
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    print(f"🎯 REAL PIN HUNT PROGRESS - Booking ID: {REAL_BOOKING_ID}")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    if stats['success_found']:
        print(f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 SUCCESS ACHIEVED! 🎉                                   ║
║                                                                              ║
║  Booking ID: {REAL_BOOKING_ID}                                               ║
║  WINNING PIN: {stats['success_pin']}                                       ║
║  Total Attempts: {stats['total_attempts']}                                  ║
║                                                                              ║
║                   🚀 MISSION COMPLETE! 🚀                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
""")
    else:
        print(f"{Fore.YELLOW}📊 HUNT IN PROGRESS...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total attempts: {stats['total_attempts']}/10000{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Progress: {stats['progress_percent']:.2f}%{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Active agents: {len(stats['agents_active'])}{Style.RESET_ALL}")
        
        # Progress bar
        bar_length = 50
        filled_length = int(bar_length * stats['progress_percent'] / 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"{Fore.GREEN}Progress: |{bar}| {stats['progress_percent']:.1f}%{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}📋 Recent attempts:{Style.RESET_ALL}")
    if stats['recent_attempts']:
        for attempt in stats['recent_attempts']:
            color = Fore.GREEN if attempt['result'] == 'SUCCESS' else Fore.RED if attempt['result'] == 'FAILURE' else Fore.YELLOW
            print(f"  {color}{attempt['timestamp']} | {attempt['agent']} | PIN: {attempt['pin']} | {attempt['result']}{Style.RESET_ALL}")
    else:
        print(f"  {Fore.GRAY}No attempts yet{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

def main():
    """Main monitoring function"""
    print(f"{Fore.GREEN}🎯 REAL PIN HUNT MONITOR - Starting...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop monitoring{Style.RESET_ALL}\n")
    
    try:
        while True:
            # Clear screen (works on Windows)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            display_progress()
            
            # Check if success found
            if os.path.exists(SUCCESS_FILE):
                print(f"\n{Fore.GREEN}🎉 SUCCESS FOUND! Monitoring complete.{Style.RESET_ALL}")
                break
            
            print(f"\n{Fore.BLUE}⏱️ Next update in 10 seconds...{Style.RESET_ALL}")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}❌ Monitoring stopped by user{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
