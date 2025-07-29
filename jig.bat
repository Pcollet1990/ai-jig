@echo off
REM This batch script activates the Python virtual environment and runs the AI Jig application.

REM Navigate to the directory where this script is located (project root)
pushd "%~dp0"

REM Activate the virtual environment
REM Use the correct activation script based on your OS and shell
REM For Windows Command Prompt:
REM call .venv\Scripts\activate.bat

REM For Windows PowerShell (if running from cmd, this will open a new PowerShell window)
REM If you are running this .bat file directly from a PowerShell terminal,
REM you might prefer to run the activation script directly in PowerShell:
REM .venv\Scripts\Activate.ps1
REM However, for a generic .bat file, 'call' is usually safer for cmd/batch environments.
call .venv\Scripts\activate.bat

REM Check if activation was successful (optional, but good practice)
if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found or activation failed.
    pause
    exit /b 1
)

REM Run the Flet application as a Python module
python -m src.main

REM Keep the console window open after the application closes (useful for seeing output/errors)
pause

REM Return to the original directory
popd
