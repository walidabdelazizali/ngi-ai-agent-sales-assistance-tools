# bootstrap.ps1 — Create venv and install dependencies
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$venvPath = ".venv"

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvPath
}

Write-Host "Activating virtual environment..."
& "$venvPath\Scripts\Activate.ps1"

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Bootstrap complete."
