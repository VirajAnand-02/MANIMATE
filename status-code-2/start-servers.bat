@echo off
REM Start both servers script for Windows

echo Starting AI Video Generation Pipeline...
echo =========================================

REM Check if Python virtual environment exists
if not exist "..\langChan_tst\venv" (
    echo Warning: Python virtual environment not found. Please create one first:
    echo    cd ..\langChan_tst ^&^& python -m venv venv
    echo    Then activate it and install requirements: pip install -r requirements.txt
    pause
    exit /b 1
)

echo Starting Python API server on port 8001...
cd ..\langChan_tst
call venv\Scripts\activate
start "Python API Server" cmd /c "python main.py api"

REM Wait for Python server to start
timeout /t 5 /nobreak > nul

echo Starting Node.js server on port 5001...
cd ..\status-code-2
start "Node.js API Server" cmd /c "npm start"

echo.
echo Both servers started successfully!
echo Python API Server: http://localhost:8001
echo Python API Docs: http://localhost:8001/docs
echo Node.js API Server: http://localhost:5001
echo.
echo Press any key to continue...
pause > nul
