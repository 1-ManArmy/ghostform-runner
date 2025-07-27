# 🎯 GHOSTFORM RUNNER - 400 AGENT ARMY DEPLOYMENT
# Boss's Sequential Strategy: A→B→C→D (1 by 1, with breaks)

Set-Location "$PSScriptRoot"

Write-Host "🎯 GHOSTFORM RUNNER - 400 AGENT ARMY DEPLOYMENT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 Boss's Sequential Strategy: A→B→C→D" -ForegroundColor Yellow
Write-Host "⚡ Behavior-Based Logic: ACTIVE" -ForegroundColor Green
Write-Host "🎯 Target Bookings: 4 Different IDs" -ForegroundColor Green
Write-Host "🔐 Random PINs: 2000 Synchronized Across Batches" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# Function to run a batch of agents
function Run-Batch {
    param([string]$BatchLetter, [string]$BatchName)
    
    Write-Host "`n🔄 DEPLOYING BATCH $BatchLetter ($BatchName)" -ForegroundColor Magenta
    Write-Host "Strategy: Sequential execution with behavior logic" -ForegroundColor Green
    
    $successCount = 0
    $errorCount = 0
    
    for ($i = 1; $i -le 100; $i++) {
        $padded = "{0:D3}" -f $i
        $file = "agent_${padded}${BatchLetter}.py"
        
        if (Test-Path $file) {
            Write-Host "🚀 Launching Agent $padded$BatchLetter..." -ForegroundColor Yellow
            
            try {
                python $file
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ Agent $padded$BatchLetter completed" -ForegroundColor Green
                    $successCount++
                } else {
                    Write-Host "⚠️ Agent $padded$BatchLetter finished with warnings" -ForegroundColor Yellow
                    $errorCount++
                }
            }
            catch {
                Write-Host "❌ Agent $padded$BatchLetter failed: $($_.Exception.Message)" -ForegroundColor Red
                $errorCount++
            }
            
            # Brief pause between agents
            Start-Sleep -Seconds 1
        }
        else {
            Write-Host "⚠️ File not found: $file" -ForegroundColor Red
            $errorCount++
        }
    }
    
    Write-Host "`n📊 BATCH $BatchLetter SUMMARY:" -ForegroundColor Cyan
    Write-Host "✅ Successful: $successCount" -ForegroundColor Green
    Write-Host "❌ Errors: $errorCount" -ForegroundColor Red
}

# Function to pause between batches
function Take-Break {
    param([string]$NextBatch)
    
    Write-Host "`n⏸️ TACTICAL BREAK - Boss's Strategy" -ForegroundColor Yellow
    Write-Host "Next up: Batch $NextBatch" -ForegroundColor Cyan
    Write-Host "Taking 5 second break..." -ForegroundColor White
    
    for ($i = 5; $i -gt 0; $i--) {
        Write-Host "⏳ $i..." -ForegroundColor Yellow
        Start-Sleep -Seconds 1
    }
    
    Write-Host "🚀 Break over! Deploying next batch..." -ForegroundColor Green
}

# Main Execution - Boss's Sequential Strategy
$startTime = Get-Date
Write-Host "`n🎯 MISSION START: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Green

try {
    # BATCH A - Booking ID: 5830944764
    Run-Batch -BatchLetter "A" -BatchName "Alpha Squad (5830944764)"
    Take-Break -NextBatch "B"
    
    # BATCH B - Booking ID: 5727559423  
    Run-Batch -BatchLetter "B" -BatchName "Bravo Squad (5727559423)"
    Take-Break -NextBatch "C"
    
    # BATCH C - Booking ID: 6860261353
    Run-Batch -BatchLetter "C" -BatchName "Charlie Squad (6860261353)"
    Take-Break -NextBatch "D"
    
    # BATCH D - Booking ID: 6339614781
    Run-Batch -BatchLetter "D" -BatchName "Delta Squad (6339614781)"
    
    # Mission Complete
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    Write-Host "`n🎉 MISSION COMPLETE!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "⏱️ Total Duration: $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor White
    Write-Host "🎯 All 400 Agents Deployed!" -ForegroundColor Green
    Write-Host "🏆 GHOSTFORM ARMY DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Cyan
}
catch {
    Write-Host "`n❌ MISSION FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Check for victories
Write-Host "`n🔍 Scanning for victories..." -ForegroundColor Cyan
$victoryFiles = Get-ChildItem -Path "victory_*.json" -ErrorAction SilentlyContinue

if ($victoryFiles) {
    Write-Host "🏆 VICTORIES FOUND:" -ForegroundColor Green
    foreach ($victory in $victoryFiles) {
        Write-Host "✅ $($victory.Name)" -ForegroundColor Green
    }
} else {
    Write-Host "📝 No victories yet - agents are still hunting!" -ForegroundColor Yellow
}

Write-Host "`n🎯 Run complete! Check logs for details." -ForegroundColor Cyan
