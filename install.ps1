# Pop the Lock - Windows PowerShell installer/runner.
# Usage (PowerShell):
#   irm https://raw.githubusercontent.com/tobin-wq/pop-the-lock/main/install.ps1 | iex
# Usage (cmd.exe):
#   powershell -c "irm https://raw.githubusercontent.com/tobin-wq/pop-the-lock/main/install.ps1 | iex"

$ErrorActionPreference = "Stop"

$repoRaw = "https://raw.githubusercontent.com/tobin-wq/pop-the-lock/main"
$gameUrl = "$repoRaw/pop-the-lock.py"

# Find a working Python launcher (py, python, python3).
$python = $null
foreach ($cmd in @("py", "python", "python3")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $python = $cmd
        break
    }
}
if (-not $python) {
    Write-Host "Error: Python is required but was not found." -ForegroundColor Red
    Write-Host "Install it from https://www.python.org/downloads/ and try again."
    exit 1
}

Write-Host "~~~~~~~~~~~~~~~~~~~~~~~~~~"
Write-Host "Installing Pop the Lock..."
Write-Host "~~~~~~~~~~~~~~~~~~~~~~~~~~"

# Python on Windows does not ship the `curses` module - install windows-curses
# the first time if it is missing. Suppress stderr at the OS level via cmd.exe
# so PowerShell's "Stop" preference doesn't promote a Python traceback into a
# terminating NativeCommandError.
& cmd.exe /c "$python -c ""import curses"" 2>nul"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing windows-curses..."
    & $python -m pip install --quiet windows-curses
}

$tmpFile = Join-Path $env:TEMP ("pop_the_lock_" + [guid]::NewGuid().ToString() + ".py")
try {
    Invoke-WebRequest -Uri $gameUrl -OutFile $tmpFile -UseBasicParsing
    & $python $tmpFile
} finally {
    if (Test-Path $tmpFile) { Remove-Item $tmpFile -Force }
}
