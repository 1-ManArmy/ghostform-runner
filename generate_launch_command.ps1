# 🚀 1000-Agent Sequential PowerShell Launcher
# This creates the long command to run all agents in sequence

Write-Host "🚀 Generating 1000-agent launch command..." -ForegroundColor Green

$command = ""
for ($i = 1; $i -le 1000; $i++) {
    if ($i -eq 1) {
        $command += "python boss_ai_playwright_pin$i.py"
    } else {
        $command += "; python boss_ai_playwright_pin$i.py"
    }
}

Write-Host "📋 Command generated! Copy and paste this into PowerShell:" -ForegroundColor Yellow
Write-Host ""
Write-Host $command -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 This will run all 1000 agents sequentially!" -ForegroundColor Green
