@echo off
echo Starting Job Market Analyzer Backend...
echo.
echo Server will be available at: http://127.0.0.1:8001
echo API Documentation: http://127.0.0.1:8001/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python simple_server.py

pause 