#!/usr/bin/env python3
"""
🎯 Dashboard Launcher
Quick start script for the Multi-Agent PIN Brute Force Dashboard
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Timer

def check_flask_installed():
    """Check if Flask is installed"""
    try:
        import flask
        print("✅ Flask is installed")
        return True
    except ImportError:
        print("❌ Flask is not installed")
        print("Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "pyyaml"])
            print("✅ Flask and PyYAML installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Flask. Please install manually:")
            print("pip install flask pyyaml")
            return False

def open_browser():
    """Open browser to dashboard URL after a delay"""
    time.sleep(2)  # Give server time to start
    webbrowser.open('http://localhost:5000')

def main():
    print("🎯 Multi-Agent PIN Brute Force Dashboard Launcher")
    print("=" * 60)
    
    # Check if dashboard server exists
    if not os.path.exists('dashboard_server.py'):
        print("❌ dashboard_server.py not found!")
        print("Make sure you're in the correct directory.")
        input("Press Enter to exit...")
        return
    
    # Check Flask installation
    if not check_flask_installed():
        input("Press Enter to exit...")
        return
    
    # Check for log file
    if os.path.exists('agent-log.txt'):
        print("✅ Found agent-log.txt")
    else:
        print("⚠️  No agent-log.txt found - dashboard will show empty until agents run")
    
    # Check for agent files
    agent_files = [f for f in os.listdir('.') if f.startswith('boss_ai_playwright') and f.endswith('.py')]
    print(f"📁 Found {len(agent_files)} agent files")
    
    print("\n🚀 Starting dashboard server...")
    print("📊 Dashboard will open at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Open browser after delay
    Timer(3.0, open_browser).start()
    
    try:
        # Start the dashboard server
        subprocess.run([sys.executable, "dashboard_server.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard server stopped")
    except FileNotFoundError:
        print("❌ Python not found. Make sure Python is installed and in PATH.")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
