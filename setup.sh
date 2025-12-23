#!/bin/bash
# PostBot Setup Script for Railway Deployment

echo "🤖 PostBot - Railway Deployment Setup"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "postbot.py" ]; then
    echo "❌ Error: postbot.py not found. Please run this script from the PostBot directory."
    exit 1
fi

# Create logs directory
mkdir -p logs
echo "✅ Created logs directory"

# Check if .env exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from .env.example"
    else
        echo "⚠️  Warning: No .env.example found. You'll need to create .env manually."
    fi
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Git setup
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial PostBot setup"
    echo "✅ Git repository initialized"
    echo "💡 Next: Create a GitHub repository and run:"
    echo "   git remote add origin https://github.com/yourusername/PostBot.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "🚀 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Test locally: python postbot.py test"
echo "3. Push to GitHub: git add . && git commit -m 'Ready for Railway' && git push"
echo "4. Deploy to Railway: https://railway.app"
echo ""
echo "📖 Full deployment guide: RAILWAY_DEPLOYMENT.md"