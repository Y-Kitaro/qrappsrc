@echo off

REM Check if the 'venv' virtual environment exists, create it if not
if not exist "venv" (
    REM Create a Python virtual environment
    python -m venv venv

    REM Install necessary packages
    venv\Scripts\pip install -r requirements.txt
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Execute main.py
python main.py
