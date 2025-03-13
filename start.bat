@echo off
REM Starte das Python-Skript in einem neuen Fenster
start "" python earthquake_warning_app.py
REM Warte 5 Sekunden, damit der Server hochfährt
timeout /t 5
REM Öffne den Browser mit der lokalen Weboberfläche
start http://127.0.0.1:5000