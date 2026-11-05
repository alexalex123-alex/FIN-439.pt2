$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$localPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
$buildPython = Join-Path $PSScriptRoot '../../work/venv/Scripts/python.exe'
$priorLabPython = Join-Path $env:USERPROFILE 'Documents/Codex/2026-11-03/wha/work/venv/Scripts/python.exe'
if (Test-Path -LiteralPath $localPython) {
    $labPython = $localPython
} elseif (Test-Path -LiteralPath $buildPython) {
    $labPython = (Resolve-Path -LiteralPath $buildPython).Path
} elseif (Test-Path -LiteralPath $priorLabPython) {
    $labPython = $priorLabPython
} else {
    $bundledPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
    if (Test-Path -LiteralPath $bundledPython) {
        $basePython = $bundledPython
    } else {
        $basePython = (Get-Command python -ErrorAction Stop).Source
    }
    & $basePython -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Python environment creation failed. Install Python and retry.' }
    $labPython = $localPython
    & $labPython -m pip install --no-cache-dir -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
}
& $labPython -m streamlit run app.py --server.address 127.0.0.1 --server.port 8519 --browser.gatherUsageStats false
