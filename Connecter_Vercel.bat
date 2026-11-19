@echo off
rem A lancer UNE SEULE FOIS par PC : installe l'outil Vercel et connecte votre compte,
rem pour que le bouton "Publier le site" de l'admin puisse mettre le site en ligne.
cd /d "%~dp0"
echo ================================================
echo  Etape 1/2 : installation de l'outil Vercel
echo ================================================
call npm install -g vercel
if errorlevel 1 (
  echo.
  echo Echec : Node.js est-il installe ? Telechargez-le sur https://nodejs.org puis relancez ce fichier.
  pause
  exit /b 1
)
echo.
echo ================================================
echo  Etape 2/2 : connexion a votre compte Vercel
echo  Une page s'ouvre dans le navigateur : validez la connexion.
echo ================================================
call vercel login
echo.
echo Termine. Vous pouvez maintenant utiliser "Publier le site" dans l'admin.
pause
