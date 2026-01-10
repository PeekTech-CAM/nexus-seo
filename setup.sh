#!/bin/bash

echo "🚀 Setting up Nexus SEO Intelligence..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your Stripe keys!"
else
    echo "✅ .env file already exists"
fi

# Create services directory if it doesn't exist
if [ ! -d services ]; then
    echo "📁 Creating services directory..."
    mkdir services
    touch services/__init__.py
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your Stripe API keys"
echo "2. Update Stripe price IDs in app.py"
echo "3. Run: streamlit run app.py"
echo ""
echo "🔗 For Stripe webhook testing, run:"
echo "   stripe listen --forward-to localhost:8501/webhook"
echo ""