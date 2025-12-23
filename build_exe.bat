@echo off
echo Building PostBot Executable...
echo ==============================

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo Installing PyInstaller if needed...
pip install pyinstaller

echo Building executable...
pyinstaller postbot.spec --clean

if exist "dist\PostBot.exe" (
    echo.
    echo ========================================
    echo SUCCESS: PostBot.exe created!
    echo ========================================
    echo.
    echo Location: dist\PostBot.exe
    echo Size: 
    dir "dist\PostBot.exe" | findstr PostBot.exe
    echo.
    echo To run: 
    echo 1. Copy your .env file to the same folder as PostBot.exe
    echo 2. Double-click PostBot.exe or run from command line
    echo.
    echo IMPORTANT: Make sure .env file is in the same directory!
) else (
    echo.
    echo ERROR: Build failed!
    echo Check the output above for errors.
)

pause