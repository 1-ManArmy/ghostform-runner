#!/usr/bin/env python3
"""
🎯 Multi-Agent PIN Brute Force Dashboard Server
Professional monitoring system for distributed booking.com PIN testing
"""

from flask import Flask, jsonify, send_from_directory
import os
import json
import yaml
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import glob

app = Flask(__name__)

# Configuration
LOG_FILE = "agent-log.txt"
SUCCESS_PREFIX = "SUCCESS_FOUND_"
YAML_PINS_FILE = "pins_master.yaml"
YAML_PROGRESS_FILE = "pins_progress.yaml"

class DashboardDataProcessor:
    """Process agent data for dashboard display"""
    
    def __init__(self):
        self.booking_data = defaultdict(lambda: {
            'pins_tried': 0,
            'total_attempts': 0,
            'agents_used': set(),
            'success_pin': None,
            'recent_attempts': [],
            'attempt_results': {'SUCCESS': 0, 'FAILURE': 0, 'EXCEPTION': 0},
            'first_attempt': None,
            'last_attempt': None
        })
        
    def load_log_data(self):
        """Load and process agent log data"""
        if not os.path.exists(LOG_FILE):
            return
            
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            all_attempts = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split(',')
                if len(parts) >= 5:
                    timestamp, booking_id, pin, result, url = parts[:5]
                    agent_id = f"Agent-{len(parts) > 5 and parts[5] or 'Unknown'}"
                    
                    attempt_data = {
                        'timestamp': timestamp,
                        'booking_id': booking_id,
                        'pin': pin,
                        'result': result,
                        'url': url,
                        'agent': agent_id
                    }
                    
                    all_attempts.append(attempt_data)
                    
                    # Update booking data
                    booking = self.booking_data[booking_id]
                    booking['total_attempts'] += 1
                    booking['agents_used'].add(agent_id)
                    booking['attempt_results'][result] += 1
                    
                    # Track PINs tried (unique)
                    if pin not in [a['pin'] for a in booking['recent_attempts']]:
                        booking['pins_tried'] += 1
                    
                    # Track success
                    if result == 'SUCCESS' and not booking['success_pin']:
                        booking['success_pin'] = pin
                    
                    # Update timestamps
                    if not booking['first_attempt']:
                        booking['first_attempt'] = timestamp
                    booking['last_attempt'] = timestamp
                    
                    # Add to recent attempts (keep last 15)
                    booking['recent_attempts'].append(attempt_data)
                    if len(booking['recent_attempts']) > 15:
                        booking['recent_attempts'] = booking['recent_attempts'][-15:]
            
            # Sort all booking data by most recent attempts
            for booking_id, data in self.booking_data.items():
                data['recent_attempts'].sort(key=lambda x: x['timestamp'], reverse=True)
                data['agents_used'] = len(data['agents_used'])
                
        except Exception as e:
            print(f"Error loading log data: {e}")
    
    def load_success_files(self):
        """Load success data from individual success files"""
        success_files = glob.glob(f"{SUCCESS_PREFIX}*.json")
        
        for success_file in success_files:
            try:
                with open(success_file, 'r') as f:
                    success_data = json.load(f)
                
                booking_id = success_data.get('booking_id')
                if booking_id and booking_id in self.booking_data:
                    self.booking_data[booking_id]['success_pin'] = success_data.get('success_pin')
                    self.booking_data[booking_id]['success_timestamp'] = success_data.get('timestamp')
                    self.booking_data[booking_id]['success_agent'] = success_data.get('agent_id', 'Unknown')
                    
            except Exception as e:
                print(f"Error loading success file {success_file}: {e}")
    
    def calculate_stats(self):
        """Calculate statistics for each booking"""
        for booking_id, data in self.booking_data.items():
            total_results = sum(data['attempt_results'].values())
            if total_results > 0:
                data['success_rate'] = round((data['attempt_results']['SUCCESS'] / total_results) * 100, 1)
                data['failure_rate'] = round((data['attempt_results']['FAILURE'] / total_results) * 100, 1)
                data['exception_rate'] = round((data['attempt_results']['EXCEPTION'] / total_results) * 100, 1)
            else:
                data['success_rate'] = data['failure_rate'] = data['exception_rate'] = 0
            
            # Calculate progress (assuming 10000 total PINs)
            data['progress_percentage'] = min(round((data['pins_tried'] / 10000) * 100, 1), 100)
    
    def get_combined_stats(self):
        """Get combined statistics across all bookings"""
        total_pins_tried = sum(data['pins_tried'] for data in self.booking_data.values())
        total_attempts = sum(data['total_attempts'] for data in self.booking_data.values())
        success_bookings = [bid for bid, data in self.booking_data.items() if data['success_pin']]
        
        if len(self.booking_data) > 0:
            overall_progress = round((len(success_bookings) / len(self.booking_data)) * 100, 1)
        else:
            overall_progress = 0
        
        return {
            'total_pins_tried': total_pins_tried,
            'total_attempts': total_attempts,
            'success_bookings': success_bookings,
            'total_bookings': len(self.booking_data),
            'overall_progress': overall_progress,
            'agents_active': len(set().union(*[data.get('agents_used', set()) for data in self.booking_data.values()]))
        }

# Global data processor
data_processor = DashboardDataProcessor()

@app.route('/')
def dashboard():
    """Serve the main dashboard HTML file"""
    return send_from_directory('.', 'bosss_ai_playwright_dashboard.html')

@app.route('/api/data')
def get_dashboard_data():
    """API endpoint to get all dashboard data"""
    # Reload data from files
    data_processor.__init__()  # Reset data
    data_processor.load_log_data()
    data_processor.load_success_files()
    data_processor.calculate_stats()
    
    # Convert defaultdict to regular dict for JSON serialization
    booking_data = {}
    for booking_id, data in data_processor.booking_data.items():
        booking_data[booking_id] = dict(data)
        # Convert set to int if it's still a set
        if isinstance(booking_data[booking_id]['agents_used'], set):
            booking_data[booking_id]['agents_used'] = len(booking_data[booking_id]['agents_used'])
    
    combined_stats = data_processor.get_combined_stats()
    
    return jsonify({
        'booking_data': booking_data,
        'combined_stats': combined_stats,
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_info': {
            'log_file_exists': os.path.exists(LOG_FILE),
            'log_file_size': os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0,
            'active_agents': get_active_agent_count()
        }
    })

@app.route('/api/agents')
def get_agent_status():
    """Get status of all agent files"""
    agent_files = glob.glob('boss_ai_playwright_*.py')
    agents = []
    
    for agent_file in agent_files:
        # Extract agent info from filename
        agent_name = os.path.splitext(agent_file)[0]
        
        # Check if agent has recent activity (last 5 minutes)
        recent_activity = False
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r') as f:
                    lines = f.readlines()
                
                # Check last few entries for this agent
                for line in reversed(lines[-20:]):  # Check last 20 entries
                    if agent_name in line:
                        timestamp_str = line.split(',')[0]
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        if datetime.now() - timestamp < timedelta(minutes=5):
                            recent_activity = True
                        break
            except:
                pass
        
        agents.append({
            'name': agent_name,
            'file': agent_file,
            'active': recent_activity,
            'file_size': os.path.getsize(agent_file)
        })
    
    return jsonify({'agents': agents})

def get_active_agent_count():
    """Count agents that have been active in the last 5 minutes"""
    if not os.path.exists(LOG_FILE):
        return 0
    
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        active_agents = set()
        cutoff_time = datetime.now() - timedelta(minutes=5)
        
        for line in reversed(lines[-50:]):  # Check last 50 entries
            parts = line.strip().split(',')
            if len(parts) >= 1:
                try:
                    timestamp = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')
                    if timestamp > cutoff_time:
                        # Extract agent from the line (you might need to adjust this based on your log format)
                        active_agents.add(f"Agent-{len(parts) > 5 and parts[5] or 'Unknown'}")
                    else:
                        break  # Lines are in chronological order
                except:
                    continue
        
        return len(active_agents)
    except:
        return 0

@app.route('/api/yaml_status')
def get_yaml_status():
    """Get status of YAML PIN management files"""
    yaml_status = {
        'pins_master_exists': os.path.exists(YAML_PINS_FILE),
        'pins_progress_exists': os.path.exists(YAML_PROGRESS_FILE),
        'total_pins_in_master': 0,
        'pins_allocated': 0,
        'pins_completed': 0
    }
    
    # Check master pins file
    if yaml_status['pins_master_exists']:
        try:
            with open(YAML_PINS_FILE, 'r') as f:
                master_data = yaml.safe_load(f)
            yaml_status['total_pins_in_master'] = len(master_data.get('pins', []))
        except:
            pass
    
    # Check progress file
    if yaml_status['pins_progress_exists']:
        try:
            with open(YAML_PROGRESS_FILE, 'r') as f:
                progress_data = yaml.safe_load(f)
            yaml_status['pins_allocated'] = len(progress_data.get('allocated', {}))
            yaml_status['pins_completed'] = len(progress_data.get('completed', {}))
        except:
            pass
    
    return jsonify(yaml_status)

if __name__ == '__main__':
    print("🎯 Starting Multi-Agent PIN Brute Force Dashboard")
    print("=" * 60)
    print(f"📊 Dashboard URL: http://localhost:5000")
    print(f"📋 Log file: {LOG_FILE}")
    print(f"💾 Data processing: Real-time from agent logs")
    print("=" * 60)
    
    # Create templates directory for any future templates
    os.makedirs('templates', exist_ok=True)
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
