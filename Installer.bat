@echo off
rem A lancer une seule fois sur un nouveau PC (apres avoir clone le depot).
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "deploy\installer.ps1"
pause
