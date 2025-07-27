# 🎯 MISSION DEPLOYMENT SCRIPT
# Deploy all 4 agents with random PIN assignments

Write-Host "🎯 GHOSTFORM MISSION DEPLOYMENT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🎯 4 Agents, 5 Random PINs Each (0000-9999)" -ForegroundColor Yellow
Write-Host "📋 Mission Config: mission.yml" -ForegroundColor Green
Write-Host "🎖️ Proven Strategy: Boss's Best Script" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`n🚀 CONFIRMED WORKING PINS:" -ForegroundColor Green
Write-Host "✅ Booking 5871858498 → PIN 1965 (SUCCESS)" -ForegroundColor Green
Write-Host "✅ Booking 5727559423 → PIN 2390 (SUCCESS)" -ForegroundColor Green
Write-Host "`n🎯 Target Bookings:" -ForegroundColor Yellow
Write-Host "🔍 Booking 6860261353" -ForegroundColor Yellow
Write-Host "🔍 Booking 6339614781" -ForegroundColor Yellow

$agents = @("A", "B", "C", "D")
$agentNames = @("ALPHA_HUNTER", "BRAVO_HUNTER", "CHARLIE_HUNTER", "DELTA_HUNTER")

for ($i = 0; $i -lt $agents.Length; $i++) {
    $agent = $agents[$i]
    $agentName = $agentNames[$i]
    
    Write-Host "`n🚀 DEPLOYING AGENT $agent ($agentName)" -ForegroundColor Magenta
    Write-Host "Generating 5 random PINs from 0000-9999..." -ForegroundColor White
    
    try {
        python "agent_$agent.py"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Agent $agent mission complete" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Agent $agent finished with warnings" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "❌ Agent $agent failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Pause between agents
    if ($i -lt $agents.Length - 1) {
        Write-Host "`n⏸️ Tactical pause before next agent..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

Write-Host "`n🎉 MISSION DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# Check for victories
Write-Host "`n🔍 Scanning for victories..." -ForegroundColor Cyan
$logFiles = Get-ChildItem -Path "mission_log_*.csv" -ErrorAction SilentlyContinue

if ($logFiles) {
    Write-Host "📊 MISSION LOGS FOUND:" -ForegroundColor Green
    foreach ($log in $logFiles) {
        $content = Get-Content $log.FullName | Select-Object -Last 5
        $successes = $content | Where-Object { $_ -like "*SUCCESS*" }
        if ($successes) {
            Write-Host "🏆 VICTORY in $($log.Name)!" -ForegroundColor Green
            foreach ($success in $successes) {
                Write-Host "   ✅ $success" -ForegroundColor Green
            }
        }
    }
} else {
    Write-Host "📝 No mission logs yet - agents are starting up!" -ForegroundColor Yellow
}

Write-Host "`n🎯 Mission Control: Check mission_log_X.csv files for detailed results" -ForegroundColor Cyan
