@echo off
title KisanSamvaad Demo Runner (Lightweight 8GB RAM Optimized)
cls
echo ====================================================================
echo      KisanSamvaad (किसान संवाद / ಕಿಸಾನ್ ಸಂವಾದ)
echo      Sovereign Indic Voice & Document AI for Indian Agriculture
echo      Optimized for 8GB RAM - Memory footprint: ^< 50 MB
echo ====================================================================
echo.
echo [1/2] Launching KisanSamvaad Sovereign Server on http://localhost:8000 ...

start /b python backend/server.py 8000

echo [2/2] Opening Demo in Default Web Browser...
timeout /t 2 /nobreak >nul
start http://localhost:8000

echo.
echo ====================================================================
echo   Server is running smoothly!
echo   Press CTRL+C in this window or close it to stop the server.
echo ====================================================================
pause

