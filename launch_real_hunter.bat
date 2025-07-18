@echo off
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                    🎯 REAL PIN HUNTER LAUNCHER 🎯                            ║
echo ║                                                                              ║
echo ║  Real Booking ID: 6160911170                                                ║
echo ║  Mission: Find correct PIN from 0000-9999                                  ║
echo ║  Strategy: Deploy multiple agents (10 attempts each)                       ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

set PYTHON_PATH=C:/Users/HP/Pablo_Agent/ghostform-runner/venv/Scripts/python.exe
set SCRIPT_PATH=real_pin_hunter_6160911170.py

echo 🎯 Choose your deployment strategy:
echo.
echo 1. 🔍 Single agent test (10 attempts)
echo 2. 👥 Small squad (3 agents = 30 attempts)
echo 3. 🚀 Medium force (5 agents = 50 attempts)
echo 4. 💪 Strong army (10 agents = 100 attempts)
echo 5. 🔥 MASSIVE ARMY (20 agents = 200 attempts)
echo 6. 📊 View current progress
echo 7. 🧪 Test system
echo 8. 🚪 Exit
echo.

set /p choice=Enter your choice (1-8): 

if "%choice%"=="1" (
    echo.
    echo 🔍 Deploying single agent for testing...
    echo ⚠️  Browser will be visible for monitoring
    %PYTHON_PATH% %SCRIPT_PATH%
) else if "%choice%"=="2" (
    echo.
    echo 👥 Deploying small squad (3 agents)...
    start "Real Hunter 1" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 2" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 3" %PYTHON_PATH% %SCRIPT_PATH%
    echo 🚀 3 agents deployed! Each will try 10 PINs then return home.
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Deploying medium force (5 agents)...
    start "Real Hunter 1" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 2" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 3" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 4" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 5" %PYTHON_PATH% %SCRIPT_PATH%
    echo 🚀 5 agents deployed! Total: 50 PIN attempts.
) else if "%choice%"=="4" (
    echo.
    echo 💪 Deploying strong army (10 agents)...
    start "Real Hunter 1" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 2" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 3" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 4" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 5" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 6" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 7" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 8" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 9" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 10" %PYTHON_PATH% %SCRIPT_PATH%
    echo 🚀 10 agents deployed! Total: 100 PIN attempts.
) else if "%choice%"=="5" (
    echo.
    echo 🔥 DEPLOYING MASSIVE ARMY (20 agents)...
    echo ⚠️  This is serious business!
    start "Real Hunter 1" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 2" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 3" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 4" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 5" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 6" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 7" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 8" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 9" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 10" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 11" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 12" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 13" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 14" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 15" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 16" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 17" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 18" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 19" %PYTHON_PATH% %SCRIPT_PATH%
    start "Real Hunter 20" %PYTHON_PATH% %SCRIPT_PATH%
    echo 🔥 20 agents deployed! Total: 200 PIN attempts.
    echo 🎯 This should give us excellent coverage!
) else if "%choice%"=="6" (
    echo.
    echo 📊 CHECKING CURRENT PROGRESS...
    echo.
    if exist "REAL_SUCCESS_6160911170.json" (
        echo ✅ SUCCESS FOUND!
        type "REAL_SUCCESS_6160911170.json"
    ) else (
        echo ⏳ No success yet, hunt continues...
    )
    echo.
    if exist "real_hunt_log_6160911170.txt" (
        echo 📋 Latest attempts:
        powershell "Get-Content real_hunt_log_6160911170.txt | Select-Object -Last 10"
    ) else (
        echo 📋 No log file found yet
    )
) else if "%choice%"=="7" (
    echo.
    echo 🧪 Running system test...
    %PYTHON_PATH% test_target_setup.py
) else if "%choice%"=="8" (
    echo.
    echo 👋 Goodbye! Happy hunting!
    exit
) else (
    echo Invalid choice. Please try again.
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🎯 MISSION STATUS: AGENTS DEPLOYED
echo 📋 Booking ID: 6160911170
echo 🔍 Hunt in progress...
echo 💡 Check progress with option 6
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
