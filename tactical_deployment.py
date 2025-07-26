#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 GHOSTFORM TACTICAL DEPLOYMENT COMMANDER
Strategic deployment and monitoring system for GHOSTFORM RUNNER army
"""

import subprocess
import threading
import time
import json
import os
from datetime import datetime
import glob

class TacticalCommander:
    def __init__(self):
        self.deployed_agents = []
        self.results = {}
        self.start_time = None
        
    def deploy_agent(self, agent_file):
        """Deploy a single agent and monitor its execution"""
        print(f"🚀 Deploying {agent_file}...")
        try:
            # Deploy with visible output - no stealth from us! 😄
            process = subprocess.Popen(
                ['C:/Users/HP/Pablo_Agent/ghostform-runner/ghostform-runner/venv/Scripts/python.exe', agent_file],
                stdout=None,  # Show output directly in terminal
                stderr=None,  # Show errors directly in terminal
                text=True
            )
            
            self.deployed_agents.append({
                'agent': agent_file,
                'process': process,
                'start_time': datetime.now(),
                'status': 'RUNNING'
            })
            
            print(f"✅ {agent_file} deployed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to deploy {agent_file}: {e}")
            return False
    
    def monitor_agents(self):
        """Monitor all deployed agents"""
        print("📊 MONITORING DEPLOYED AGENTS...")
        while True:
            active_count = 0
            for agent_info in self.deployed_agents:
                if agent_info['status'] == 'RUNNING':
                    if agent_info['process'].poll() is None:
                        active_count += 1
                    else:
                        agent_info['status'] = 'COMPLETED'
                        agent_info['end_time'] = datetime.now()
                        print(f"🏁 {agent_info['agent']} completed!")
            
            if active_count == 0:
                print("🎉 All agents completed!")
                break
                
            print(f"📊 Active agents: {active_count}")
            time.sleep(10)  # Check every 10 seconds
    
    def collect_results(self):
        """Collect results from all agents"""
        print("📋 COLLECTING RESULTS...")
        
        # Look for victory files
        victory_files = glob.glob("victory_*.json")
        log_files = glob.glob("agent_*_log.csv")
        
        success_count = len(victory_files)
        total_attempts = 0
        
        print(f"\n🎯 TACTICAL DEPLOYMENT RESULTS:")
        print(f"=" * 50)
        
        if success_count > 0:
            print(f"🎉 SUCCESS! Found {success_count} victories!")
            for victory_file in victory_files:
                try:
                    with open(victory_file, 'r') as f:
                        victory_data = json.load(f)
                    print(f"✅ {victory_data['agent']}: PIN {victory_data['success_pin']} for booking {victory_data['booking_id']}")
                except:
                    print(f"✅ Victory file: {victory_file}")
        else:
            print("🔍 No victories yet - continuing search...")
        
        print(f"\n📊 Log files generated: {len(log_files)}")
        print(f"📊 Deployed agents: {len(self.deployed_agents)}")
        
        return success_count > 0

def main():
    print("🎯 GHOSTFORM TACTICAL DEPLOYMENT INITIATED")
    print("=" * 60)
    
    commander = TacticalCommander()
    
    # Phase 1: Deploy test group (001A, 001B, 001C, 001D)
    print("\n🎯 PHASE 1: TACTICAL TEST GROUP DEPLOYMENT")
    print("Testing synchronized PIN group: 001A, 001B, 001C, 001D")
    
    test_agents = ['agent_001A.py', 'agent_001B.py', 'agent_001C.py', 'agent_001D.py']
    
    # Check if agents exist
    available_agents = []
    for agent in test_agents:
        if os.path.exists(agent):
            available_agents.append(agent)
            print(f"✅ {agent} ready")
        else:
            print(f"⚠️ {agent} not found")
    
    if len(available_agents) == 0:
        print("❌ No test agents found! Check agent files.")
        return
    
    print(f"\n🚀 Deploying {len(available_agents)} test agents...")
    
    # Deploy agents with 5-second intervals for stealth
    for i, agent in enumerate(available_agents):
        if commander.deploy_agent(agent):
            if i < len(available_agents) - 1:  # Don't wait after last agent
                print(f"⏳ Stealth delay... waiting 5 seconds before next deployment...")
                time.sleep(5)
    
    if len(commander.deployed_agents) > 0:
        print(f"\n📊 {len(commander.deployed_agents)} agents deployed successfully!")
        print("🔍 Monitoring agents... (Press Ctrl+C to stop monitoring)")
        
        try:
            # Start monitoring in a separate thread
            monitor_thread = threading.Thread(target=commander.monitor_agents)
            monitor_thread.start()
            
            # Wait for monitoring to complete or user interrupt
            monitor_thread.join()
            
        except KeyboardInterrupt:
            print("\n⚠️ Monitoring interrupted by user")
        
        # Collect and display results
        commander.collect_results()
    
    else:
        print("❌ No agents deployed successfully!")
    
    print("\n🎯 TACTICAL DEPLOYMENT COMPLETE")

if __name__ == "__main__":
    main()
