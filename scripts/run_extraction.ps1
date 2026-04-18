# run_extraction.ps1 — Run the extraction pipeline via CLI entry point
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path "$PSScriptRoot\..").Path
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: .venv not found. Run scripts\bootstrap.ps1 first."
    exit 1
}

# TODO: Add pipeline arguments as implementation progresses
Push-Location $projectRoot
try {
    & $venvPython -m src
} finally {
    Pop-Location
}
