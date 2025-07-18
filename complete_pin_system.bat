@echo off
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                 🎯 COMPLETE PIN HUNTING SYSTEM 🎯                            ║
echo ║                                                                              ║
echo ║  Phase 1: Test 50 specific PINs for booking 5727559423                     ║
echo ║  Phase 2: Use discovered PIN for automation with other bookings            ║
echo ║  Phase 3: Launch army of agents for unknown bookings                       ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

set PYTHON_PATH=C:/Users/HP/Pablo_Agent/ghostform-runner/venv/Scripts/python.exe

:MAIN_MENU
echo.
echo 🎯 MAIN MENU - Choose your mission:
echo.
echo 1. 🔍 Test 50 specific PINs for booking 5727559423
echo 2. 🤖 Run automation system (requires Phase 1 success)
echo 3. 🚀 Launch army of random PIN hunters
echo 4. 📊 View results and logs
echo 5. 🧪 Run system tests
echo 6. 🎬 Run demo
echo 7. 🚪 Exit
echo.

set /p choice=Enter your choice (1-7): 

if "%choice%"=="1" goto PHASE1
if "%choice%"=="2" goto PHASE2
if "%choice%"=="3" goto PHASE3
if "%choice%"=="4" goto VIEW_RESULTS
if "%choice%"=="5" goto SYSTEM_TESTS
if "%choice%"=="6" goto DEMO
if "%choice%"=="7" goto EXIT

echo Invalid choice. Please try again.
goto MAIN_MENU

:PHASE1
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                     🔍 PHASE 1: TARGETED PIN TEST 🔍                        ║
echo ║                                                                              ║
echo ║  Testing 50 specific PINs for booking ID: 5727559423                       ║
echo ║  One of these PINs should be correct                                       ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo Starting targeted PIN test...
%PYTHON_PATH% targeted_pin_tester_5727559423.py

echo.
echo Phase 1 complete. Check results above.
pause
goto MAIN_MENU

:PHASE2
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                   🤖 PHASE 2: AUTOMATION SYSTEM 🤖                          ║
echo ║                                                                              ║
echo ║  Using discovered PIN to test other booking IDs                            ║
echo ║  Requires successful completion of Phase 1                                 ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo Starting automation system...
%PYTHON_PATH% automation_system.py

echo.
echo Phase 2 complete. Check results above.
pause
goto MAIN_MENU

:PHASE3
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                    🚀 PHASE 3: ARMY DEPLOYMENT 🚀                           ║
echo ║                                                                              ║
echo ║  Launch multiple agents for random PIN hunting                             ║
echo ║  Each agent does 10 attempts then returns home                             ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo Choose army size:
echo 1. Single agent (10 attempts)
echo 2. Squad of 3 agents (30 attempts)
echo 3. Platoon of 5 agents (50 attempts)
echo 4. Company of 10 agents (100 attempts)
echo.

set /p army_choice=Enter choice (1-4): 

if "%army_choice%"=="1" (
    echo Deploying single agent...
    %PYTHON_PATH% target_pin_hunter_5727559423.py
) else if "%army_choice%"=="2" (
    echo Deploying squad of 3 agents...
    start "Agent 1" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 2" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 3" %PYTHON_PATH% target_pin_hunter_5727559423.py
) else if "%army_choice%"=="3" (
    echo Deploying platoon of 5 agents...
    start "Agent 1" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 2" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 3" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 4" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 5" %PYTHON_PATH% target_pin_hunter_5727559423.py
) else if "%army_choice%"=="4" (
    echo Deploying company of 10 agents...
    start "Agent 1" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 2" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 3" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 4" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 5" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 6" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 7" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 8" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 9" %PYTHON_PATH% target_pin_hunter_5727559423.py
    start "Agent 10" %PYTHON_PATH% target_pin_hunter_5727559423.py
) else (
    echo Invalid choice.
)

echo.
echo Phase 3 deployment complete.
pause
goto MAIN_MENU

:VIEW_RESULTS
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                        📊 RESULTS & LOGS 📊                                 ║
echo ║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo Checking results files...
echo.

if exist "TARGETED_SUCCESS_5727559423.json" (
    echo ✅ PHASE 1 SUCCESS FOUND:
    type "TARGETED_SUCCESS_5727559423.json"
    echo.
) else (
    echo ❌ Phase 1: No success file found
)

if exist "AUTOMATION_SUCCESS_*.json" (
    echo ✅ PHASE 2 AUTOMATION SUCCESSES:
    for %%f in (AUTOMATION_SUCCESS_*.json) do (
        echo --- %%f ---
        type "%%f"
        echo.
    )
) else (
    echo ❌ Phase 2: No automation success files found
)

if exist "TARGET_SUCCESS_5727559423.json" (
    echo ✅ PHASE 3 ARMY SUCCESS:
    type "TARGET_SUCCESS_5727559423.json"
    echo.
) else (
    echo ❌ Phase 3: No army success file found
)

echo.
echo Log files:
if exist "targeted_test_log_5727559423.txt" echo - targeted_test_log_5727559423.txt
if exist "automation_system_log.txt" echo - automation_system_log.txt
if exist "target_hunt_log_5727559423.txt" echo - target_hunt_log_5727559423.txt

echo.
pause
goto MAIN_MENU

:SYSTEM_TESTS
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                        🧪 SYSTEM TESTS 🧪                                   ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo Running system tests...
%PYTHON_PATH% test_target_setup.py

echo.
pause
goto MAIN_MENU

:DEMO
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                           🎬 DEMO MODE 🎬                                    ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo Running demo...
%PYTHON_PATH% demo_target_hunter.py

echo.
pause
goto MAIN_MENU

:EXIT
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                    👋 THANK YOU FOR USING THE SYSTEM 👋                     ║
echo ║                                                                              ║
echo ║                         🎯 HAPPY HUNTING! 🎯                                ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
pause
exit
