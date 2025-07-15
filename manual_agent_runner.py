#!/usr/bin/env python3
"""
Simple Manual Agent Runner - Run agents one by one with proper timing
"""

import subprocess
import time
import glob
import os

def run_agents_manually():
    """Run agents manually with proper timing"""
    
    # Get all agent files
    agent_files = sorted(glob.glob("boss_ai_playwright_*.py"))
    
    print(f"🎯 MANUAL AGENT RUNNER STARTED")
    print(f"📁 Found {len(agent_files)} agent files")
    print(f"⏱️ Strategy: 60 seconds between agents")
    print("="*60)
    
    for i, agent_file in enumerate(agent_files):
        print(f"\n[{i+1}/{len(agent_files)}] Starting: {agent_file}")
        
        try:
            # Run agent
            result = subprocess.run([
                "C:/Users/HP/ghostform-runner/venv/Scripts/python.exe",
                agent_file,
                "--headless"
            ], 
            cwd="c:/Users/HP/ghostform-runner",
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes timeout
            )
            
            print(f"✅ {agent_file} completed")
            if result.stdout:
                print(f"📋 Output: {result.stdout[-200:]}")  # Last 200 chars
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {agent_file} timed out")
        except Exception as e:
            print(f"❌ {agent_file} error: {e}")
        
        # Wait before next agent
        if i < len(agent_files) - 1:
            print(f"⏱️ Waiting 60 seconds before next agent...")
            time.sleep(60)
    
    print("\n🎯 MANUAL AGENT RUNNER COMPLETE!")

if __name__ == "__main__":
    run_agents_manually()
