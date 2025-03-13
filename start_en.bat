@echo off
REM Start the Python script in a new window
start "" python earthquake_warning_app_en.py
REM Wait 5 seconds for the server to start
timeout /t 5
REM Open the browser with the local web interface
start http://127.0.0.1:5000
