# Zone Occupancy & Phone Detection System Startup Script (PowerShell)
# This script sets up and starts both the detection system and dashboard

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Zone Occupancy & Phone Detection System" -ForegroundColor Cyan
Write-Host "  With Real-Time Analytics Dashboard" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[INFO] Python installed: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Check and install requirements
Write-Host "[INFO] Checking dependencies..." -ForegroundColor Yellow
$missingDeps = @()
@('flask', 'ultralytics', 'opencv-python', 'winotify') | ForEach-Object {
    if (-not (pip list | Select-String -Pattern $_ -Quiet)) {
        $missingDeps += $_
    }
}

if ($missingDeps.Count -gt 0) {
    Write-Host "[WARNING] Installing missing dependencies: $($missingDeps -join ', ')" -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "[SUCCESS] All dependencies ready!" -ForegroundColor Green
Write-Host ""

# Display startup information
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Starting Services..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[STEP 1] Starting Detection System" -ForegroundColor Yellow
Write-Host "         Press Q in the detection window to quit" -ForegroundColor Gray
Write-Host ""
Write-Host "[STEP 2] Starting Dashboard" -ForegroundColor Yellow
Write-Host "         Open browser: http://localhost:5000" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to start"

Write-Host ""
Write-Host "[INFO] Launching detection system..." -ForegroundColor Cyan
Start-Process -FilePath "python" -ArgumentList "main.py" -WindowStyle Normal -PassThru

Write-Host "[INFO] Waiting for detection system to initialize (5 seconds)..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

Write-Host "[INFO] Launching analytics dashboard..." -ForegroundColor Cyan
Start-Process -FilePath "python" -ArgumentList "dashboard.py" -WindowStyle Normal -PassThru

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "[SUCCESS] Both services launched!" -ForegroundColor Green
Write-Host ""
Write-Host "Detection window: Zone Occupancy & Phone Monitor" -ForegroundColor Gray
Write-Host "Dashboard URL:    http://localhost:5000" -ForegroundColor Gray
Write-Host ""
Write-Host "Opening dashboard in browser..." -ForegroundColor Cyan
Start-Process "http://localhost:5000"

Write-Host ""
Write-Host "[INFO] Dashboard should open automatically" -ForegroundColor Green
Write-Host "[INFO] If not, manually visit: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
