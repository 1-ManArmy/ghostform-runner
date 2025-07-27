@echo off
setlocal enabledelayedexpansion
color 0A

echo.
echo ===============================================================
echo                🎯 GHOSTFORM AUTO MISSION CONTROL 🎯
echo ===============================================================
echo 🔄 Auto-Loop: 10 Cycles of A→B→C→D
echo 📊 Total Tests: 200 PINs (4 agents × 5 PINs × 10 cycles)
echo 🎯 Target Bookings: 6339614781, 6860261353, 6160911170, 5830944764
echo ===============================================================
echo.

set /a total_cycles=10
set /a current_cycle=0

:CYCLE_LOOP
set /a current_cycle+=1

echo.
echo ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
echo                    🚀 CYCLE %current_cycle% of %total_cycles% STARTING 🚀
echo ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
echo.

REM Agent A - ALPHA HUNTER
echo.
echo 🔵 DEPLOYING AGENT A - ALPHA HUNTER
echo 📋 Target: 6339614781 (Boss provided)
echo 🔑 Generating 5 random PINs...
echo.
python agent_A.py
if %errorlevel% equ 0 (
    echo ✅ Agent A completed successfully
) else (
    echo ⚠️ Agent A finished with warnings
)

REM Brief pause between agents
echo.
echo ⏸️ Tactical pause... (5 seconds)
timeout /t 5 /nobreak >nul

REM Agent B - BRAVO HUNTER  
echo.
echo 🟠 DEPLOYING AGENT B - BRAVO HUNTER
echo 📋 Target: 6860261353 (Boss provided)
echo 🔑 Generating 5 random PINs...
echo.
python agent_B.py
if %errorlevel% equ 0 (
    echo ✅ Agent B completed successfully
) else (
    echo ⚠️ Agent B finished with warnings
)

REM Brief pause between agents
echo.
echo ⏸️ Tactical pause... (5 seconds)
timeout /t 5 /nobreak >nul

REM Agent C - CHARLIE HUNTER
echo.
echo 🟡 DEPLOYING AGENT C - CHARLIE HUNTER
echo 📋 Target: 6160911170 (Boss provided)
echo 🔑 Generating 5 random PINs...
echo.
python agent_C.py
if %errorlevel% equ 0 (
    echo ✅ Agent C completed successfully
) else (
    echo ⚠️ Agent C finished with warnings
)

REM Brief pause between agents
echo.
echo ⏸️ Tactical pause... (5 seconds)
timeout /t 5 /nobreak >nul

REM Agent D - DELTA HUNTER
echo.
echo 🔴 DEPLOYING AGENT D - DELTA HUNTER
echo 📋 Target: 5830944764 (Boss provided)
echo 🔑 Generating 5 random PINs...
echo.
python agent_D.py
if %errorlevel% equ 0 (
    echo ✅ Agent D completed successfully
) else (
    echo ⚠️ Agent D finished with warnings
)

echo.
echo 🎉 CYCLE %current_cycle% COMPLETED! 
echo.

REM Check if we should continue
if %current_cycle% lss %total_cycles% (
    echo ⏳ Preparing for next cycle... (10 seconds)
    timeout /t 10 /nobreak >nul
    goto CYCLE_LOOP
)

REM Mission Complete
echo.
echo ===============================================================
echo                   🏆 MISSION COMPLETE! 🏆
echo ===============================================================
echo ✅ Total Cycles Completed: %total_cycles%
echo 📊 Total PIN Tests: 200 (estimated)
echo 🎯 Check mission_log_*.csv files for results
echo 🏆 Check for any SUCCESS entries in logs!
echo ===============================================================
echo.

REM Check for victories
echo 🔍 Scanning for victories...
echo.

if exist mission_log_A.csv (
    echo 📊 Agent A Log Found:
    findstr "SUCCESS" mission_log_A.csv 2>nul
    if errorlevel 1 (
        echo    No victories yet for Agent A
    )
    echo.
)

if exist mission_log_B.csv (
    echo 📊 Agent B Log Found:
    findstr "SUCCESS" mission_log_B.csv 2>nul
    if errorlevel 1 (
        echo    No victories yet for Agent B
    )
    echo.
)

if exist mission_log_C.csv (
    echo 📊 Agent C Log Found:
    findstr "SUCCESS" mission_log_C.csv 2>nul
    if errorlevel 1 (
        echo    No victories yet for Agent C
    )
    echo.
)

if exist mission_log_D.csv (
    echo 📊 Agent D Log Found:
    findstr "SUCCESS" mission_log_D.csv 2>nul
    if errorlevel 1 (
        echo    No victories yet for Agent D
    )
    echo.
)

echo 🎯 Auto-Mission Complete! Press any key to exit...
pause >nul
