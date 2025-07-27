from flask import Flask, render_template, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuration for Speed Hunter monitoring
BOOKING_ID = "5727559423"
LOG_FILE = f"speed_hunt_log_{BOOKING_ID}.txt"
SUCCESS_FILE = f"SUCCESS_FOUND_{BOOKING_ID}.json"

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """Get current hunting status"""
    status = {
        'booking_id': BOOKING_ID,
        'total_attempts': 0,
        'success_found': False,
        'success_pin': None,
        'recent_attempts': [],
        'last_activity': None,
        'speed_hunter_active': True
    }
    
    # Check for success
    if os.path.exists(SUCCESS_FILE):
        try:
            with open(SUCCESS_FILE, 'r') as f:
                success_data = json.load(f)
            status['success_found'] = True
            status['success_pin'] = success_data.get('success_pin')
            status['success_timestamp'] = success_data.get('timestamp')
            status['attempt_number'] = success_data.get('attempt_number')
        except:
            pass
    
    # Read log file for progress
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                lines = f.readlines()
            
            status['total_attempts'] = len(lines)
            
            # Get recent attempts (last 10)
            recent_lines = lines[-10:] if len(lines) > 10 else lines
            for line in recent_lines:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    status['recent_attempts'].append({
                        'timestamp': parts[0],
                        'pin': parts[3],
                        'result': parts[4]
                    })
            
            # Get last activity
            if lines:
                last_line = lines[-1]
                parts = last_line.strip().split(',')
                if len(parts) >= 1:
                    status['last_activity'] = parts[0]
        except:
            pass
    
    return jsonify(status)

@app.route('/api/target_pins')
def get_target_pins():
    """Get list of target PINs"""
    target_pins = [
        "8745", "7864", "9636", "2537", "1083", "4729", "6591", "2376", "9854", "7162",
        "3407", "8941", "6215", "5038", "7920", "3816", "4359", "2684", "1973", "8496",
        "6027", "9345", "7812", "4108", "3590", "6843", "2257", "9174", "3065", "4732",
        "5648", "7291", "8126", "6580", "2491", "3906", "8753", "6420", "1235", "9867",
        "3072", "6184", "4721", "7913", "3850", "2486", "9615", "1348", "2390", "7249"
    ]
    return jsonify({'target_pins': target_pins, 'total_pins': len(target_pins)})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Speed Hunter Dashboard</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        .success {
            background: rgba(0,255,0,0.2);
            border-color: #00ff00;
        }
        .recent-attempts {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .attempt-item {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .result-success { color: #00ff00; font-weight: bold; }
        .result-failure { color: #ff6b6b; }
        .result-exception { color: #ffa500; }
        .target-pins {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
        }
        .pins-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .pin-item {
            background: rgba(255,255,255,0.1);
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .pin-tested { background: rgba(255,0,0,0.2); }
        .pin-success { background: rgba(0,255,0,0.2); border-color: #00ff00; }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Speed Hunter Dashboard</h1>
            <h2>Booking ID: <span id="booking-id"></span></h2>
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh</button>
        </div>

        <div class="stats-grid">
            <div class="stat-card" id="attempts-card">
                <div class="stat-label">Total Attempts</div>
                <div class="stat-value" id="total-attempts">0</div>
            </div>
            <div class="stat-card" id="success-card">
                <div class="stat-label">Success Status</div>
                <div class="stat-value" id="success-status">🔍 Hunting...</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Last Activity</div>
                <div class="stat-value" id="last-activity">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Speed</div>
                <div class="stat-value">⚡ Maximum</div>
            </div>
        </div>

        <div class="recent-attempts">
            <h3>🔄 Recent Attempts</h3>
            <div id="recent-attempts-list">
                <div class="attempt-item">
                    <span>No attempts yet...</span>
                </div>
            </div>
        </div>

        <div class="target-pins">
            <h3>🎯 Target PINs (50 total)</h3>
            <div class="pins-grid" id="pins-grid">
                <!-- Pins will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        let targetPins = [];
        let testedPins = [];
        let successPin = null;

        function refreshData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('booking-id').textContent = data.booking_id;
                    document.getElementById('total-attempts').textContent = data.total_attempts;
                    document.getElementById('last-activity').textContent = data.last_activity || '-';
                    
                    // Update success status
                    const successCard = document.getElementById('success-card');
                    const successStatus = document.getElementById('success-status');
                    if (data.success_found) {
                        successStatus.textContent = '🎉 SUCCESS!';
                        successCard.classList.add('success');
                        successPin = data.success_pin;
                    } else {
                        successStatus.textContent = '🔍 Hunting...';
                        successCard.classList.remove('success');
                    }
                    
                    // Update recent attempts
                    const recentList = document.getElementById('recent-attempts-list');
                    recentList.innerHTML = '';
                    
                    testedPins = [];
                    data.recent_attempts.forEach(attempt => {
                        const item = document.createElement('div');
                        item.className = 'attempt-item';
                        
                        let resultClass = '';
                        if (attempt.result === 'SUCCESS') resultClass = 'result-success';
                        else if (attempt.result === 'FAILURE') resultClass = 'result-failure';
                        else resultClass = 'result-exception';
                        
                        item.innerHTML = `
                            <span>${attempt.timestamp}</span>
                            <span>PIN: ${attempt.pin}</span>
                            <span class="${resultClass}">${attempt.result}</span>
                        `;
                        recentList.appendChild(item);
                        
                        testedPins.push(attempt.pin);
                    });
                    
                    updatePinsGrid();
                })
                .catch(error => console.error('Error fetching status:', error));
        }

        function loadTargetPins() {
            fetch('/api/target_pins')
                .then(response => response.json())
                .then(data => {
                    targetPins = data.target_pins;
                    updatePinsGrid();
                })
                .catch(error => console.error('Error fetching target pins:', error));
        }

        function updatePinsGrid() {
            const pinsGrid = document.getElementById('pins-grid');
            pinsGrid.innerHTML = '';
            
            targetPins.forEach(pin => {
                const pinItem = document.createElement('div');
                pinItem.className = 'pin-item';
                pinItem.textContent = pin;
                
                if (pin === successPin) {
                    pinItem.classList.add('pin-success');
                    pinItem.textContent += ' ✅';
                } else if (testedPins.includes(pin)) {
                    pinItem.classList.add('pin-tested');
                }
                
                pinsGrid.appendChild(pinItem);
            });
        }

        // Load data on page load
        loadTargetPins();
        refreshData();
        
        // Auto-refresh every 5 seconds
        setInterval(refreshData, 5000);
    </script>
</body>
</html>
    '''
    
    # Write the HTML template
    with open('templates/dashboard.html', 'w') as f:
        f.write(html_template)
    
    print("🚀 Speed Hunter Dashboard starting...")
    print("📊 Dashboard URL: http://localhost:5000")
    print("🎯 Monitoring booking ID: " + BOOKING_ID)
    print("="*50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
                print(f"❓ PIN {pin} is UNDETERMINED (no clear result)")
                page.screenshot(path=f"{SCREEN_DIR}/{CONFIRMATION}_{pin}_UNDETERMINED.png")
                log_result(pin, "UNDETERMINED", current_url)
                undetermined_count += 1
                print("❓ UNDETERMINED RESULT! Pausing 10 seconds to see the page...")
                time.sleep(10)  # Pause to see the page