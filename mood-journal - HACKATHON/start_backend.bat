@echo off
echo Starting Mood Journal Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements if needed
echo Installing/updating requirements...
pip install -r requirements.txt

REM Start the Flask application
echo.http://localhost:5000
echo Starting Flask backend on 
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
