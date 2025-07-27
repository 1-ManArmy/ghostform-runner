# 🎯 Multi-Agent PIN Brute Force Dashboard

**Professional monitoring system for distributed booking.com PIN testing with proxy rotation**

## 📊 Dashboard Features

### Real-Time Monitoring
- **Live agent activity tracking** - See which agents are currently active
- **Real-time attempt monitoring** - Watch PIN attempts as they happen
- **Success/failure rate tracking** - Monitor overall system performance
- **Proxy rotation status** - Track agent proxy usage

### Professional Interface
- **Multi-booking support** - Monitor multiple booking IDs simultaneously
- **Interactive charts** - Visual representation of attempt results
- **Export functionality** - Generate reports and data exports
- **Auto-refresh** - Automatic updates every 30 seconds

### System Overview
- **Total PINs tried** across all agents and bookings
- **Total attempts** including retries and exceptions
- **Active agents** currently running and making attempts
- **Overall success rate** across the entire operation

## 🚀 Quick Start

### Method 1: Batch File (Windows)
```cmd
# Double-click or run from command prompt
launch_dashboard.bat
```

### Method 2: Python Launcher
```bash
python launch_dashboard.py
```

### Method 3: Direct Server Start
```bash
# Install dependencies
pip install flask pyyaml

# Start dashboard server
python dashboard_server.py
```

### Method 4: Manual Flask Run
```bash
# For development/debugging
python -m flask --app dashboard_server run --host=0.0.0.0 --port=5000
```

## 📱 Dashboard Access

Once started, access the dashboard at:
- **Local:** http://localhost:5000
- **Network:** http://YOUR_IP:5000 (accessible from other devices)

## 📋 Data Sources

The dashboard reads from:

### 1. Agent Log File (`agent-log.txt`)
```csv
timestamp,booking_id,pin,result,url,agent_id
2025-07-21 03:06:54,5724349472,6054,EXCEPTION,https://secure.booking.com/help/confirmation_pin_auth,Agent-1
2025-07-21 03:11:06,5871858498,1985,SUCCESS,https://secure.booking.com/help/confirmation_pin_auth,Agent-2
```

### 2. Success Files (`SUCCESS_FOUND_*.json`)
```json
{
  "booking_id": "5871858498",
  "success_pin": "1985",
  "timestamp": "2025-07-21 03:11:06",
  "agent_id": "Agent-2",
  "attempt_number": 47
}
```

### 3. YAML PIN Management (Optional)
- `pins_master.yaml` - Master list of all PINs
- `pins_progress.yaml` - Allocation and completion tracking

## 🎛️ Dashboard Controls

### Refresh Controls
- **🔄 Refresh** - Manually update dashboard data
- **⏱️ Auto-Refresh** - Toggle automatic 30-second updates

### Agent Management
- **🤖 Agent Status** - View active/idle agent status
- **📊 Export Data** - Download session reports as JSON

## 📊 Dashboard Sections

### 1. System Overview
- **Total PINs Tried** - Unique PINs attempted across all bookings
- **Total Attempts** - All attempts including retries
- **Active Agents** - Currently running agents (last 5 minutes)
- **Total Bookings** - Number of booking IDs being tested
- **Success Rate** - Overall success percentage
- **System Status** - Current operational status

### 2. Booking Sections
Each booking ID gets its own section showing:
- **Booking ID** and current status (SUCCESS/SEARCHING)
- **Success alert** with found PIN (if successful)
- **Statistics**: PINs tried, attempts, agents used, success rate
- **Progress bar** showing completion percentage
- **Interactive chart** showing attempt result distribution
- **Recent attempts** log with timestamps and results

## 🔧 Configuration

### Server Configuration
Edit `dashboard_server.py` to modify:
```python
# Files to monitor
LOG_FILE = "agent-log.txt"
SUCCESS_PREFIX = "SUCCESS_FOUND_"
YAML_PINS_FILE = "pins_master.yaml"
YAML_PROGRESS_FILE = "pins_progress.yaml"

# Server settings
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Dashboard Customization
Edit `bosss_ai_playwright_dashboard.html` to modify:
- Auto-refresh interval (default: 30 seconds)
- Chart types and colors
- UI layout and styling
- Additional features and controls

## 🛠️ API Endpoints

The dashboard provides REST API endpoints:

### `/api/data` - Main Dashboard Data
```json
{
  "booking_data": {
    "5871858498": {
      "pins_tried": 47,
      "total_attempts": 52,
      "success_pin": "1985",
      "recent_attempts": [...],
      "success_rate": 8.5
    }
  },
  "combined_stats": {
    "total_pins_tried": 47,
    "total_attempts": 52,
    "agents_active": 3,
    "total_bookings": 1
  },
  "last_update": "2025-07-21 15:30:45"
}
```

### `/api/agents` - Agent Status
```json
{
  "agents": [
    {
      "name": "boss_ai_playwright_1A",
      "file": "boss_ai_playwright_1A.py",
      "active": true,
      "file_size": 15842
    }
  ]
}
```

### `/api/yaml_status` - YAML File Status
```json
{
  "pins_master_exists": true,
  "pins_progress_exists": true,
  "total_pins_in_master": 10000,
  "pins_allocated": 150,
  "pins_completed": 47
}
```

## 🔍 Troubleshooting

### Dashboard Won't Start
1. Check Python installation: `python --version`
2. Install Flask: `pip install flask pyyaml`
3. Check port availability: `netstat -an | findstr :5000`
4. Run with debug: `python dashboard_server.py`

### No Data Showing
1. Verify `agent-log.txt` exists and has data
2. Check log file format matches expected CSV structure
3. Ensure agents are writing to the correct log file
4. Check file permissions

### Agents Not Showing as Active
1. Agents must write to log file within last 5 minutes
2. Check agent log format includes timestamp as first column
3. Verify agents are actually running and making attempts

### Browser Issues
1. Try different browser or incognito mode
2. Clear browser cache and cookies
3. Check JavaScript console for errors
4. Ensure network connectivity to dashboard server

## 📈 Performance Tips

### For Large Scale Operations (1000+ Agents)
1. **Enable log rotation** to prevent huge log files
2. **Use SSD storage** for faster file I/O
3. **Monitor RAM usage** during heavy operations
4. **Consider database storage** for very large datasets

### Dashboard Optimization
1. **Adjust auto-refresh interval** based on system load
2. **Limit recent attempts** display to last 10-15 entries
3. **Use browser performance tools** to monitor resource usage
4. **Close unused browser tabs** when running intensive operations

## 🔒 Security Notes

### Development vs Production
- **Current setup is for development** with debug mode enabled
- **For production use**, deploy with proper WSGI server (gunicorn, uwsgi)
- **Add authentication** for production environments
- **Use HTTPS** in production deployments

### Network Security
- **Dashboard runs on all interfaces** (0.0.0.0) for network access
- **Consider firewall rules** if exposing to network
- **Monitor access logs** for unauthorized access attempts

## 📞 Support & Integration

### Integration with Agent System
The dashboard automatically detects and works with:
- All `boss_ai_playwright_*.py` agent files
- The `agent-log.txt` logging system
- Success files with `SUCCESS_FOUND_` prefix
- YAML PIN management files (when implemented)

### Future Enhancements
- **Database integration** for persistent storage
- **Email/SMS alerts** for successful PIN discoveries
- **Advanced analytics** and trend analysis
- **Multi-user support** with role-based access
- **Real-time WebSocket updates** for instant notifications

---

**🎯 Ready to monitor your PIN brute force operation like a pro!**

Start the dashboard, launch your agents, and watch the magic happen in real-time.
