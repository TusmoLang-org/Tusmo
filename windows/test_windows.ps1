$ErrorActionPreference = 'Stop'

Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host 'Tusmo Windows smoke tests'

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python was not found on PATH.'
}

if (-not (Get-Command gcc -ErrorAction SilentlyContinue)) {
    throw 'GCC was not found on PATH. Install the MSYS2 MinGW toolchain first.'
}

$env:TUSMO_CC = 'gcc'

Write-Host 'Checking compiler version...'
python tusmo.py --version

Write-Host 'Running language-server tests...'
python Extension/server/test_server.py -v

$sample = Join-Path $PSScriptRoot 'hello.tus'
@'
hawl main(): waxbo {
    qor("Tusmo Windows OK");
}
'@ | Set-Content -Path $sample -Encoding utf8

$generatedC = [System.IO.Path]::ChangeExtension($sample, '.c')
$generatedExe = [System.IO.Path]::ChangeExtension($sample, '.exe')

try {
    Write-Host 'Compiling and running a Tusmo program...'
    python tusmo.py $sample

    if (-not (Test-Path $generatedExe)) {
        throw "The compiler did not produce $generatedExe."
    }

    $output = & $generatedExe 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "The generated Windows executable exited with code $LASTEXITCODE.`n$output"
    }

    if ($output -notmatch 'Tusmo Windows OK') {
        throw "Unexpected program output:`n$output"
    }

    Write-Host 'Windows smoke tests passed.' -ForegroundColor Green
}
finally {
    Remove-Item -Force -ErrorAction SilentlyContinue $sample, $generatedC, $generatedExe
}
