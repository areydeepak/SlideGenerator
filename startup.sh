#!/bin/bash

# SlideGenerator Startup Script
echo "🚀 Starting SlideGenerator..."

# Set script directory as the working directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env file exists, create from template if not
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp env.example .env
    echo "Please update the .env file with your configuration"
fi

# Export PYTHONPATH
export PYTHONPATH=$(pwd)

# Check if presentations directory exists
if [ ! -d "presentations" ]; then
    echo "📁 Creating presentations directory..."
    mkdir -p presentations
fi


# Check if Redis is running
redis-cli ping > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️ Redis not running. Please start Redis server."
    echo "On macOS: brew services start redis"
    echo "On Linux: sudo systemctl start redis"
    exit 1
fi

# Start worker process in the background
echo "👷 Starting worker process..."
python start_worker.py &
WORKER_PID=$!

# Give worker time to start
sleep 2

# Start the FastAPI server
echo "🌐 Starting API server..."
python app/main.py &
SERVER_PID=$!

# Create function to handle exit
function cleanup {
    echo "🛑 Stopping SlideGenerator..."
    kill $WORKER_PID
    kill $SERVER_PID
    echo "✅ SlideGenerator stopped"
    exit 0
}

# Register the cleanup function for SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

echo "✅ SlideGenerator is running!"
echo "API: http://localhost:8000"
echo "Press Ctrl+C to stop"

# Wait for signals
wait 