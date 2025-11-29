#!/bin/bash
# Setup script for LLM Quiz Solver (Linux/Mac/Git Bash)

echo "========================================"
echo "LLM Quiz Solver - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "ERROR: Python is not installed!"
        echo "Please install Python 3.9 or higher"
        exit 1
    fi
    PYTHON=python3
else
    PYTHON=python
fi

echo "[1/5] Creating virtual environment..."
$PYTHON -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/Scripts/activate || source venv/bin/activate

echo "[3/5] Upgrading pip..."
pip install --upgrade pip

echo "[4/5] Installing Python packages..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install packages"
    exit 1
fi

echo "[5/5] Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to install browsers"
    echo "You may need to install manually: playwright install chromium"
fi

echo ""
echo "[6/6] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - PLEASE EDIT IT WITH YOUR CREDENTIALS!"
else
    echo ".env file already exists"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "NEXT STEPS:"
echo "1. Edit .env file with your credentials"
echo "2. Activate venv: source venv/Scripts/activate  (or venv/bin/activate)"
echo "3. Run: python app.py"
echo "4. Test: python test_endpoint.py"
echo ""
