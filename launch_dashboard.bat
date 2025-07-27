@echo off
echo 🎯 Multi-Agent PIN Brute Force Dashboard Launcher
echo ============================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is available

echo.
echo Installing/Checking Flask and PyYAML...
python -m pip install flask pyyaml --quiet
if errorlevel 1 (
    echo ⚠️  Warning: Could not install Flask. Trying anyway...
) else (
    echo ✅ Flask and PyYAML ready
)

echo.
echo 🚀 Starting Multi-Agent Dashboard Server...
echo 📊 Dashboard URL: http://localhost:5000
echo 🔧 Press Ctrl+C to stop the server
echo ============================================================
echo.

start "" "http://localhost:5000"
python dashboard_server.py

echo.
echo 🛑 Dashboard server stopped
pause
