#!/usr/bin/env python3
"""
ARMY DEPLOYMENT - Final Attack on Booking ID 6339614781
"""

import subprocess
import time
import glob
import os
from datetime import datetime
import threading
import json

class ArmyDeployment:
    def __init__(self):
        self.booking_id = "6339614781"
        self.agent_delay = 30  # 30 seconds between agents
        self.success_found = False
        self.current_agent = None
        
    def check_success(self):
        """Check if success PIN has been found"""
        data_file = f"pin_manager_{self.booking_id}.json"
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    return data.get('success_pin') is not None
            except:
                pass
        return False
    
    def run_agent(self, agent_file):
        """Run a single agent"""
        if self.success_found:
            return False
            
        self.current_agent = agent_file
        
        try:
            print(f"🚀 Deploying: {agent_file}")
            
            # Run agent with correct booking ID
            result = subprocess.run([
                "C:/Users/HP/ghostform-runner/venv/Scripts/python.exe",
                agent_file,
                "--confirmation", self.booking_id,
                "--headless"
            ], 
            cwd="c:/Users/HP/ghostform-runner",
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
            )
            
            # Check for success after agent runs
            if self.check_success():
                self.success_found = True
                print(f"🎉 SUCCESS! Agent {agent_file} found the PIN!")
                return True
            
            print(f"✅ {agent_file} completed mission")
            return False
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {agent_file} timed out")
            return False
        except Exception as e:
            print(f"❌ {agent_file} failed: {e}")
            return False
    
    def deploy_army(self):
        """Deploy the full army"""
        print("🎯 ARMY DEPLOYMENT INITIATED")
        print("="*60)
        print(f"📋 Target: Booking ID {self.booking_id}")
        print(f"⏱️ Strategy: 30-second intervals between agents")
        print(f"🤖 Total agents: 105")
        print(f"🎯 Mission: Find the PIN at all costs!")
        print("="*60)
        
        # Get all agent files
        agent_files = sorted(glob.glob("boss_ai_playwright_*.py"))
        
        print(f"📁 Agents ready for deployment: {len(agent_files)}")
        
        start_time = datetime.now()
        
        for i, agent_file in enumerate(agent_files):
            if self.success_found:
                print("🎉 MISSION ACCOMPLISHED! PIN FOUND!")
                break
            
            print(f"\n[{i+1}/{len(agent_files)}] Agent: {agent_file}")
            
            # Deploy agent
            success = self.run_agent(agent_file)
            
            if success:
                print("🎉 VICTORY! ARMY MISSION COMPLETE!")
                break
            
            # Wait before next agent deployment
            if i < len(agent_files) - 1 and not self.success_found:
                print(f"⏱️ Next deployment in {self.agent_delay} seconds...")
                time.sleep(self.agent_delay)
        
        end_time = datetime.now()
        elapsed = end_time - start_time
        
        print("\n" + "="*60)
        print("📊 FINAL ARMY REPORT")
        print("="*60)
        print(f"⏱️ Total deployment time: {elapsed}")
        print(f"🤖 Agents deployed: {i+1}")
        
        if self.success_found:
            print("🎉 MISSION STATUS: SUCCESS!")
            # Show the PIN
            data_file = f"pin_manager_{self.booking_id}.json"
            if os.path.exists(data_file):
                try:
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                        success_pin = data.get('success_pin')
                        if success_pin:
                            print(f"✅ SUCCESS PIN: {success_pin}")
                except:
                    pass
        else:
            print("🔍 MISSION STATUS: CONTINUING...")
        
        print("="*60)

def main():
    """Main deployment function"""
    army = ArmyDeployment()
    army.deploy_army()

if __name__ == "__main__":
    main()
