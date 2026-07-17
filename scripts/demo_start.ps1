[CmdletBinding()]
param(
    [switch]$SeedData,
    [int]$FrontendPort = 5173,
    [int]$BackendPort = 8000,
    [string]$Python = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom
$env:PYTHONIOENCODING = "utf-8"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Frontend = Join-Path $Root "frontend"
$Backend = Join-Path $Root "backend"

function Test-PortInUse {
    param([int]$Port)

    try {
        $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
        return $null -ne $connection
    } catch {
        return $false
    }
}

function Wait-Http {
    param(
        [string]$Url,
        [int]$Seconds = 20
    )

    $deadline = (Get-Date).AddSeconds($Seconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
                return $true
            }
        } catch {
            Start-Sleep -Milliseconds 700
        }
    }
    return $false
}

if ($SeedData) {
    Write-Host "Seeding demo submissions..."
    & $Python (Join-Path $Root "scripts\seed_demo_data.py")
}

if (Test-PortInUse -Port $BackendPort) {
    Write-Host "Backend port $BackendPort is already in use; keeping the existing process."
} else {
    Write-Host "Starting backend on http://127.0.0.1:$BackendPort ..."
    Start-Process `
        -FilePath $Python `
        -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", [string]$BackendPort) `
        -WorkingDirectory $Backend `
        -WindowStyle Hidden
}

if (Test-PortInUse -Port $FrontendPort) {
    Write-Host "Frontend port $FrontendPort is already in use; keeping the existing process."
} else {
    Write-Host "Starting frontend on http://127.0.0.1:$FrontendPort ..."
    Start-Process `
        -FilePath "npm.cmd" `
        -ArgumentList @("run", "dev", "--", "--host", "127.0.0.1", "--port", [string]$FrontendPort) `
        -WorkingDirectory $Frontend `
        -WindowStyle Hidden
}

$backendReady = Wait-Http -Url "http://127.0.0.1:$BackendPort/api/health" -Seconds 20
$frontendReady = Wait-Http -Url "http://127.0.0.1:$FrontendPort" -Seconds 25

Write-Host ""
Write-Host "Demo URLs:"
Write-Host "  Frontend: http://127.0.0.1:$FrontendPort"
Write-Host "  Backend:  http://127.0.0.1:$BackendPort/api/health"
Write-Host "  Stats:    http://127.0.0.1:$FrontendPort/stats"
Write-Host ""
Write-Host "Backend ready:  $backendReady"
Write-Host "Frontend ready: $frontendReady"

if (-not $backendReady -or -not $frontendReady) {
    Write-Host "One or more services did not answer before the timeout. They may still be starting."
}
