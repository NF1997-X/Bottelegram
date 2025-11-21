#!/bin/bash

# File Sharing Bot Startup Script
# ================================

echo "🤖 Starting File Sharing Bot..."
echo "================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your bot configuration."
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python -c "import pyrogram, aiohttp, psycopg2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

echo "✅ Dependencies OK"

# Start the bot
echo "🚀 Starting bot..."
echo "================================"
python main.py