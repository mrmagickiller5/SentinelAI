@echo off

title SentinelAI Setup

echo ========================================
echo        SENTINELAI SETUP
echo ========================================
echo.

echo Checking Python...
python --version

if errorlevel 1 (
    echo.
    echo Python is not installed.
    echo Please install Python 3.11 or newer.
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...

if not exist ".venv" (
    python -m venv .venv

    if errorlevel 1 (
        echo.
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo.
echo Activating virtual environment...

call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo.
echo Upgrading pip...

python -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo Failed to upgrade pip.
    pause
    exit /b 1
)

echo.
echo Installing SentinelAI dependencies...

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ========================================
echo       SENTINELAI SETUP COMPLETE
echo ========================================
echo.

echo To start SentinelAI, run:
echo.
echo run.bat
echo.

pause