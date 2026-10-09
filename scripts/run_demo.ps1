$ErrorActionPreference = "Stop"
$FrontendPath = Join-Path $PSScriptRoot "..\frontend"
Set-Location $FrontendPath

if (-not (Test-Path ".env.local")) {
  @"
VITE_DEMO_MODE=true
VITE_API_BASE_URL=http://localhost:8000/api/v1
"@ | Set-Content ".env.local"
  Write-Host "Created frontend/.env.local for sample mode."
}

if (-not (Test-Path "node_modules")) {
  npm install
}
npm run dev
