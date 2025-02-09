@echo off
REM ===============================
REM Windows Run Script
REM ===============================

if not exist ".venv" (
    echo Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Running the project...
python main.py

pause
