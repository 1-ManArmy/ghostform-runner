#!/usr/bin/env python3
"""
Multi-Booking Dashboard - Monitor all 3 booking IDs with smart analytics
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
booking_ids = ["6339614781", "6763779197", "6763734263"]
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

def get_booking_data(booking_id):
    """Get comprehensive data for a single booking ID"""
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
    
    return {
        'booking_id': booking_id,
        'status': status,
        'success_pin': success_pin,
        'pins_tried': pins_tried,
        'remaining_pins': remaining_pins,
        'progress_percentage': round(progress_percentage, 2),
        'total_attempts': total_attempts,
        'agents_used': len(agent_stats),
        'success_rate': round(success_rate, 1),
        'failure_rate': round(failure_rate, 1),
        'exception_rate': round(exception_rate, 1),
        'agent_statistics': agent_stats,
        'recent_attempts': attempts[-10:] if len(attempts) > 10 else attempts
    }

def get_combined_dashboard_data():
    """Get combined dashboard data for all booking IDs"""
    global last_update
    
    booking_data = {}
    combined_stats = {
        'total_pins_tried': 0,
        'total_attempts': 0,
        'total_agents': 0,
        'success_bookings': [],
        'active_bookings': [],
        'overall_progress': 0
    }
    
    # Get data for each booking ID
    for booking_id in booking_ids:
        data = get_booking_data(booking_id)
        booking_data[booking_id] = data
        
        # Add to combined stats
        combined_stats['total_pins_tried'] += data['pins_tried']
        combined_stats['total_attempts'] += data['total_attempts']
        combined_stats['total_agents'] += data['agents_used']
        
        if data['success_pin']:
            combined_stats['success_bookings'].append(booking_id)
        else:
            combined_stats['active_bookings'].append(booking_id)
    
    # Calculate overall progress
    combined_stats['overall_progress'] = round(
        (combined_stats['total_pins_tried'] / (len(booking_ids) * 10000) * 100), 2
    )
    
    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'booking_data': booking_data,
        'combined_stats': combined_stats,
        'last_update': last_update
    }

@app.route('/')
def dashboard():
    """Main dashboard route"""
    return render_template('multi_dashboard.html')

@app.route('/api/data')
def api_data():
    """API endpoint for dashboard data"""
    return jsonify(get_combined_dashboard_data())

@app.route('/api/booking/<booking_id>')
def api_booking_data(booking_id):
    """API endpoint for specific booking data"""
    if booking_id in booking_ids:
        return jsonify(get_booking_data(booking_id))
    else:
        return jsonify({'error': 'Invalid booking ID'}), 400

if __name__ == '__main__':
    print("🎯 MULTI-BOOKING DASHBOARD STARTED")
    print("="*50)
    print("📋 Monitoring booking IDs:")
    for booking_id in booking_ids:
        print(f"   • {booking_id}")
    print(f"🌐 Dashboard: http://localhost:5000")
    print("="*50)
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)
