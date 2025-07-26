@echo off
echo ======================================
echo  MASTER AUTOMATION FOR PIN TESTING
echo ======================================
echo.
echo This will run all 27 files automatically:
echo - Primary file: boss_ai_playwright.py
echo - Then A to Z files sequentially
echo - Stops when PIN is found
echo.
echo Usage Examples:
echo   run_automation.bat
echo   run_automation.bat --confirmation 1234567890 --pins "1000,2000,3000" --wait 30
echo   run_automation.bat --headless --delay 10
echo.
echo Press Ctrl+C to stop anytime
echo.
echo Starting automation...
echo.

python master_automation.py %*
