@echo off
REM Bid Leveling AI - Quick Start Script for Windows
REM This script helps you get started quickly with the Bid Leveling AI system

echo.
echo ========================================
echo 🏗️  Bid Leveling AI - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✓ Python found

REM Check if we're in the correct directory
if not exist "backend\app.py" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

echo.
echo 📦 Step 1: Installing Python dependencies...
cd backend
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed

echo.
echo 🔑 Step 2: Setting up environment variables...

REM Check if .env exists
if not exist ".env" (
    echo.
    echo Please enter your Anthropic API key:
    echo (Get one from: https://console.anthropic.com/)
    set /p api_key="API Key: "
    
    if "%api_key%"=="" (
        echo ❌ API key is required
        pause
        exit /b 1
    )
    
    echo ANTHROPIC_API_KEY=%api_key%> .env
    echo FLASK_ENV=development>> .env
    echo FLASK_DEBUG=True>> .env
    echo ✓ Environment file created
) else (
    echo ✓ Environment file exists
)

echo.
echo 📄 Step 3: Generating sample bid PDFs...
python generate_sample_bids.py

echo.
echo ========================================
echo ✅ Setup Complete!
echo.
echo To start the application:
echo.
echo 1. Backend (in this terminal):
echo    cd backend
echo    python app.py
echo.
echo 2. Frontend (in a new terminal):
echo    cd frontend
echo    Open index.html in your browser
echo    Or run: python -m http.server 8080
echo.
echo 3. Test with sample bids in backend\sample_bids\
echo.
echo ========================================
echo.
pause
