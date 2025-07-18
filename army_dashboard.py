#!/usr/bin/env python3
"""
Single Booking Dashboard - Monitor booking ID 6339614781
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

def get_booking_data():
    """Get data for booking 6339614781"""
    booking_id = "6339614781"
    
    # Read PIN manager data
    data_file = f"pin_manager_{booking_id}.json"
    if not os.path.exists(data_file):
        return {
            'booking_id': booking_id,
            'pins_tried': 0,
            'success_pin': None,
            'total_attempts': 0,
            'agents_used': [],
            'status': 'WAITING'
        }
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            
        # Read log file
        log_file = f"unified_log_{booking_id}.txt"
        recent_attempts = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[-10:]:  # Last 10 attempts
                        parts = line.strip().split(',')
                        if len(parts) >= 5:
                            recent_attempts.append({
                                'timestamp': parts[0],
                                'agent': parts[2],
                                'pin': parts[3],
                                'result': parts[4]
                            })
            except:
                pass
        
        return {
            'booking_id': booking_id,
            'pins_tried': len(data.get('used_pins', [])),
            'success_pin': data.get('success_pin'),
            'total_attempts': data.get('total_attempts', 0),
            'agents_used': data.get('agents_used', []),
            'status': 'SUCCESS' if data.get('success_pin') else 'RUNNING',
            'recent_attempts': recent_attempts,
            'progress': len(data.get('used_pins', [])) / 10000 * 100
        }
    except Exception as e:
        print(f"Error reading data: {e}")
        return {'error': str(e)}

@app.route('/')
def dashboard():
    """Main dashboard"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ARMY Dashboard - Booking 6339614781</title>
        <style>
            body { font-family: Arial; background: #1a1a2e; color: white; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: #16213e; padding: 20px; border-radius: 10px; text-align: center; }
            .stat-value { font-size: 2rem; font-weight: bold; color: #0f3460; }
            .success { color: #00ff00; }
            .attempts { max-height: 300px; overflow-y: auto; background: #16213e; padding: 15px; border-radius: 10px; }
            .attempt { padding: 8px; margin: 5px 0; background: #0f3460; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 ARMY DASHBOARD</h1>
                <h2>Booking ID: 6339614781</h2>
            </div>
            
            <div class="stats" id="stats">
                <!-- Stats will be populated here -->
            </div>
            
            <div class="attempts">
                <h3>Recent Attempts</h3>
                <div id="recent-attempts">
                    <!-- Recent attempts will be populated here -->
                </div>
            </div>
        </div>
        
        <script>
            function updateDashboard() {
                fetch('/api/data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('stats').innerHTML = `
                            <div class="stat-card">
                                <div class="stat-value">${data.pins_tried}</div>
                                <div>PINs Tried</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${data.total_attempts}</div>
                                <div>Total Attempts</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${data.agents_used.length}</div>
                                <div>Agents Used</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value ${data.success_pin ? 'success' : ''}">${data.success_pin || 'Searching...'}</div>
                                <div>Success PIN</div>
                            </div>
                        `;
                        
                        document.getElementById('recent-attempts').innerHTML = data.recent_attempts.map(attempt => 
                            `<div class="attempt">${attempt.timestamp} - Agent ${attempt.agent} - PIN ${attempt.pin} - ${attempt.result}</div>`
                        ).join('');
                    });
            }
            
            updateDashboard();
            setInterval(updateDashboard, 5000); // Update every 5 seconds
        </script>
    </body>
    </html>
    '''

@app.route('/api/data')
def api_data():
    """API endpoint"""
    return jsonify(get_booking_data())

if __name__ == '__main__':
    print("🎯 ARMY DASHBOARD STARTED")
    print("🌐 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
