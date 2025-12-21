#!/bin/bash

# Bid Leveling AI - Quick Start Script
# This script helps you get started quickly with the Bid Leveling AI system

echo "🏗️  Bid Leveling AI - Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if we're in the correct directory
if [ ! -f "backend/app.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo ""
echo "📦 Step 1: Installing Python dependencies..."
cd backend
python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🔑 Step 2: Setting up environment variables..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Please enter your Anthropic API key:"
    echo "(Get one from: https://console.anthropic.com/)"
    read -p "API Key: " api_key
    
    if [ -z "$api_key" ]; then
        echo "❌ API key is required"
        exit 1
    fi
    
    echo "ANTHROPIC_API_KEY=$api_key" > .env
    echo "FLASK_ENV=development" >> .env
    echo "FLASK_DEBUG=True" >> .env
    echo "✓ Environment file created"
else
    echo "✓ Environment file exists"
fi

echo ""
echo "📄 Step 3: Generating sample bid PDFs..."
python3 generate_sample_bids.py

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Backend (in this terminal):"
echo "   cd backend"
echo "   python3 app.py"
echo ""
echo "2. Frontend (in a new terminal):"
echo "   cd frontend"
echo "   Open index.html in your browser"
echo "   Or use: python3 -m http.server 8080"
echo ""
echo "3. Test with sample bids in backend/sample_bids/"
echo ""
echo "=================================="
