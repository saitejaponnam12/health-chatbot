@echo off
REM Health Chatbot System - Quick Start Batch File
REM Run this file to execute all demos and generate outputs

echo.
echo ================================
echo  Health Chatbot System
echo  Quick Start
echo ================================
echo.

REM Change to script directory
cd /d %~dp0

echo.
echo [1/4] Installing dependencies...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed

echo.
echo [2/4] Running main system initialization...
python scripts/main.py
if errorlevel 1 (
    echo Error: Main system failed
    pause
    exit /b 1
)
echo OK: Main system complete

echo.
echo [3/4] Running demo examples...
python scripts/demo.py
if errorlevel 1 (
    echo Warning: Demo had issues (non-critical)
)
echo OK: Demo complete

echo.
echo [4/4] Generation summary...
echo.
echo Generated Files:
echo.
if exist "outputs\conversation_logs.json" (
    echo + outputs\conversation_logs.json (Conversation logs)
) else (
    echo - outputs\conversation_logs.json (MISSING)
)

if exist "outputs\query_response_analysis.json" (
    echo + outputs\query_response_analysis.json (Query analysis)
) else (
    echo - outputs\query_response_analysis.json (MISSING)
)

if exist "outputs\similarity_scores_analysis.png" (
    echo + outputs\similarity_scores_analysis.png (Visualization)
) else (
    echo - outputs\similarity_scores_analysis.png (MISSING)
)

echo.
echo ================================
echo  System Ready!
echo ================================
echo.
echo Next steps:
echo.
echo 1. Review conversation logs:
echo    outputs\conversation_logs.json
echo.
echo 2. View visualization:
echo    outputs\similarity_scores_analysis.png
echo.
echo 3. Run interactive mode:
echo    python scripts/interactive_chatbot.py --mode interactive
echo.
echo 4. Read documentation:
echo    README.md
echo.
echo ================================
echo.
pause
