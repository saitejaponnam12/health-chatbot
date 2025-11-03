#!/usr/bin/env pwsh
# Health Chatbot System - Quick Start PowerShell Script

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Health Chatbot System" -ForegroundColor Cyan
Write-Host "  Quick Start" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

Write-Host ""
Write-Host "[1/4] Installing dependencies..." -ForegroundColor Yellow
python -m pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "OK: Dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "[2/4] Running main system initialization..." -ForegroundColor Yellow
python scripts/main.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Main system failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "OK: Main system complete" -ForegroundColor Green

Write-Host ""
Write-Host "[3/4] Running demo examples..." -ForegroundColor Yellow
python scripts/demo.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Demo had issues (non-critical)" -ForegroundColor Yellow
}
Write-Host "OK: Demo complete" -ForegroundColor Green

Write-Host ""
Write-Host "[4/4] Generation summary..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Generated Files:" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "outputs\conversation_logs.json") {
    Write-Host "+ outputs\conversation_logs.json (Conversation logs)" -ForegroundColor Green
} else {
    Write-Host "- outputs\conversation_logs.json (MISSING)" -ForegroundColor Red
}

if (Test-Path "outputs\query_response_analysis.json") {
    Write-Host "+ outputs\query_response_analysis.json (Query analysis)" -ForegroundColor Green
} else {
    Write-Host "- outputs\query_response_analysis.json (MISSING)" -ForegroundColor Red
}

if (Test-Path "outputs\similarity_scores_analysis.png") {
    Write-Host "+ outputs\similarity_scores_analysis.png (Visualization)" -ForegroundColor Green
} else {
    Write-Host "- outputs\similarity_scores_analysis.png (MISSING)" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  System Ready!" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Review conversation logs:" -ForegroundColor Cyan
Write-Host "   outputs\conversation_logs.json"
Write-Host ""
Write-Host "2. View visualization:" -ForegroundColor Cyan
Write-Host "   outputs\similarity_scores_analysis.png"
Write-Host ""
Write-Host "3. Run interactive mode:" -ForegroundColor Cyan
Write-Host "   python scripts/interactive_chatbot.py --mode interactive"
Write-Host ""
Write-Host "4. Read documentation:" -ForegroundColor Cyan
Write-Host "   README.md"
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
