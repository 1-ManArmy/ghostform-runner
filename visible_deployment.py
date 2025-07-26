#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 VISIBLE TACTICAL DEPLOYMENT 
No more stealth mode - let's see our agents in action! 🤣
"""

import subprocess
import time
import os

def deploy_visible_agent(agent_file):
    """Deploy agent with full visibility"""
    print(f"🚀 LAUNCHING VISIBLE AGENT: {agent_file}")
    print("=" * 50)
    
    try:
        # Launch agent with full visibility - no hiding!
        result = subprocess.run(
            ['C:/Users/HP/Pablo_Agent/ghostform-runner/ghostform-runner/venv/Scripts/python.exe', agent_file],
            cwd=os.getcwd(),
            text=True,
            capture_output=False  # Show everything!
        )
        
        print(f"🏁 {agent_file} completed with exit code: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Failed to deploy {agent_file}: {e}")
        return False

def main():
    print("🎯 VISIBLE GHOSTFORM DEPLOYMENT - NO MORE STEALTH MODE! 🤣")
    print("=" * 60)
    
    # Deploy one agent at a time so we can see what's happening
    test_agents = ['agent_001A.py']  # Start with just one
    
    for agent in test_agents:
        if os.path.exists(agent):
            print(f"\n🎯 Testing {agent} with FULL VISIBILITY...")
            deploy_visible_agent(agent)
            print(f"\n✅ {agent} test complete!")
        else:
            print(f"⚠️ {agent} not found")
    
    print("\n🎯 VISIBLE DEPLOYMENT COMPLETE!")
    
    # Check for any results
    print("\n📋 CHECKING RESULTS...")
    if os.path.exists("victory_001A.json"):
        print("🎉 VICTORY FILE FOUND!")
        with open("victory_001A.json", 'r') as f:
            print(f.read())
    else:
        print("🔍 No victory file yet")
    
    if os.path.exists("agent_001A_log.csv"):
        print("📊 LOG FILE FOUND!")
        print("Last few lines of log:")
        with open("agent_001A_log.csv", 'r') as f:
            lines = f.readlines()
            for line in lines[-3:]:
                print(line.strip())
    else:
        print("📊 No log file yet")

if __name__ == "__main__":
    main()
