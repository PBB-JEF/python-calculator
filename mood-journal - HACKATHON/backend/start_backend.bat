@echo off
echo Starting Mood Journal Backend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "..\venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv ..\venv
)

REM Activate virtual environment
echo Activating virtual environment...
call ..\venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the backend server
echo.
echo Starting Flask development server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python run.py

pause
