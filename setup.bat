@echo off
REM ===============================
REM Windows Setup Script
REM ===============================

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Upgrading pip...
pip install --upgrade pip

echo Installing required packages from requirements.txt...
pip install -r requirements.txt

echo Setup complete.
pause
