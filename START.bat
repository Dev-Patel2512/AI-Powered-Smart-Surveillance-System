
@echo off
REM Zone Occupancy & Phone Detection System Startup Script
REM This script starts both the detection system and dashboard

setlocal enabledelayedexpansion

echo ================================================
echo   Zone Occupancy ^& Phone Detection System
echo   With Real-Time Analytics Dashboard
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [INFO] Python is installed
echo.

REM Check if requirements are installed
echo [INFO] Checking dependencies...
pip list | findstr /i "flask ultralytics opencv winotify" >nul
if errorlevel 1 (
    echo [WARNING] Some dependencies may be missing
    echo [INFO] Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [SUCCESS] All dependencies ready!
echo.

echo ================================================
echo   Starting Services...
echo ================================================
echo.
echo [STEP 1] Starting Detection System
echo         Press Q in the detection window to quit
echo.
echo [STEP 2] Starting Dashboard (wait 5 seconds after detection starts)
echo         Open browser: http://localhost:5000
echo.
echo [TIP] Run these in separate terminals for better management:
echo       Terminal 1: python main.py
echo       Terminal 2: python dashboard.py
echo.

pause

REM Start detection in background
echo [INFO] Launching detection system...
start "Zone Occupancy Detection" python main.py

REM Wait a bit for detection to initialize
timeout /t 5 /nobreak

REM Start dashboard in another window
echo [INFO] Launching dashboard...
start "Analytics Dashboard" python dashboard.py

echo.
echo [SUCCESS] Both services launched!
echo.
echo Detection window: Zone Occupancy & Phone Monitor
echo Dashboard URL:    http://localhost:5000
echo.
echo Press any key to open the dashboard in your browser...
pause

REM Try to open the dashboard in default browser
start http://localhost:5000

echo.
echo [INFO] Dashboard opening in your default browser...
echo [INFO] If it didn't open, manually visit: http://localhost:5000
echo.
pause
