# Disease Detection Auto-Fix PowerShell Script
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "              DISEASE DETECTION - AUTO FIX" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're in the right directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
$venvPath = "..\..\..\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "[OK] Virtual environment activated`n" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Virtual environment not found at: $venvPath" -ForegroundColor Yellow
    Write-Host "[INFO] Trying alternative path..." -ForegroundColor Yellow
    $altVenvPath = "C:\Users\Aman\Desktop\ibm\.venv\Scripts\Activate.ps1"
    if (Test-Path $altVenvPath) {
        & $altVenvPath
        Write-Host "[OK] Virtual environment activated`n" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Could not find virtual environment!" -ForegroundColor Red
        Write-Host "[INFO] Please activate it manually and run: python AUTO_FIX.py" -ForegroundColor Yellow
        exit 1
    }
}

# Run the Python auto-fix script
Write-Host "[INFO] Running auto-fix script..." -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

python AUTO_FIX.py

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "[INFO] Auto-fix script completed" -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
