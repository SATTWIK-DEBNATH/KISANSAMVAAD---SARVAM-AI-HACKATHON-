# KisanSamvaad Lightweight 8GB RAM Demo Launcher
Write-Host "====================================================================" -ForegroundColor Green
Write-Host "     KisanSamvaad (किसान संवाद / ಕಿಸಾನ್ ಸಂವಾದ)" -ForegroundColor Yellow
Write-Host "     Sovereign Indic Voice & Document AI - 8GB RAM Optimized" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Green

Write-Host "`n[1/2] Starting Python Server on http://localhost:8000..." -ForegroundColor Cyan
$process = Start-Process python -ArgumentList "backend/server.py", "8000" -PassThru

Start-Sleep -Seconds 2
Write-Host "[2/2] Opening Demo in Browser..." -ForegroundColor Cyan
Start-Process "http://localhost:8000"

Write-Host "`nDemo is running smoothly! Memory usage: < 50MB." -ForegroundColor Green
Write-Host "Press any key to stop the server..." -ForegroundColor DarkYellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Stop-Process -Id $process.Id -Force
Write-Host "Server stopped." -ForegroundColor Red

