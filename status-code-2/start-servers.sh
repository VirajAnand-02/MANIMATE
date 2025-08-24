#!/bin/bash

# Start both servers script

echo "Starting AI Video Generation Pipeline..."
echo "========================================="

# Check if Python virtual environment exists
if [ ! -d "../langChan_tst/venv" ]; then
    echo "⚠️  Python virtual environment not found. Please create one first:"
    echo "   cd ../langChan_tst && python -m venv venv"
    echo "   Then activate it and install requirements: pip install -r requirements.txt"
    exit 1
fi

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use"
        return 1
    fi
    return 0
}

# Check ports
if ! check_port 8001; then
    echo "Please stop the service using port 8001 or change PYTHON_API_PORT"
    exit 1
fi

if ! check_port 5001; then
    echo "Please stop the service using port 5001 or change PORT in .env"
    exit 1
fi

echo "🐍 Starting Python API server on port 8001..."
cd ../langChan_tst
source venv/bin/activate  # Use 'venv\Scripts\activate' on Windows
python main.py api &
PYTHON_PID=$!

# Wait for Python server to start
sleep 5

echo "🟢 Node.js server starting on port 5001..."
cd ../status-code-2
npm start &
NODE_PID=$!

echo ""
echo "🚀 Both servers started successfully!"
echo "📊 Python API Server: http://localhost:8001"
echo "📊 Python API Docs: http://localhost:8001/docs"
echo "🌐 Node.js API Server: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $PYTHON_PID 2>/dev/null
    kill $NODE_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait
