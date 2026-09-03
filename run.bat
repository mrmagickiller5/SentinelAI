@echo off
echo ================================
echo        Starting SentinelAI
echo ================================

echo.
echo Checking environment...

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo.
echo Starting SentinelAI Dashboard...
echo.
echo Open your browser at:
echo http://localhost:8501
echo.

.venv\Scripts\python.exe -m streamlit run dashboard\app.py

pause