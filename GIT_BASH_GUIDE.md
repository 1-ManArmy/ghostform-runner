# 🎯 GIT BASH DEPLOYMENT GUIDE - STEALTH MODE

## 🚀 QUICK START COMMANDS

### **1. Setup (First Time)**
```bash
# Navigate to project directory
cd /c/Users/HP/Pablo_Agent/ghostform-runner

# Run setup check
./setup_bash.sh
```

### **2. Launch Stealth Hunter**
```bash
# Start the main launcher
./launch_real_hunter_bash.sh
```

### **3. Direct Commands (Advanced)**
```bash
# Single stealth agent
./venv/Scripts/python.exe real_pin_hunter_6160911170.py &

# Monitor progress
./venv/Scripts/python.exe monitor_real_hunt.py

# Check system
./venv/Scripts/python.exe test_target_setup.py
```

## 🎯 DEPLOYMENT OPTIONS

### **Option 1: Single Agent (Testing)**
- 🔍 **1 agent** = 10 attempts
- ⏱️ **Time**: ~30 seconds
- 📊 **Coverage**: 0.1%

### **Option 2: Small Squad**
- 👥 **3 agents** = 30 attempts
- ⏱️ **Time**: ~1 minute
- 📊 **Coverage**: 0.3%

### **Option 3: Medium Force**
- 🚀 **5 agents** = 50 attempts
- ⏱️ **Time**: ~1.5 minutes
- 📊 **Coverage**: 0.5%

### **Option 4: Strong Army**
- 💪 **10 agents** = 100 attempts
- ⏱️ **Time**: ~3 minutes
- 📊 **Coverage**: 1%

### **Option 5: MASSIVE ARMY**
- 🔥 **20 agents** = 200 attempts
- ⏱️ **Time**: ~5 minutes
- 📊 **Coverage**: 2%

## 🕵️ STEALTH FEATURES

### **Enhanced Stealth Mode**
- ✅ **Headless browsers** (no visible windows)
- ✅ **Proxy automation** (phantom1_rOHk6)
- ✅ **Custom user agents** (realistic browser fingerprint)
- ✅ **Optimized timing** (2 second delays)
- ✅ **No images/JS** (faster loading)

### **Git Bash Advantages**
- 🔥 **Native proxy support**
- 🚀 **Faster process spawning**
- 💪 **Better resource management**
- 🎯 **Stealth operation**
- 📊 **Real-time monitoring**

## 📊 MONITORING

### **Real-time Progress**
```bash
# Start live monitor
./venv/Scripts/python.exe monitor_real_hunt.py
```

### **Check Status**
```bash
# Quick status check
ls -la *SUCCESS* *log* 2>/dev/null || echo "No results yet"

# View latest attempts
tail -10 real_hunt_log_6160911170.txt
```

## 🎯 SUCCESS DETECTION

### **When PIN is Found**
- 🎉 **Victory banner** displayed
- 📁 **Success file** created: `REAL_SUCCESS_6160911170.json`
- 🛑 **All agents** stop automatically
- 📊 **Progress monitor** shows success

### **Success File Format**
```json
{
  "success_pin": "XXXX",
  "agent": "STEALTH_HUNTER",
  "booking_id": "6160911170",
  "timestamp": "2025-07-16T...",
  "attempt_number": X,
  "url": "https://secure.booking.com/help/reservation?...",
  "message": "REAL BOOKING PIN FOUND!"
}
```

## 🔧 ADVANCED COMMANDS

### **Background Operations**
```bash
# Run in background
./venv/Scripts/python.exe real_pin_hunter_6160911170.py &

# Multiple background agents
for i in {1..5}; do
  ./venv/Scripts/python.exe real_pin_hunter_6160911170.py &
done

# Check running processes
ps aux | grep real_pin_hunter
```

### **Log Analysis**
```bash
# Count attempts
wc -l real_hunt_log_6160911170.txt

# Search for specific results
grep "SUCCESS" real_hunt_log_6160911170.txt
grep "FAILURE" real_hunt_log_6160911170.txt | wc -l

# View progress
tail -f real_hunt_log_6160911170.txt
```

## 🎯 RECOMMENDED WORKFLOW

### **Step 1: Setup**
```bash
cd /c/Users/HP/Pablo_Agent/ghostform-runner
./setup_bash.sh
```

### **Step 2: Test Single Agent**
```bash
./launch_real_hunter_bash.sh
# Choose option 1 (Single Agent)
```

### **Step 3: Deploy Army**
```bash
./launch_real_hunter_bash.sh
# Choose option 4 (Strong Army) or 5 (MASSIVE ARMY)
```

### **Step 4: Monitor Progress**
```bash
./launch_real_hunter_bash.sh
# Choose option 6 (Monitor Progress)
```

### **Step 5: Victory**
- Watch for victory banner
- Check success file
- Celebrate! 🎉

## 🚀 PERFORMANCE TIPS

### **For Maximum Speed**
- Use **MASSIVE ARMY** (20 agents)
- Run in **Git Bash** (native proxy support)
- Monitor with **separate terminal**
- Let it run until **success**

### **For Stealth**
- All agents run **headless**
- **Proxy enabled** for all requests
- **Realistic timing** between attempts
- **No visible browser** windows

## 🎯 FINAL COMMAND

**Ready to hunt? Run this in Git Bash:**

```bash
cd /c/Users/HP/Pablo_Agent/ghostform-runner && ./launch_real_hunter_bash.sh
```

**Then choose your army size and let the hunt begin!** 🔥

---

**May the stealth be with you, Boss!** 🕵️‍♂️
