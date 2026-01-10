#!/bin/bash

echo "🚀 Starting Nexus SEO Intelligence"
echo "=================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your credentials"
    echo "See SETUP_GUIDE.md for instructions"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Function to start webhook server
start_webhook_server() {
    echo "🎣 Starting webhook server on port 8000..."
    python webhook_server.py &
    WEBHOOK_PID=$!
    echo "✅ Webhook server started (PID: $WEBHOOK_PID)"
}

# Function to start Streamlit
start_streamlit() {
    echo "🌐 Starting Streamlit app on port 8501..."
    streamlit run app.py &
    STREAMLIT_PID=$!
    echo "✅ Streamlit app started (PID: $STREAMLIT_PID)"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    if [ ! -z "$WEBHOOK_PID" ]; then
        kill $WEBHOOK_PID 2>/dev/null
        echo "✅ Webhook server stopped"
    fi
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null
        echo "✅ Streamlit app stopped"
    fi
    echo "👋 Goodbye!"
    exit 0
}

# Trap CTRL+C and call cleanup
trap cleanup INT TERM

# Start services
start_webhook_server
sleep 2
start_streamlit

echo ""
echo "=================================="
echo "✨ All services are running!"
echo ""
echo "📍 Streamlit App: http://localhost:8501"
echo "📍 Webhook Server: http://localhost:8000"
echo ""
echo "💡 In another terminal, run:"
echo "   stripe listen --forward-to localhost:8000/webhook"
echo ""
echo "Press CTRL+C to stop all services"
echo "=================================="

# Wait for processes
wait