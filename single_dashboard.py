#!/usr/bin/env python3
"""
Single Booking Dashboard - Monitor booking ID 6339614781
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import time
from datetime import datetime
import glob
import re

app = Flask(__name__)

# Global variables
booking_id = "6339614781"
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
        print(f"Error reading log file for {booking_id}: {e}")
    
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
        print(f"Error reading PIN manager data for {booking_id}: {e}")
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

def get_dashboard_data():
    """Get comprehensive dashboard data"""
    global last_update
    
    attempts = read_unified_log(booking_id)
    pin_manager_data = read_pin_manager_data(booking_id)
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
    
    # Get success PIN
    success_pin = pin_manager_data.get('success_pin')
    status = 'SUCCESS' if success_pin else 'SEARCHING'
    
    # Get PIN statistics
    pins_tried = len(pin_manager_data.get('used_pins', []))
    remaining_pins = 10000 - pins_tried
    progress_percentage = (pins_tried / 10000 * 100) if pins_tried > 0 else 0
    
    # Calculate timing
    start_time = None
    if attempts:
        try:
            start_time = datetime.strptime(attempts[0]['timestamp'], '%Y-%m-%d %H:%M:%S')
        except:
            start_time = datetime.now()
    
    elapsed_time = '00:00:00'
    pins_per_minute = 0
    
    if start_time:
        elapsed = datetime.now() - start_time
        elapsed_seconds = elapsed.total_seconds()
        hours = int(elapsed_seconds // 3600)
        minutes = int((elapsed_seconds % 3600) // 60)
        seconds = int(elapsed_seconds % 60)
        elapsed_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        if elapsed_seconds > 0:
            pins_per_minute = int((total_attempts / elapsed_seconds) * 60)
    
    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'booking_id': booking_id,
        'status': status,
        'success_pin': success_pin,
        'pins_tried': pins_tried,
        'remaining_pins': remaining_pins,
        'progress_percentage': round(progress_percentage, 3),
        'total_attempts': total_attempts,
        'agents_used': len(agent_stats),
        'success_rate': round(success_rate, 1),
        'failure_rate': round(failure_rate, 1),
        'exception_rate': round(exception_rate, 1),
        'agent_statistics': agent_stats,
        'recent_attempts': attempts[-20:] if len(attempts) > 20 else attempts,
        'elapsed_time': elapsed_time,
        'pins_per_minute': pins_per_minute,
        'last_update': last_update
    }

@app.route('/')
def dashboard():
    """Main dashboard route"""
    return render_template('single_dashboard.html')

@app.route('/api/data')
def api_data():
    """API endpoint for dashboard data"""
    return jsonify(get_dashboard_data())

if __name__ == '__main__':
    print("🎯 SINGLE BOOKING DASHBOARD STARTED")
    print("="*50)
    print(f"📋 Monitoring booking ID: {booking_id}")
    print(f"🌐 Dashboard: http://localhost:5000")
    print("="*50)
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)
