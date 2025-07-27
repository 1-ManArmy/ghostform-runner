#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SEQUENTIAL DEPLOYMENT STRATEGY
Execute agents in synchronized PIN groups: A→B→C→D for each number
Based on boss's strategic approach
"""

import os
import subprocess
import time

def deploy_sequential():
    print("🎯 SEQUENTIAL DEPLOYMENT INITIATED")
    print("=" * 50)
    print("Strategy: Test synchronized PIN groups sequentially")
    print("Order: For each number 1-100 → A, B, C, D")
    print()
    
    # Use the virtual environment Python
    python_cmd = "C:/Users/HP/Pablo_Agent/ghostform-runner/ghostform-runner/venv/Scripts/python.exe"
    
    total_deployed = 0
    successful_agents = 0
    
    for i in range(1, 101):  # 1 to 100
        print(f"\n🔢 PIN GROUP {i:03d} - Testing synchronized PINs:")
        
        for suffix in ["A", "B", "C", "D"]:
            agent_file = f"agent_{i:03d}{suffix}.py"
            
            if os.path.exists(agent_file):
                print(f"▶ Running {agent_file}...")
                total_deployed += 1
                
                try:
                    # Run agent and wait for completion
                    result = subprocess.run(
                        [python_cmd, agent_file],
                        capture_output=False,  # Show output directly
                        text=True,
                        timeout=300  # 5 minute timeout per agent
                    )
                    
                    if result.returncode == 0:
                        print(f"✅ {agent_file} completed successfully")
                        successful_agents += 1
                    else:
                        print(f"⚠️ {agent_file} completed with warnings")
                        
                except subprocess.TimeoutExpired:
                    print(f"⏰ {agent_file} timed out (5 minutes)")
                except KeyboardInterrupt:
                    print(f"\n⚠️ Deployment interrupted by user at {agent_file}")
                    break
                except Exception as e:
                    print(f"❌ Error running {agent_file}: {e}")
                
                # Small delay between agents in same group
                time.sleep(2)
                
            else:
                print(f"⚠️ File not found: {agent_file}")
        
        # Check for victory files after each group
        victory_files = [f for f in os.listdir('.') if f.startswith('victory_')]
        if victory_files:
            print(f"\n🎉 VICTORY DETECTED! Found {len(victory_files)} success(es)!")
            for victory_file in victory_files:
                print(f"🏆 {victory_file}")
            
            response = input("\n🤔 Continue deployment or stop to analyze? (c/s): ").strip().lower()
            if response == 's':
                print("🛑 Deployment stopped for analysis")
                break
        
        # Delay between PIN groups for stealth
        if i < 100:  # Don't wait after last group
            print(f"⏳ Stealth delay before next PIN group...")
            time.sleep(5)
    
    print(f"\n🎯 DEPLOYMENT SUMMARY:")
    print(f"📊 Total agents deployed: {total_deployed}")
    print(f"✅ Successful completions: {successful_agents}")
    print(f"🏆 Victory files found: {len([f for f in os.listdir('.') if f.startswith('victory_')])}")

if __name__ == "__main__":
    deploy_sequential()
