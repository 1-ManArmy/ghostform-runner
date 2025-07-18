#!/usr/bin/env python3
"""
🧠 SMART ARMY LAUNCHER - RAM-Optimized Batch Deployment
Deploys agents in intelligent batches to prevent system overload
"""

import subprocess
import os
import time
import sys
import psutil
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init
import threading

init(autoreset=True)

# Configuration
BOOKING_ID = "5724349472"
PYTHON_PATH = sys.executable
BASE_DIR = Path(".")
MAX_AGENTS = 106

# Smart resource management
TOTAL_RAM_GB = psutil.virtual_memory().total / (1024**3)
AVAILABLE_RAM_GB = psutil.virtual_memory().available / (1024**3)
CPU_CORES = psutil.cpu_count()

# Calculate optimal batch size based on system resources
def calculate_optimal_batch_size():
    """Calculate the best batch size based on system resources"""
    
    # Each Playwright browser uses roughly 150-300MB RAM
    estimated_ram_per_browser = 0.25  # 250MB per browser (conservative estimate)
    
    # Reserve 4GB for system + safety margin
    usable_ram = AVAILABLE_RAM_GB - 4.0
    
    if usable_ram < 2:
        return 5  # Very conservative for low RAM
    
    # Calculate based on RAM
    ram_based_batch = int(usable_ram / estimated_ram_per_browser)
    
    # Calculate based on CPU (2-3 browsers per core)
    cpu_based_batch = CPU_CORES * 2
    
    # Take the smaller of the two, but cap at reasonable limits
    optimal_batch = min(ram_based_batch, cpu_based_batch, 25)  # Max 25 browsers at once
    optimal_batch = max(optimal_batch, 3)  # Min 3 browsers
    
    return optimal_batch

BATCH_SIZE = calculate_optimal_batch_size()

def display_smart_banner():
    """Display the smart deployment banner"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🧠 SMART ARMY DEPLOYMENT SYSTEM 🧠                       ║
║                                                                              ║
║  📊 SYSTEM ANALYSIS:                                                         ║
║     • Total RAM: {TOTAL_RAM_GB:.1f} GB                                                   ║
║     • Available RAM: {AVAILABLE_RAM_GB:.1f} GB                                            ║
║     • CPU Cores: {CPU_CORES}                                                        ║
║     • Optimal Batch Size: {BATCH_SIZE} browsers                                   ║
║                                                                              ║
║  🎯 STRATEGY:                                                                ║
║     • Deploy {MAX_AGENTS} agents in batches of {BATCH_SIZE}                              ║
║     • Monitor RAM usage between batches                                      ║
║     • Auto-terminate on success                                              ║
║     • Prevent system overload                                                ║
║                                                                              ║
║                      🚀 SMART DEPLOYMENT READY! 🚀                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def monitor_system_resources():
    """Monitor system resources"""
    ram_percent = psutil.virtual_memory().percent
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return {
        'ram_percent': ram_percent,
        'cpu_percent': cpu_percent,
        'ram_available_gb': psutil.virtual_memory().available / (1024**3)
    }

def launch_agent_batch(agent_numbers):
    """Launch a batch of agents"""
    processes = []
    
    print(f"\n{Fore.YELLOW}🚀 Launching batch: Agents {agent_numbers[0]:03d}-{agent_numbers[-1]:03d}{Style.RESET_ALL}")
    
    for agent_num in agent_numbers:
        agent_dir = BASE_DIR / f"agent_{agent_num:03d}"
        main_py_path = agent_dir / "main.py"
        
        if not main_py_path.exists():
            print(f"{Fore.RED}❌ Agent #{agent_num:03d}: main.py not found{Style.RESET_ALL}")
            continue
        
        try:
            process = subprocess.Popen(
                [PYTHON_PATH, "main.py"],
                cwd=agent_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            processes.append((agent_num, process))
            print(f"{Fore.GREEN}✅ Agent #{agent_num:03d}: Launched{Style.RESET_ALL}")
            time.sleep(1)  # Small delay between launches
            
        except Exception as e:
            print(f"{Fore.RED}❌ Agent #{agent_num:03d}: Launch failed - {e}{Style.RESET_ALL}")
    
    return processes

def monitor_batch_for_success(processes, batch_num):
    """Monitor a batch of agents for success"""
    print(f"\n{Fore.CYAN}📊 Monitoring Batch #{batch_num} ({len(processes)} agents)...{Style.RESET_ALL}")
    
    success_found = False
    completed = 0
    
    while completed < len(processes) and not success_found:
        # Check for global success file
        success_file = BASE_DIR / "SUCCESS_FOUND.txt"
        if success_file.exists():
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 SUCCESS DETECTED IN BATCH #{batch_num}!{Style.RESET_ALL}")
            success_found = True
            break
        
        # Check individual processes
        for i, (agent_num, process) in enumerate(processes):
            if process and process.poll() is not None:
                stdout, stderr = process.communicate()
                completed += 1
                
                if "SUCCESS" in stdout:
                    success_found = True
                    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 Agent #{agent_num:03d} FOUND SUCCESS!{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.BLUE}Agent #{agent_num:03d}: Completed{Style.RESET_ALL}")
                
                processes[i] = (agent_num, None)
        
        if not success_found:
            time.sleep(3)  # Check every 3 seconds
    
    # Terminate remaining processes in this batch
    for agent_num, process in processes:
        if process and process.poll() is None:
            try:
                process.terminate()
                print(f"{Fore.YELLOW}🛑 Agent #{agent_num:03d}: Terminated{Style.RESET_ALL}")
            except:
                pass
    
    return success_found

def wait_for_ram_recovery():
    """Wait for RAM to recover before next batch"""
    while True:
        resources = monitor_system_resources()
        if resources['ram_percent'] < 80 and resources['ram_available_gb'] > 3:
            break
        
        print(f"{Fore.YELLOW}⏳ Waiting for RAM recovery... (RAM: {resources['ram_percent']:.1f}%, Available: {resources['ram_available_gb']:.1f}GB){Style.RESET_ALL}")
        time.sleep(5)

def main():
    """Main smart deployment function"""
    display_smart_banner()
    
    print(f"{Fore.CYAN}📋 DEPLOYMENT STRATEGY:{Style.RESET_ALL}")
    print(f"   • Total agents: {MAX_AGENTS}")
    print(f"   • Batch size: {BATCH_SIZE} agents per batch")
    print(f"   • Total batches: {(MAX_AGENTS + BATCH_SIZE - 1) // BATCH_SIZE}")
    print(f"   • Estimated time: 2-5 minutes per batch")
    print(f"   • RAM monitoring: Active")
    print()
    
    # Show system status
    resources = monitor_system_resources()
    print(f"{Fore.GREEN}💻 SYSTEM STATUS:")
    print(f"   • RAM Usage: {resources['ram_percent']:.1f}%")
    print(f"   • CPU Usage: {resources['cpu_percent']:.1f}%")
    print(f"   • Available RAM: {resources['ram_available_gb']:.1f} GB{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}Press ENTER to start smart deployment...{Style.RESET_ALL}")
    
    # Create agent batches
    all_agents = list(range(1, MAX_AGENTS + 1))
    batches = [all_agents[i:i + BATCH_SIZE] for i in range(0, len(all_agents), BATCH_SIZE)]
    
    print(f"\n{Fore.RED}🔥 STARTING SMART DEPLOYMENT...{Style.RESET_ALL}")
    start_time = time.time()
    
    for batch_num, agent_batch in enumerate(batches, 1):
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"📦 BATCH #{batch_num}/{len(batches)}: Agents {agent_batch[0]:03d}-{agent_batch[-1]:03d}")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        # Check system resources before launching
        resources = monitor_system_resources()
        if resources['ram_percent'] > 85:
            print(f"{Fore.YELLOW}⚠️  High RAM usage detected. Waiting for recovery...{Style.RESET_ALL}")
            wait_for_ram_recovery()
        
        # Launch batch
        batch_processes = launch_agent_batch(agent_batch)
        
        if not batch_processes:
            print(f"{Fore.RED}❌ Batch #{batch_num}: No agents launched{Style.RESET_ALL}")
            continue
        
        # Monitor batch for success
        success_found = monitor_batch_for_success(batch_processes, batch_num)
        
        if success_found:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🏆 SUCCESS FOUND! Stopping all deployment.{Style.RESET_ALL}")
            break
        
        # Wait a bit before next batch (unless it's the last one)
        if batch_num < len(batches):
            print(f"\n{Fore.CYAN}⏳ Batch #{batch_num} complete. Preparing next batch...{Style.RESET_ALL}")
            wait_for_ram_recovery()
            time.sleep(2)
    
    # Final results
    end_time = time.time()
    total_time = end_time - start_time
    
    # Check if we found success
    success_file = BASE_DIR / "SUCCESS_FOUND.txt"
    if success_file.exists():
        try:
            with open(success_file, "r") as f:
                success_data = f.read().strip()
            
            victory_banner = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 SMART ARMY MISSION ACCOMPLISHED! 🎉                   ║
║                                                                              ║
║  📊 Success Details: {success_data[:40]}...                    ║
║  ⏱️  Total Time: {total_time:.1f} seconds                                         ║
║  🧠 Strategy: Smart batching prevented system overload                      ║
║  💻 System: Stable throughout deployment                                    ║
║                                                                              ║
║                     🏆 SMART VICTORY ACHIEVED! 🏆                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
            print(victory_banner)
        except:
            print(f"\n{Fore.GREEN}🎉 SUCCESS! Check SUCCESS_FOUND.txt for details{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}📋 Smart deployment completed - no success found{Style.RESET_ALL}")
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Batches deployed: {len(batches)}")
    
    # Final system status
    final_resources = monitor_system_resources()
    print(f"\n{Fore.CYAN}📊 FINAL SYSTEM STATUS:")
    print(f"• RAM Usage: {final_resources['ram_percent']:.1f}%")
    print(f"• CPU Usage: {final_resources['cpu_percent']:.1f}%")
    print(f"• System: {'✅ Stable' if final_resources['ram_percent'] < 90 else '⚠️ High usage'}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
