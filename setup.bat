@echo off
REM PostBot Setup Script for Railway Deployment (Windows)

echo 🤖 PostBot - Railway Deployment Setup
echo ==================================

REM Check if we're in the right directory
if not exist "postbot.py" (
    echo ❌ Error: postbot.py not found. Please run this script from the PostBot directory.
    pause
    exit /b 1
)

REM Create logs directory
if not exist "logs" mkdir logs
echo ✅ Created logs directory

REM Check if .env exists
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo ✅ Created .env file from .env.example
    ) else (
        echo ⚠️  Warning: No .env.example found. You'll need to create .env manually.
    )
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📦 Installing Python dependencies...
    pip install -r requirements.txt
    echo ✅ Dependencies installed
)

REM Git setup
if not exist ".git" (
    echo 🔧 Initializing git repository...
    git init
    git add .
    git commit -m "Initial PostBot setup"
    echo ✅ Git repository initialized
    echo 💡 Next: Create a GitHub repository and run:
    echo    git remote add origin https://github.com/yourusername/PostBot.git
    echo    git branch -M main
    echo    git push -u origin main
) else (
    echo ✅ Git repository already exists
)

echo.
echo 🚀 Setup Complete!
echo.
echo Next steps:
echo 1. Edit .env file with your API credentials
echo 2. Test locally: python postbot.py test
echo 3. Push to GitHub: git add . ^&^& git commit -m "Ready for Railway" ^&^& git push
echo 4. Deploy to Railway: https://railway.app
echo.
echo 📖 Full deployment guide: RAILWAY_DEPLOYMENT.md
echo.
pause