@echo off
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

if not exist venv\Lib\site-packages\PyQt6 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

python main.py
pause
