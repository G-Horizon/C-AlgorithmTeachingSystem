[CmdletBinding()]
param(
    [switch]$Build,
    [switch]$SkipBuild,
    [switch]$SkipDemoData,
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
$Curriculum = Join-Path $Frontend "src\data\curriculum.ts"
$Problems = Join-Path $Root "backend\app\content\problems.py"

$script:FailureCount = 0

function Add-CheckResult {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Detail = ""
    )

    if ($Passed) {
        Write-Host "[OK]   $Name $Detail"
    } else {
        $script:FailureCount += 1
        Write-Host "[FAIL] $Name $Detail"
    }
}

Write-Host "Checking demo integrity..."
Write-Host "Root: $Root"
Write-Host ""

& $Python -m py_compile `
    (Join-Path $Root "backend\app\content\problems.py") `
    (Join-Path $Root "backend\app\main.py") `
    (Join-Path $Root "backend\app\storage.py") `
    (Join-Path $Root "scripts\seed_demo_data.py")
Add-CheckResult "Python syntax" ($LASTEXITCODE -eq 0)

$curriculumText = Get-Content -Encoding UTF8 $Curriculum -Raw
$curriculumDataText = ((Get-ChildItem (Split-Path $Curriculum) -Filter "*.ts") | ForEach-Object {
    Get-Content -Encoding UTF8 $_.FullName -Raw
}) -join "`n"
$problemFiles = Get-ChildItem (Split-Path $Problems) -Filter "*problems.py"
$problemsText = ($problemFiles | ForEach-Object { Get-Content -Encoding UTF8 $_.FullName -Raw }) -join "`n"

$towerCount = ([regex]::Matches($curriculumText, 'id: "recurrence-number-tower"')).Count
$recurrenceStart = $curriculumText.IndexOf('id: "recurrence"')
$towerIndex = $curriculumText.IndexOf('id: "recurrence-number-tower"')
$recursionStart = $curriculumText.IndexOf('id: "recursion"')
$towerInRecurrence = $towerCount -eq 1 -and $recurrenceStart -ge 0 -and $towerIndex -gt $recurrenceStart -and $towerIndex -lt $recursionStart
Add-CheckResult "Number tower lesson placement" $towerInRecurrence "count=$towerCount"

$problemIdPattern = 'id: "([a-z0-9-]+)",\s*title: "[^"]+",\s*difficulty:'
$frontendProblemIds = @(
    @([regex]::Matches($curriculumDataText, $problemIdPattern) | ForEach-Object { $_.Groups[1].Value }) +
    @([regex]::Matches($curriculumDataText, 'problem\(\s*"([a-z0-9-]+)"') | ForEach-Object { $_.Groups[1].Value }) |
    Sort-Object -Unique
)
$backendProblemIds = @(
    @([regex]::Matches($problemsText, 'id="([a-z0-9-]+)"') | ForEach-Object { $_.Groups[1].Value }) +
    @([regex]::Matches($problemsText, '(?m)^\s*"([a-z0-9-]+)":\s*[a-z_]*problem\(') | ForEach-Object { $_.Groups[1].Value }) +
    @([regex]::Matches($problemsText, '(?m)^\s*add\(\s*"([a-z0-9-]+)"') | ForEach-Object { $_.Groups[1].Value }) |
    Sort-Object -Unique
)
$missingBackend = @($frontendProblemIds | Where-Object { $_ -notin $backendProblemIds })
$missingFrontend = @($backendProblemIds | Where-Object { $_ -notin $frontendProblemIds })
Add-CheckResult "Problem ids referenced by frontend exist in backend" ($missingBackend.Count -eq 0) "frontend=$($frontendProblemIds.Count) backend=$($backendProblemIds.Count)"
if ($missingBackend.Count -gt 0) {
    $missingBackend | ForEach-Object { Write-Host "       missing backend: $_" }
}
Add-CheckResult "Backend problem ids are exposed in frontend" ($missingFrontend.Count -eq 0) "backend=$($backendProblemIds.Count) frontend=$($frontendProblemIds.Count)"
if ($missingFrontend.Count -gt 0) {
    $missingFrontend | ForEach-Object { Write-Host "       missing frontend: $_" }
}

$mediaMatches = @([regex]::Matches($curriculumText, '(?:videoUrl|previewImage): "(/[^"]+)"'))
$missingMedia = @()
foreach ($match in $mediaMatches) {
    $url = $match.Groups[1].Value
    $relative = if ($url.StartsWith("/videos/")) {
        Join-Path "media" $url.TrimStart("/")
    } elseif ($url.StartsWith("/previews/")) {
        Join-Path "media" $url.TrimStart("/")
    } else {
        $url.TrimStart("/")
    }
    $path = Join-Path $Root $relative
    if (-not (Test-Path $path)) {
        $missingMedia += $url
    }
}
Add-CheckResult "Media references exist" ($missingMedia.Count -eq 0) "checked=$($mediaMatches.Count)"
if ($missingMedia.Count -gt 0) {
    $missingMedia | ForEach-Object { Write-Host "       missing media: $_" }
}

if (-not $SkipDemoData) {
    $dbPath = Join-Path $Root "backend\app\.data\submissions.sqlite3"
    if (Test-Path $dbPath) {
        $demoCount = & $Python (Join-Path $Root "scripts\seed_demo_data.py") --count-only
        Add-CheckResult "Demo seed submissions" ([int]$demoCount -gt 0) "count=$demoCount"
    } else {
        Add-CheckResult "Demo seed submissions" $false "database not found"
    }
}

if ($Build -and -not $SkipBuild) {
    Push-Location $Frontend
    try {
        npm.cmd run build
        Add-CheckResult "Frontend build" ($LASTEXITCODE -eq 0)
    } finally {
        Pop-Location
    }
} else {
    Add-CheckResult "Frontend build skipped" $true "run 'npm.cmd run build' from frontend, or pass -Build outside restricted shells"
}

Write-Host ""
if ($script:FailureCount -gt 0) {
    Write-Host "Demo check finished with $script:FailureCount failure(s)."
    exit 1
}

Write-Host "Demo check passed."
