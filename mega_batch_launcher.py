#!/usr/bin/env python3
"""
🚀 MEGA BATCH LAUNCHER - Single Folder Strategy
Launches agents from single 'agents' folder in batches
Much more efficient than separate folders!
"""

import subprocess
import os
import time
import sys
from pathlib import Path
from datetime import datetime

# Configuration
AGENTS_FOLDER = "agents"
BATCH_SIZE = 53  # 53 agents per batch (2 batches total)
PYTHON_PATH = sys.executable

def display_mega_banner():
    """Display the mega batch banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🚀 MEGA BATCH LAUNCHER - SMART STRATEGY 🚀               ║
║                                                                              ║
║  📁 SINGLE FOLDER APPROACH:                                                 ║
║     • All agents in one '{AGENTS_FOLDER}' folder                                    ║
║     • Each agent is a standalone .py file                                   ║
║     • Batch processing: {BATCH_SIZE} agents at once                               ║
║     • Automatic batch management                                            ║
║                                                                              ║
║  🎯 STRATEGY:                                                                ║
║     • Batch 1: agent_001.py → agent_053.py                                  ║
║     • Batch 2: agent_054.py → agent_106.py                                  ║
║     • Each agent tests exactly 1 PIN                                        ║
║     • First success stops all batches                                       ║
║                                                                              ║
║                      🔥 MEGA DEPLOYMENT READY! 🔥                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def get_agent_files():
    """Get all agent files from the agents folder"""
    agents_path = Path(AGENTS_FOLDER)
    if not agents_path.exists():
        print(f"❌ Agents folder '{AGENTS_FOLDER}' not found!")
        print(f"🔧 Run 'python create_mega_agents.py' first to create agents")
        return []
    
    # Get all agent_XXX.py files
    agent_files = sorted([f for f in agents_path.glob("agent_*.py")])
    return agent_files

def launch_batch(agent_files, batch_num):
    """Launch a batch of agents"""
    processes = []
    
    print(f"\n🚀 LAUNCHING BATCH #{batch_num}: {len(agent_files)} agents")
    print("-" * 50)
    
    for i, agent_file in enumerate(agent_files, 1):
        try:
            # Run each agent file directly
            process = subprocess.Popen(
                [PYTHON_PATH, str(agent_file)],
                cwd=AGENTS_FOLDER,  # Run from agents folder
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            processes.append((agent_file.name, process))
            print(f"✅ {agent_file.name}: Launched")
            time.sleep(0.2)  # Small delay between launches
            
        except Exception as e:
            print(f"❌ {agent_file.name}: Failed - {e}")
    
    return processes

def monitor_batch(processes, batch_num):
    """Monitor batch for results"""
    print(f"\n🔍 Monitoring Batch #{batch_num} ({len(processes)} agents)...")
    
    completed = 0
    success_found = False
    
    while completed < len(processes) and not success_found:
        # Check for success file
        success_file = Path(AGENTS_FOLDER) / "MEGA_SUCCESS.txt"
        if success_file.exists():
            print(f"\n🎉 SUCCESS DETECTED IN BATCH #{batch_num}!")
            success_found = True
            break
        
        # Check individual processes
        for i, (agent_name, process) in enumerate(processes):
            if process and process.poll() is not None:
                stdout, stderr = process.communicate()
                completed += 1
                
                if "MEGA_SUCCESS" in stdout:
                    success_found = True
                    print(f"\n🎉 {agent_name} FOUND SUCCESS!")
                    break
                else:
                    print(f"📊 {agent_name}: Completed")
                
                processes[i] = (agent_name, None)
        
        if not success_found:
            active_agents = len([p for _, p in processes if p and p.poll() is None])
            print(f"📊 Batch #{batch_num}: {completed}/{len(processes)} complete, {active_agents} active")
            time.sleep(3)  # Check every 3 seconds
    
    # Terminate remaining processes
    terminated = 0
    for agent_name, process in processes:
        if process and process.poll() is None:
            try:
                process.terminate()
                terminated += 1
            except:
                pass
    
    if terminated > 0:
        print(f"🛑 Terminated {terminated} remaining agents in Batch #{batch_num}")
    
    return success_found

def main():
    """Main mega batch launcher"""
    display_mega_banner()
    
    # Get all agent files
    agent_files = get_agent_files()
    
    if not agent_files:
        return
    
    print(f"📊 MEGA BATCH STATUS:")
    print(f"   • Found {len(agent_files)} agent files")
    print(f"   • Batch size: {BATCH_SIZE} agents")
    print(f"   • Total batches: {(len(agent_files) + BATCH_SIZE - 1) // BATCH_SIZE}")
    print(f"   • Agents folder: {AGENTS_FOLDER}/")
    
    # Show first few agents
    print(f"\n📋 Sample agents:")
    for agent in agent_files[:5]:
        print(f"   • {agent.name}")
    if len(agent_files) > 5:
        print(f"   • ... and {len(agent_files) - 5} more")
    
    input(f"\nPress ENTER to start mega batch deployment...")
    
    # Create batches
    batches = [agent_files[i:i + BATCH_SIZE] for i in range(0, len(agent_files), BATCH_SIZE)]
    
    print(f"\n🔥 STARTING MEGA BATCH DEPLOYMENT...")
    start_time = time.time()
    
    for batch_num, batch_files in enumerate(batches, 1):
        print(f"\n{'='*70}")
        print(f"🚀 MEGA BATCH #{batch_num}/{len(batches)} - {len(batch_files)} agents")
        print(f"📁 Files: {batch_files[0].name} → {batch_files[-1].name}")
        print(f"{'='*70}")
        
        # Launch batch
        batch_processes = launch_batch(batch_files, batch_num)
        
        if not batch_processes:
            print(f"❌ Batch #{batch_num}: No agents launched")
            continue
        
        # Monitor for success
        success_found = monitor_batch(batch_processes, batch_num)
        
        if success_found:
            print(f"\n🏆 MEGA MISSION ACCOMPLISHED!")
            break
        
        # Brief pause between batches
        if batch_num < len(batches):
            print(f"\n⏳ Batch #{batch_num} complete. Preparing next batch...")
            time.sleep(3)
    
    # Final results
    end_time = time.time()
    total_time = end_time - start_time
    
    success_file = Path(AGENTS_FOLDER) / "MEGA_SUCCESS.txt"
    if success_file.exists():
        try:
            with open(success_file, "r") as f:
                success_data = f.read().strip()
            
            victory_banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎉 MEGA BATCH MISSION ACCOMPLISHED! 🎉                   ║
║                                                                              ║
║  📊 Success: {success_data[:55]}...   ║
║  ⏱️  Total Time: {total_time:.1f} seconds                                         ║
║  📁 Strategy: Single folder with batch processing                           ║
║  🚀 Agents deployed: {len(agent_files)}                                              ║
║                                                                              ║
║                     🏆 MEGA VICTORY ACHIEVED! 🏆                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
            print(victory_banner)
        except:
            print(f"\n🎉 MEGA SUCCESS! Check {AGENTS_FOLDER}/MEGA_SUCCESS.txt")
    else:
        print(f"\n📊 Mega batch deployment complete - no success found")
        print(f"Total time: {total_time:.1f} seconds")
        print(f"Agents tested: {len(agent_files)}")
    
    print(f"\n📊 MEGA BATCH STATS:")
    print(f"• Total agents: {len(agent_files)}")
    print(f"• Batches deployed: {len(batches)}")
    print(f"• Total time: {total_time:.1f} seconds")
    print(f"• Average batch time: {total_time/len(batches):.1f} seconds")

if __name__ == "__main__":
    main()
