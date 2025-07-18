@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                      🎯 TARGET PIN HUNTER LAUNCHER 🎯                        ║
echo ║                                                                              ║
echo ║  Target Booking ID: 5727559423                                              ║
echo ║  Each agent does 10 attempts                                                ║
echo ║  Multiple agents can run simultaneously                                     ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

set PYTHON_PATH=C:/Users/HP/Pablo_Agent/ghostform-runner/venv/Scripts/python.exe
set SCRIPT_PATH=target_pin_hunter_5727559423.py

echo Choose an option:
echo 1. Run single agent (10 attempts)
echo 2. Run 3 agents simultaneously
echo 3. Run 5 agents simultaneously
echo 4. Run demo
echo 5. Run test setup
echo.

set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting single agent...
    %PYTHON_PATH% %SCRIPT_PATH%
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Starting 3 agents simultaneously...
    start "Agent 1" %PYTHON_PATH% %SCRIPT_PATH%
    start "Agent 2" %PYTHON_PATH% %SCRIPT_PATH%
    start "Agent 3" %PYTHON_PATH% %SCRIPT_PATH%
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Starting 5 agents simultaneously...
    start "Agent 1" %PYTHON_PATH% %SCRIPT_PATH%
    start "Agent 2" %PYTHON_PATH% %SCRIPT_PATH%
    start "Agent 3" %PYTHON_PATH% %SCRIPT_PATH%
    start "Agent 4" %PYTHON_PATH% %SCRIPT_PATH%
    start "Agent 5" %PYTHON_PATH% %SCRIPT_PATH%
) else if "%choice%"=="4" (
    echo.
    echo 🎬 Running demo...
    %PYTHON_PATH% demo_target_hunter.py
) else if "%choice%"=="5" (
    echo.
    echo 🧪 Running test setup...
    %PYTHON_PATH% test_target_setup.py
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause
