# Master Automation System for PIN Testing

## Overview
This system automatically runs all 27 PIN testing files sequentially:
- **Primary file**: `boss_ai_playwright.py`
- **A-Z files**: `boss_ai_playwright_A.py` through `boss_ai_playwright_Z.py`

The system stops immediately when any file finds the correct PIN (SUCCESS), or continues through all files if no PIN is found.

## Features
- ✅ **Sequential Execution**: Runs files one by one automatically
- ✅ **Auto-Stop on Success**: Stops immediately when PIN is found
- ✅ **Comprehensive Logging**: Tracks all activities in log files
- ✅ **Proxy Support**: All files include Oxylabs proxy credentials
- ✅ **Configurable Parameters**: Customizable confirmation, PINs, timing
- ✅ **Error Handling**: Continues even if individual files fail

## Quick Start

### Method 1: Using Batch File (Recommended)
```batch
run_automation.bat
```

### Method 2: Using PowerShell
```powershell
.\run_automation.ps1
```

### Method 3: Direct Python
```bash
python master_automation.py
```

## Configuration Options

### Basic Usage
```bash
# Default settings
python master_automation.py

# Custom confirmation and PINs
python master_automation.py --confirmation 1234567890 --pins "1000,2000,3000,4000"

# Headless mode with custom timing
python master_automation.py --headless --wait 30 --delay 10
```

### Parameters
- `--confirmation`: Booking confirmation number (default: "1234567890")
- `--pins`: Comma-separated PIN list (default: "1,2,3,4")
- `--wait`: Wait time between PIN attempts in seconds (default: 60)
- `--headless`: Run browsers in headless mode (default: false)
- `--delay`: Delay between switching files in seconds (default: 30)

## File Structure
```
ghostform-runner/
├── boss_ai_playwright.py          # Primary file
├── boss_ai_playwright_A.py        # File A
├── boss_ai_playwright_B.py        # File B
├── ...                           # Files C through Y
├── boss_ai_playwright_Z.py        # File Z
├── master_automation.py           # Main automation script
├── run_automation.bat             # Windows batch launcher
├── run_automation.ps1             # PowerShell launcher
├── agent-log.txt                  # Individual agent results
├── master-automation-log.txt      # Master automation log
└── screenshots/                   # Screenshot directory
```

## Logging System

### Agent Log (`agent-log.txt`)
Records all PIN testing attempts:
```
2025-07-15 14:30:25,1234567890,1000,FAILURE,https://secure.booking.com/help/confirmation_pin_auth
2025-07-15 14:31:30,1234567890,2000,SUCCESS,https://secure.booking.com/help/confirmation_pin_auth?unique_order_id=123
```

### Master Log (`master-automation-log.txt`)
Tracks automation flow:
```
2025-07-15 14:30:20 - MASTER: === MASTER AUTOMATION STARTED ===
2025-07-15 14:30:21 - MASTER: [1/27] Processing: boss_ai_playwright.py
2025-07-15 14:31:35 - MASTER: 🎉 SUCCESS! PIN found by agent: boss_ai_playwright.py
```

## Process Flow
1. **Start**: Master automation begins
2. **Primary File**: Runs `boss_ai_playwright.py` first
3. **Check Result**: If PIN found → STOP, if not → continue
4. **File A**: Runs `boss_ai_playwright_A.py`
5. **Check Result**: If PIN found → STOP, if not → continue
6. **Continue**: Proceeds through B, C, D... until Z
7. **Final Report**: Shows summary of all attempts

## Success Scenarios
- ✅ **PIN Found**: System stops immediately and logs success
- ✅ **File Error**: System continues with next file
- ✅ **Timeout**: System moves to next file after 1 hour
- ✅ **Manual Stop**: Press Ctrl+C to stop anytime

## Proxy Configuration
All files include Oxylabs proxy credentials:
- **Server**: `pr.oxylabs.io:7777`
- **Username**: `customer-Oxylab_WFqvh`
- **Password**: `Oxylab_WFqvh1`

## Examples

### Example 1: Basic Run
```bash
python master_automation.py --confirmation 5871858498 --pins "1000,2000,3000,4000,5000"
```

### Example 2: Fast Testing
```bash
python master_automation.py --headless --wait 10 --delay 5
```

### Example 3: Extensive PIN Range
```bash
python master_automation.py --pins "1000,1001,1002,1003,1004,1005,1006,1007,1008,1009"
```

## Troubleshooting

### Common Issues
1. **File Not Found**: Ensure all 27 files exist in the directory
2. **Python Error**: Check if Python and Playwright are installed
3. **Proxy Issues**: Verify proxy credentials are correct
4. **Timeout**: Increase wait time if site is slow

### Installation Requirements
```bash
pip install playwright
playwright install chromium
```

## Safety Features
- **Automatic Logging**: All activities are logged
- **Error Recovery**: Continues even if files crash
- **Screenshot Capture**: Screenshots saved for each attempt
- **Timeout Protection**: Prevents infinite hanging

## Monitoring
- Watch `master-automation-log.txt` for real-time progress
- Check `agent-log.txt` for detailed PIN results
- Monitor `screenshots/` folder for visual confirmations

---

**Important**: This system is designed for legitimate booking confirmation recovery only. Use responsibly and in compliance with booking.com's terms of service.
