@echo off
REM Setup script for LLM Quiz Solver

echo ========================================
echo LLM Quiz Solver - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing Python packages...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo [4/5] Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo WARNING: Failed to install browsers
    echo You may need to install manually: playwright install chromium
)

echo [5/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - PLEASE EDIT IT WITH YOUR CREDENTIALS!
) else (
    echo .env file already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Edit .env file with your credentials
echo 2. Run: python app.py
echo 3. Test: python test_endpoint.py
echo.
pause
