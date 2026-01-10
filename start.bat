@echo off
echo ========================================
echo 🚀 Starting Nexus SEO Intelligence
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please create .env file with your credentials
    echo See SETUP_GUIDE.md for instructions
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    echo ✅ Dependencies installed
    echo.
)

REM Start webhook server in new window
echo 🎣 Starting webhook server...
start "Webhook Server" cmd /k "venv\Scripts\activate.bat && python webhook_server.py"
timeout /t 2 /nobreak >nul

REM Start Streamlit in new window
echo 🌐 Starting Streamlit app...
start "Streamlit App" cmd /k "venv\Scripts\activate.bat && streamlit run app.py"

echo.
echo ========================================
echo ✨ All services are starting!
echo.
echo 📍 Streamlit App: http://localhost:8501
echo 📍 Webhook Server: http://localhost:8000
echo.
echo 💡 In another terminal, run:
echo    stripe listen --forward-to localhost:8000/webhook
echo.
echo 🛑 Close the windows to stop services
echo ========================================
echo.
pause