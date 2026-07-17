[CmdletBinding()]
param(
    [switch]$SeedData,
    [switch]$NoOpen,
    [int]$FrontendPort = 5173,
    [int]$BackendPort = 8000,
    [string]$Python = "python",
    [string]$StartPath = "/chapters/big-integer/lessons/big-integer-overflow"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom
$env:PYTHONIOENCODING = "utf-8"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$DemoStart = Join-Path $PSScriptRoot "demo_start.ps1"

if (-not $StartPath.StartsWith("/")) {
    $StartPath = "/$StartPath"
}

$studentUrl = "http://127.0.0.1:$FrontendPort$StartPath"
$statsUrl = "http://127.0.0.1:$FrontendPort/stats"

Write-Host "Starting student demo..."
Write-Host "Root: $Root"
Write-Host ""

$startArgs = @{
    FrontendPort = $FrontendPort
    BackendPort = $BackendPort
    Python = $Python
}

if ($SeedData) {
    $startArgs.SeedData = $true
}

& $DemoStart @startArgs

Write-Host ""
Write-Host "Student entry:"
Write-Host "  $studentUrl"
Write-Host ""
Write-Host "Suggested student flow:"
Write-Host "  1. Watch the lesson video."
Write-Host "  2. Read concepts and steps."
Write-Host "  3. Open a practice problem and submit C++ code."
Write-Host "  4. Use hints only when stuck."
Write-Host "  5. Return to the lesson and continue."
Write-Host ""
Write-Host "Teacher stats, if needed:"
Write-Host "  $statsUrl"
Write-Host ""
Write-Host "Stop command:"
Write-Host "  powershell.exe -ExecutionPolicy Bypass -File scripts\demo_stop.ps1"

if (-not $NoOpen) {
    Write-Host ""
    Write-Host "Opening student entry in the default browser..."
    Start-Process $studentUrl
}
