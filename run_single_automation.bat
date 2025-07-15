@echo off
echo ===================================================
echo          SINGLE BOOKING AUTOMATION LAUNCHER
echo ===================================================
echo.
echo Starting dashboard and agent runner...
echo.

REM Start the dashboard in the background
echo Starting dashboard on http://localhost:5000...
start "Dashboard" python single_dashboard.py

REM Wait a few seconds for dashboard to start
timeout /t 5 /nobreak >nul

REM Run the simple agent runner
echo Starting agent runner...
python simple_runner.py

echo.
echo ===================================================
echo            AUTOMATION COMPLETE
echo ===================================================
pause
