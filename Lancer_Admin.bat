@echo off
rem Ouvre l'espace admin du portfolio (serveur local, accessible uniquement depuis ce PC).
cd /d "%~dp0"
set LOCAL_ADMIN=1
set FLASK_APP=wsgi.py

rem Serveur deja lance ? on ouvre juste le navigateur.
netstat -ano | findstr ":5000 " | findstr LISTENING >nul
if %errorlevel%==0 (
  start "" http://127.0.0.1:5000/admin/
  exit /b
)

if not exist "venv\Scripts\python.exe" (
  echo Installation introuvable. Lancez d'abord Installer.bat
  pause
  exit /b 1
)

start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:5000/admin/"
echo ================================================
echo  Admin du portfolio en cours d'execution.
echo  Fermez cette fenetre pour arreter le serveur.
echo ================================================
venv\Scripts\python.exe -m flask run --host 127.0.0.1 --port 5000
