$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Primero instala las dependencias siguiendo README.md.'
}
if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.env'))) {
    throw 'Copia .env.example a .env y configura las credenciales de MySQL.'
}
& $pythonPath manage.py migrate
if ($LASTEXITCODE -ne 0) { throw 'No fue posible aplicar las migraciones.' }
& $pythonPath manage.py runserver 127.0.0.1:8000
