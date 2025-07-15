#!/usr/bin/env python3
"""
Production Dashboard for PIN Testing Automation
Real-time monitoring with actual data from production system
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import time
import threading
from datetime import datetime
import glob
import re

app = Flask(__name__)

# Global variables
current_booking_id = "6160911170"
last_update = None

def read_unified_log(booking_id):
    """Read and parse the unified log file"""
    log_file = f"unified_log_{booking_id}.txt"
    if not os.path.exists(log_file):
        return []
    
    attempts = []
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                # Parse CSV format: TIMESTAMP,BOOKING_ID,AGENT,PIN,RESULT,URL
                parts = line.split(',')
                if len(parts) >= 5:
                    timestamp = parts[0]
                    booking_id_log = parts[1]
                    agent = parts[2]
                    pin = parts[3]
                    result = parts[4]
                    
                    # Only process entries for the current booking ID
                    if booking_id_log == booking_id:
                        attempts.append({
                            'timestamp': timestamp,
                            'agent': agent,
                            'pin': pin,
                            'result': result
                        })
    except Exception as e:
        print(f"Error reading log file: {e}")
    
    return attempts

def read_pin_manager_data(booking_id):
    """Read PIN manager data file"""
    data_file = f"pin_manager_{booking_id}.json"
    if not os.path.exists(data_file):
        return {}
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading PIN manager data: {e}")
        return {}

def get_agent_statistics(attempts):
    """Calculate agent statistics from attempts"""
    stats = {}
    for attempt in attempts:
        agent = attempt['agent']
        if agent not in stats:
            stats[agent] = {'total': 0, 'success': 0, 'failure': 0, 'exception': 0}
        
        stats[agent]['total'] += 1
        stats[agent][attempt['result'].lower()] += 1
    
    return stats

def check_running_processes():
    """Check if any agent processes are running"""
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'boss_ai_playwright' in cmdline or 'master_automation' in cmdline:
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except ImportError:
        pass
    return False

def get_dashboard_data():
    """Get comprehensive dashboard data"""
    global current_booking_id, last_update
    
    attempts = read_unified_log(current_booking_id)
    pin_manager_data = read_pin_manager_data(current_booking_id)
    agent_stats = get_agent_statistics(attempts)
    
    # Calculate metrics
    total_attempts = len(attempts)
    success_count = sum(1 for a in attempts if a['result'] == 'SUCCESS')
    failure_count = sum(1 for a in attempts if a['result'] == 'FAILURE')
    exception_count = sum(1 for a in attempts if a['result'] == 'EXCEPTION')
    
    # Calculate rates
    success_rate = (success_count / total_attempts * 100) if total_attempts > 0 else 0
    failure_rate = (failure_count / total_attempts * 100) if total_attempts > 0 else 0
    exception_rate = (exception_count / total_attempts * 100) if total_attempts > 0 else 0
    
    # Get current agent and status
    current_agent = 'None'
    status = 'IDLE'
    success_pin = None
    
    # Check for success PIN
    for attempt in attempts:
        if attempt['result'] == 'SUCCESS':
            success_pin = attempt['pin']
            status = 'SUCCESS'
            break
    
    # If no success, check if running
    if status != 'SUCCESS':
        if check_running_processes():
            status = 'RUNNING'
            if attempts:
                current_agent = attempts[-1]['agent']
    
    # Get PIN statistics from PIN manager
    pins_tried = len(pin_manager_data.get('used_pins', []))
    total_pins = 10000
    remaining_pins = total_pins - pins_tried
    progress_percentage = (pins_tried / total_pins * 100) if total_pins > 0 else 0
    
    # Calculate timing
    start_time = None
    if attempts:
        try:
            start_time = datetime.strptime(attempts[0]['timestamp'], '%Y-%m-%d %H:%M:%S')
        except:
            start_time = datetime.now()
    
    elapsed_time = '00:00:00'
    pins_per_minute = 0
    estimated_completion = 'Calculating...'
    
    if start_time:
        elapsed = datetime.now() - start_time
        elapsed_seconds = elapsed.total_seconds()
        hours = int(elapsed_seconds // 3600)
        minutes = int((elapsed_seconds % 3600) // 60)
        seconds = int(elapsed_seconds % 60)
        elapsed_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        if elapsed_seconds > 0:
            pins_per_minute = int((pins_tried / elapsed_seconds) * 60)
            if pins_per_minute > 0:
                remaining_minutes = remaining_pins / pins_per_minute
                if remaining_minutes < 60:
                    estimated_completion = f"{int(remaining_minutes)} minutes"
                else:
                    estimated_hours = remaining_minutes / 60
                    estimated_completion = f"{estimated_hours:.1f} hours"
    
    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'booking_id': current_booking_id,
        'status': status,
        'current_agent': current_agent,
        'elapsed_time': elapsed_time,
        'total_pins_tried': pins_tried,
        'remaining_pins': remaining_pins,
        'progress_percentage': round(progress_percentage, 2),
        'estimated_completion': estimated_completion,
        'pins_per_minute': pins_per_minute,
        'total_attempts': total_attempts,
        'agents_used': len(agent_stats),
        'success_rate': round(success_rate, 1),
        'failure_rate': round(failure_rate, 1),
        'exception_rate': round(exception_rate, 1),
        'success_pin': success_pin,
        'agent_statistics': agent_stats,
        'recent_attempts': attempts[-20:] if len(attempts) > 20 else attempts,
        'last_update': last_update
    }

@app.route('/')
def dashboard():
    """Main dashboard route"""
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    """API endpoint for dashboard data"""
    return jsonify(get_dashboard_data())

@app.route('/api/set_booking_id', methods=['POST'])
def set_booking_id():
    """API endpoint to set booking ID"""
    global current_booking_id
    try:
        data = request.get_json()
        booking_id = data.get('booking_id')
        if booking_id:
            current_booking_id = booking_id
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'No booking ID provided'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("Starting Production Dashboard...")
    print(f"Dashboard available at: http://localhost:5000")
    print(f"Monitoring booking ID: {current_booking_id}")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)
