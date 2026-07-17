[CmdletBinding()]
param(
    [switch]$Background,
    [ValidateSet("medium", "high", "production")]
    [string]$Quality = "high",
    [int]$DelaySeconds = 60,
    [switch]$Force,
    [switch]$DryRun,
    [switch]$DisableCaching,
    [int]$Limit = 0,
    [string]$StartAt = "",
    [string]$LogPath = "",
    [string]$Python = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$RootPath = $Root.Path
$ScriptPath = $PSCommandPath
if ([string]::IsNullOrWhiteSpace($ScriptPath)) {
    $ScriptPath = $MyInvocation.MyCommand.Path
}
$ScriptPath = (Resolve-Path $ScriptPath).Path

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom
$env:PYTHONIOENCODING = "utf-8"

$qualitySettings = @{
    medium = @{
        Flag = "-qm"
        Dir = "720p30"
    }
    high = @{
        Flag = "-qh"
        Dir = "1080p60"
    }
    production = @{
        Flag = "-qk"
        Dir = "2160p60"
    }
}

$qualityFlag = $qualitySettings[$Quality].Flag
$qualityDir = $qualitySettings[$Quality].Dir

if ([string]::IsNullOrWhiteSpace($LogPath)) {
    $LogPath = Join-Path $RootPath ("logs\manim_hd_render_{0}.log" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
} elseif (-not [System.IO.Path]::IsPathRooted($LogPath)) {
    $LogPath = Join-Path $RootPath $LogPath
}

$LogPath = [System.IO.Path]::GetFullPath($LogPath)
$LogDir = Split-Path -Parent $LogPath
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function ConvertTo-WindowsArgument {
    param([string]$Value)

    return '"{0}"' -f ($Value -replace '"', '\"')
}

if ($Background) {
    $childArgs = @(
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        (ConvertTo-WindowsArgument $ScriptPath),
        "-Quality",
        (ConvertTo-WindowsArgument $Quality),
        "-DelaySeconds",
        [string]$DelaySeconds,
        "-LogPath",
        (ConvertTo-WindowsArgument $LogPath),
        "-Python",
        (ConvertTo-WindowsArgument $Python)
    )

    if ($Force) { $childArgs += "-Force" }
    if ($DryRun) { $childArgs += "-DryRun" }
    if ($DisableCaching) { $childArgs += "-DisableCaching" }
    if ($Limit -gt 0) {
        $childArgs += "-Limit"
        $childArgs += [string]$Limit
    }
    if (-not [string]::IsNullOrWhiteSpace($StartAt)) {
        $childArgs += "-StartAt"
        $childArgs += (ConvertTo-WindowsArgument $StartAt)
    }

    $arguments = $childArgs -join " "
    Set-Content -Path ("{0}.launcher-command.log" -f $LogPath) -Value ("powershell.exe {0}" -f $arguments) -Encoding utf8
    $process = Start-Process `
        -FilePath "powershell.exe" `
        -ArgumentList $arguments `
        -WorkingDirectory $RootPath `
        -WindowStyle Hidden `
        -PassThru

    Write-Host ("Started background HD render process. PID={0}" -f $process.Id)
    Write-Host ("Log: {0}" -f $LogPath)
    return
}

function Write-Log {
    param([string]$Message)

    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -Path $LogPath -Value $line -Encoding utf8
    Write-Host $line
}

function Test-ProcessIsRunning {
    param([int]$ProcessId)

    try {
        $null = Get-Process -Id $ProcessId -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Invoke-ManimRender {
    param(
        [string]$SceneFile,
        [string]$SceneClass
    )

    $arguments = @("-m", "manim", $qualityFlag)
    if ($DisableCaching) {
        $arguments += "--disable_caching"
    }
    $arguments += $SceneFile
    $arguments += $SceneClass

    Write-Log ("Command: {0} {1}" -f $Python, ($arguments -join " "))

    if ($DryRun) {
        return 0
    }

    try {
        $previousErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        try {
            & $Python @arguments 2>&1 | ForEach-Object {
                Write-Log ($_.ToString())
            }
            return $LASTEXITCODE
        } finally {
            $ErrorActionPreference = $previousErrorActionPreference
        }
    } catch {
        Write-Log ("ERROR: {0}" -f $_.Exception.Message)
        return 1
    }
}

$renderQueue = @(
    [pscustomobject]@{ Id = "C02-01"; SceneFile = "manim/scenes/sorting/bubble_sort_scene.py"; SceneClass = "BubbleSortVisualization" },
    [pscustomobject]@{ Id = "C02-04"; SceneFile = "manim/scenes/sorting/selection_sort_scene.py"; SceneClass = "SelectionSortVisualization" },
    [pscustomobject]@{ Id = "C02-05"; SceneFile = "manim/scenes/sorting/insertion_sort_scene.py"; SceneClass = "InsertionSortVisualization" },
    [pscustomobject]@{ Id = "C02-06"; SceneFile = "manim/scenes/sorting/counting_sort_scene.py"; SceneClass = "CountingSortVisualization" },
    [pscustomobject]@{ Id = "C02-07"; SceneFile = "manim/scenes/sorting/merge_sort_scene.py"; SceneClass = "MergeSortVisualization" },
    [pscustomobject]@{ Id = "C02-08"; SceneFile = "manim/scenes/sorting/quick_sort_scene.py"; SceneClass = "QuickSortVisualization" },

    [pscustomobject]@{ Id = "C01-01"; SceneFile = "manim/scenes/high_precision/big_integer_intro_scenes.py"; SceneClass = "BigIntegerOverflowVisualization" },
    [pscustomobject]@{ Id = "C01-02"; SceneFile = "manim/scenes/high_precision/big_integer_intro_scenes.py"; SceneClass = "BigIntegerStorageVisualization" },
    [pscustomobject]@{ Id = "C01-03"; SceneFile = "manim/scenes/high_precision/big_integer_intro_scenes.py"; SceneClass = "BigIntegerReverseStorageVisualization" },
    [pscustomobject]@{ Id = "C01-04"; SceneFile = "manim/scenes/high_precision/big_integer_addition_scene.py"; SceneClass = "BigIntegerAdditionVisualization" },
    [pscustomobject]@{ Id = "C01-05"; SceneFile = "manim/scenes/high_precision/big_integer_subtraction_scene.py"; SceneClass = "BigIntegerSubtractionVisualization" },
    [pscustomobject]@{ Id = "C01-06"; SceneFile = "manim/scenes/high_precision/big_integer_compare_scene.py"; SceneClass = "BigIntegerCompareVisualization" },
    [pscustomobject]@{ Id = "C01-07"; SceneFile = "manim/scenes/high_precision/big_integer_multiply_small_scene.py"; SceneClass = "BigIntegerMultiplySmallVisualization" },
    [pscustomobject]@{ Id = "C01-08"; SceneFile = "manim/scenes/high_precision/big_integer_multiply_big_scene.py"; SceneClass = "BigIntegerMultiplyBigVisualization" },
    [pscustomobject]@{ Id = "C01-09"; SceneFile = "manim/scenes/high_precision/big_integer_divide_small_scene.py"; SceneClass = "BigIntegerDivideSmallVisualization" },
    [pscustomobject]@{ Id = "C01-10"; SceneFile = "manim/scenes/high_precision/leading_zero_normalization_scene.py"; SceneClass = "LeadingZeroNormalizationVisualization" },
    [pscustomobject]@{ Id = "C01-11"; SceneFile = "manim/scenes/high_precision/big_integer_composite_scene.py"; SceneClass = "BigIntegerCompositeVisualization" },

    [pscustomobject]@{ Id = "C03-01"; SceneFile = "manim/scenes/recurrence/state_definition_scene.py"; SceneClass = "RecurrenceStateVisualization" },
    [pscustomobject]@{ Id = "C03-02"; SceneFile = "manim/scenes/recurrence/known_to_unknown_scene.py"; SceneClass = "RecurrenceKnownToUnknownVisualization" },
    [pscustomobject]@{ Id = "C03-03"; SceneFile = "manim/scenes/recurrence/climb_stairs_scene.py"; SceneClass = "RecurrenceClimbStairsVisualization" },
    [pscustomobject]@{ Id = "C03-04"; SceneFile = "manim/scenes/recurrence/fibonacci_sequence_scene.py"; SceneClass = "RecurrenceFibonacciSequenceVisualization" },
    [pscustomobject]@{ Id = "C03-05"; SceneFile = "manim/scenes/recurrence/rolling_variables_scene.py"; SceneClass = "RecurrenceRollingVariablesVisualization" },
    [pscustomobject]@{ Id = "C03-06"; SceneFile = "manim/scenes/recurrence/pascal_triangle_scene.py"; SceneClass = "RecurrencePascalTriangleVisualization" },
    [pscustomobject]@{ Id = "C03-07"; SceneFile = "manim/scenes/recurrence/grid_paths_scene.py"; SceneClass = "RecurrenceGridPathsVisualization" },
    [pscustomobject]@{ Id = "C03-08"; SceneFile = "manim/scenes/recurrence/number_tower_scene.py"; SceneClass = "RecurrenceNumberTowerVisualization" }
)

$lockPath = Join-Path $LogDir "manim_hd_render.lock"
if (Test-Path -LiteralPath $lockPath) {
    $lockText = Get-Content -Path $lockPath -Encoding utf8 -ErrorAction SilentlyContinue | Select-Object -First 1
    $runningPid = 0
    if ([int]::TryParse($lockText, [ref]$runningPid) -and (Test-ProcessIsRunning -ProcessId $runningPid)) {
        throw "Another HD render process is already running. PID=$runningPid. Lock=$lockPath"
    }
}

Set-Content -Path $lockPath -Value ([string]$PID) -Encoding utf8

try {
    try {
        (Get-Process -Id $PID).PriorityClass = "BelowNormal"
    } catch {
        Write-Log ("Could not lower process priority: {0}" -f $_.Exception.Message)
    }

    Write-Log ("HD render queue started. Quality={0} ({1}), DelaySeconds={2}, Force={3}, DisableCaching={4}" -f $Quality, $qualityDir, $DelaySeconds, $Force.IsPresent, $DisableCaching.IsPresent)
    Write-Log ("Workspace: {0}" -f $RootPath)
    Write-Log ("Log: {0}" -f $LogPath)

    $started = [string]::IsNullOrWhiteSpace($StartAt)
    $visited = 0
    $rendered = 0
    $skipped = 0
    $failed = @()

    foreach ($item in $renderQueue) {
        if (-not $started) {
            if ($item.Id -eq $StartAt -or $item.SceneClass -eq $StartAt) {
                $started = $true
            } else {
                continue
            }
        }

        if ($Limit -gt 0 -and $visited -ge $Limit) {
            break
        }

        $visited += 1
        $scenePath = Join-Path $RootPath $item.SceneFile
        $sceneStem = [System.IO.Path]::GetFileNameWithoutExtension($item.SceneFile)
        $expectedOutput = Join-Path $RootPath ("media\videos\{0}\{1}\{2}.mp4" -f $sceneStem, $qualityDir, $item.SceneClass)

        Write-Log ("Queue item {0}: {1}" -f $item.Id, $item.SceneClass)

        if (-not (Test-Path -LiteralPath $scenePath)) {
            Write-Log ("FAILED: Scene file not found: {0}" -f $scenePath)
            $failed += $item
            continue
        }

        if ((Test-Path -LiteralPath $expectedOutput) -and -not $Force) {
            Write-Log ("SKIP: Existing output found: {0}" -f $expectedOutput)
            $skipped += 1
        } else {
            if ((Test-Path -LiteralPath $expectedOutput) -and $Force) {
                Write-Log ("FORCE: Removing existing output before render: {0}" -f $expectedOutput)
                Remove-Item -LiteralPath $expectedOutput -Force
            }

            $exitCode = Invoke-ManimRender -SceneFile $scenePath -SceneClass $item.SceneClass
            if ($DryRun -and $exitCode -eq 0) {
                $rendered += 1
                Write-Log ("DRY RUN: Would render output: {0}" -f $expectedOutput)
            } elseif ($exitCode -eq 0 -and (Test-Path -LiteralPath $expectedOutput)) {
                $rendered += 1
                Write-Log ("DONE: {0}" -f $expectedOutput)
            } else {
                $failed += $item
                Write-Log ("FAILED: {0}, exitCode={1}, expectedOutput={2}" -f $item.SceneClass, $exitCode, $expectedOutput)
            }
        }

        if ($DelaySeconds -gt 0) {
            Write-Log ("Sleeping {0} second(s) before next item." -f $DelaySeconds)
            Start-Sleep -Seconds $DelaySeconds
        }
    }

    Write-Log ("HD render queue finished. visited={0}, rendered={1}, skipped={2}, failed={3}" -f $visited, $rendered, $skipped, $failed.Count)

    if ($failed.Count -gt 0) {
        Write-Log "Failed items:"
        foreach ($item in $failed) {
            Write-Log ("- {0} {1}" -f $item.Id, $item.SceneClass)
        }
        exit 1
    }
} finally {
    Remove-Item -LiteralPath $lockPath -Force -ErrorAction SilentlyContinue
}
