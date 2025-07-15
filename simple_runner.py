#!/usr/bin/env python3
"""
Simple Agent Runner - Run agents sequentially for booking ID 6339614781
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def get_agent_list():
    """Get list of all agent files"""
    agents = []
    
    # Add A-Z agents
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        agents.append(f'boss_ai_playwright_{letter}.py')
    
    # Add 1A-1Z agents
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        agents.append(f'boss_ai_playwright_1{letter}.py')
    
    # Add 2A-2Z agents
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        agents.append(f'boss_ai_playwright_2{letter}.py')
    
    # Add 3A-3Z agents
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        agents.append(f'boss_ai_playwright_3{letter}.py')
    
    return agents

def run_agent(agent_file):
    """Run a single agent"""
    try:
        print(f"🚀 Starting {agent_file}...")
        
        # Run the agent with headless mode
        result = subprocess.run([
            sys.executable, agent_file, '--headless'
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print(f"✅ {agent_file} completed successfully")
            return True
        else:
            print(f"❌ {agent_file} failed with return code {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {agent_file} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"💥 {agent_file} crashed: {e}")
        return False

def main():
    """Main execution function"""
    print("🎯 SIMPLE AGENT RUNNER STARTED")
    print("="*50)
    print(f"📋 Booking ID: 6339614781")
    print(f"⏰ Delay between agents: 30 seconds")
    print(f"🎭 Mode: Headless")
    print("="*50)
    
    agents = get_agent_list()
    total_agents = len(agents)
    
    print(f"📊 Total agents to run: {total_agents}")
    print(f"🕒 Estimated time: {total_agents * 30 / 60:.1f} minutes")
    print()
    
    # Check if agents exist
    missing_agents = [agent for agent in agents if not os.path.exists(agent)]
    if missing_agents:
        print(f"❌ Missing agents: {len(missing_agents)}")
        for agent in missing_agents[:5]:  # Show first 5
            print(f"   - {agent}")
        if len(missing_agents) > 5:
            print(f"   ... and {len(missing_agents) - 5} more")
        print()
    
    available_agents = [agent for agent in agents if os.path.exists(agent)]
    print(f"✅ Available agents: {len(available_agents)}")
    print()
    
    # Run agents
    successful_runs = 0
    failed_runs = 0
    
    for i, agent in enumerate(available_agents, 1):
        print(f"[{i}/{len(available_agents)}] Running {agent}")
        
        success = run_agent(agent)
        
        if success:
            successful_runs += 1
        else:
            failed_runs += 1
        
        print(f"   📈 Progress: {successful_runs} success, {failed_runs} failed")
        
        # Wait 30 seconds between agents (except for the last one)
        if i < len(available_agents):
            print(f"   ⏱️  Waiting 30 seconds before next agent...")
            time.sleep(30)
        
        print()
    
    # Final summary
    print("="*50)
    print("🏁 AUTOMATION COMPLETE")
    print(f"✅ Successful runs: {successful_runs}")
    print(f"❌ Failed runs: {failed_runs}")
    print(f"📊 Success rate: {successful_runs/(successful_runs+failed_runs)*100:.1f}%")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

if __name__ == "__main__":
    main()
