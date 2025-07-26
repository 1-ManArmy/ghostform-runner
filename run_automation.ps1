Write-Host "======================================" -ForegroundColor Green
Write-Host " MASTER AUTOMATION FOR PIN TESTING" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "This will run all 27 files automatically:" -ForegroundColor Yellow
Write-Host "- Primary file: boss_ai_playwright.py" -ForegroundColor White
Write-Host "- Then A to Z files sequentially" -ForegroundColor White
Write-Host "- Stops when PIN is found" -ForegroundColor White
Write-Host ""
Write-Host "Usage Examples:" -ForegroundColor Cyan
Write-Host "  .\run_automation.ps1" -ForegroundColor White
Write-Host "  .\run_automation.ps1 --confirmation 1234567890 --pins '1000,2000,3000' --wait 30" -ForegroundColor White
Write-Host "  .\run_automation.ps1 --headless --delay 10" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop anytime" -ForegroundColor Red
Write-Host ""
Write-Host "Starting automation..." -ForegroundColor Green
Write-Host ""

python master_automation.py $args
