$ErrorActionPreference = "Stop"
$FrontendPath = Join-Path $PSScriptRoot "..\frontend"
Set-Location $FrontendPath
npm install
Write-Host ""
Write-Host "Frontend dependencies installed."
Write-Host "Run: npm run dev"
