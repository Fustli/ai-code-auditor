#!/bin/bash

# AI Code Auditor - Startup Script

echo "🧠 AI Code Auditor - Starting up..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "🔑 Please edit .env and add your OpenAI API key!"
    echo ""
fi

# Start the application
echo "🚀 Starting AI Code Auditor..."
echo "📍 Open your browser to: http://localhost:8501"
echo ""
streamlit run app.py