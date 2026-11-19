# Installation sur un nouveau PC : environnement Python, base de donnees, icone Bureau.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Creation de l'environnement Python..."
    python -m venv venv
}
Write-Host "Installation des dependances..."
& venv\Scripts\python.exe -m pip install --upgrade pip -q
& venv\Scripts\python.exe -m pip install -r requirements.txt -q

if (-not (Test-Path ".env")) {
    $key = & venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
    @"
FLASK_ENV=development
SECRET_KEY=$key
DATABASE_URL=sqlite:///app.db
ADMIN_USERNAME=admin
ADMIN_EMAIL=jeanoelsuyaristide@gmail.com
ADMIN_PASSWORD=changeme123
DEFAULT_LANGUAGE=fr
SITE_URL=https://bikoue.jsph.site
"@ | Set-Content -Encoding ascii .env
}

$env:FLASK_APP = "wsgi.py"
Write-Host "Preparation de la base de donnees..."
& venv\Scripts\flask.exe db upgrade
& venv\Scripts\flask.exe import-content
& venv\Scripts\flask.exe create-admin

# Icone sur le Bureau
$desktop = [Environment]::GetFolderPath("Desktop")
$shell = New-Object -ComObject WScript.Shell
$lnk = $shell.CreateShortcut("$desktop\Mon Portfolio - Admin.lnk")
$lnk.TargetPath = "$root\Lancer_Admin.bat"
$lnk.WorkingDirectory = $root
$lnk.IconLocation = "$root\deploy\icon.ico"
$lnk.WindowStyle = 7
$lnk.Description = "Modifier et publier mon portfolio"
$lnk.Save()

Write-Host ""
Write-Host "Termine. Utilisez l'icone 'Mon Portfolio - Admin' sur le Bureau."
Write-Host "Pour publier, double-cliquez aussi une fois sur Connecter_Vercel.bat (installe Vercel et connecte votre compte)."
