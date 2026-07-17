[CmdletBinding()]
param(
    [int]$FrontendPort = 5173,
    [int]$BackendPort = 8000,
    [switch]$DryRun,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Get-ListenersOnPort {
    param([int]$Port)

    try {
        return @(
            Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
                Select-Object -Property LocalPort, OwningProcess -Unique
        )
    } catch {
        Write-Host "Unable to query port $Port listeners: $($_.Exception.Message)"
        return @()
    }
}

function Get-ProcessDetails {
    param([int]$ProcessId)

    $process = $null
    try {
        $process = Get-Process -Id $ProcessId -ErrorAction Stop
    } catch {
        return $null
    }

    $commandLine = ""
    try {
        $cim = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction Stop
        if ($null -ne $cim.CommandLine) {
            $commandLine = $cim.CommandLine
        }
    } catch {
        $commandLine = ""
    }

    [PSCustomObject]@{
        Id = $process.Id
        Name = $process.ProcessName
        CommandLine = $commandLine
    }
}

function Test-IsExpectedService {
    param(
        [object]$Process,
        [string]$Kind
    )

    $name = $Process.Name.ToLowerInvariant()
    $commandLine = $Process.CommandLine

    if ($Kind -eq "backend") {
        if ($commandLine -match "uvicorn" -and $commandLine -match "app\.main:app") {
            return $true
        }
        return $name -in @("python", "python3", "py")
    }

    if ($Kind -eq "frontend") {
        if ($commandLine -match "vite" -or $commandLine -match "node_modules[\\/]\.bin[\\/]vite") {
            return $true
        }
        return $name -in @("node", "npm", "npm.cmd")
    }

    return $false
}

function Stop-DemoPort {
    param(
        [string]$Kind,
        [int]$Port
    )

    $listeners = @(Get-ListenersOnPort -Port $Port)
    if ($listeners.Count -eq 0) {
        Write-Host "$Kind port ${Port}: no listener found."
        return
    }

    foreach ($listener in $listeners) {
        $details = Get-ProcessDetails -ProcessId $listener.OwningProcess
        if ($null -eq $details) {
            Write-Host "$Kind port ${Port}: process $($listener.OwningProcess) is no longer running."
            continue
        }

        $expected = Test-IsExpectedService -Process $details -Kind $Kind
        $summary = "$Kind port ${Port}: pid=$($details.Id), name=$($details.Name)"
        if ($details.CommandLine) {
            $summary = "$summary, command=$($details.CommandLine)"
        }

        if (-not $expected -and -not $Force) {
            Write-Host "$summary"
            Write-Host "  Skipped: process does not look like the demo $Kind service. Re-run with -Force to stop it."
            continue
        }

        if ($DryRun) {
            Write-Host "$summary"
            Write-Host "  DryRun: would stop this process."
            continue
        }

        Write-Host "$summary"
        Stop-Process -Id $details.Id -Force
        Write-Host "  Stopped."
    }
}

Write-Host "Stopping demo services under: $Root"
if ($DryRun) {
    Write-Host "DryRun enabled; no processes will be stopped."
}
Write-Host ""

Stop-DemoPort -Kind "frontend" -Port $FrontendPort
Stop-DemoPort -Kind "backend" -Port $BackendPort

Write-Host ""
Write-Host "Done."
