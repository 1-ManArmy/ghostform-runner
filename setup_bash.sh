#!/bin/bash
# Quick setup script for Git Bash deployment

echo "🎯 STEALTH PIN HUNTER - GIT BASH SETUP"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Make the launcher executable
chmod +x launch_real_hunter_bash.sh

# Check if Python environment exists
if [ ! -f "venv/Scripts/python.exe" ]; then
    echo "❌ Python virtual environment not found!"
    echo "💡 Please run this in VS Code first to set up the environment"
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking required packages..."
if ! ./venv/Scripts/python.exe -c "import playwright, colorama" 2>/dev/null; then
    echo "❌ Required packages not installed!"
    echo "💡 Please run this in VS Code first to install packages"
    exit 1
fi

# Check if main script exists
if [ ! -f "real_pin_hunter_6160911170.py" ]; then
    echo "❌ Main hunter script not found!"
    exit 1
fi

echo "✅ All checks passed!"
echo "🚀 Ready for stealth operation!"
echo ""
echo "📋 To start hunting:"
echo "   ./launch_real_hunter_bash.sh"
echo ""
echo "🎯 Target: Booking ID 6160911170"
echo "🔍 Range: PIN 0000-9999"
echo "🕵️ Mode: Stealth + Proxy Automation"
echo "═══════════════════════════════════════════════════════════════════════════════"
