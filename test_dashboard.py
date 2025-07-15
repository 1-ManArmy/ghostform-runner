#!/usr/bin/env python3
"""
Simple test dashboard
"""

from flask import Flask, render_template, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard route"""
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    """API endpoint for dashboard data"""
    # Test data
    return jsonify({
        'booking_id': '6160911170',
        'status': 'RUNNING',
        'current_agent': 'PRIMARY',
        'elapsed_time': '00:05:30',
        'total_pins_tried': 25,
        'remaining_pins': 9975,
        'progress_percentage': 0.25,
        'estimated_completion': '6 hours',
        'pins_per_minute': 4,
        'total_attempts': 25,
        'agents_used': 1,
        'success_rate': 0.0,
        'failure_rate': 96.0,
        'exception_rate': 4.0,
        'success_pin': None,
        'agent_statistics': {
            'PRIMARY': {'total': 25, 'success': 0, 'failure': 24, 'exception': 1}
        },
        'recent_attempts': [
            {'timestamp': '2025-07-16 00:22:09', 'agent': 'PRIMARY', 'pin': '1234', 'result': 'FAILURE'},
            {'timestamp': '2025-07-16 00:22:15', 'agent': 'PRIMARY', 'pin': '5678', 'result': 'FAILURE'},
            {'timestamp': '2025-07-16 00:22:21', 'agent': 'PRIMARY', 'pin': '9012', 'result': 'FAILURE'},
        ],
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("Starting Simple Test Dashboard...")
    print(f"Dashboard will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
