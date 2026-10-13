# verify_install.ps1 - End-to-end check that a Tusmo Windows release tarball
# can be installed and used, exactly the way install.ps1 does it.
#
# Usage:  .github/scripts/verify_install.ps1 -Tarball tusmo-windows-x86_64.tar.gz
#
# Runs entirely offline: no GitHub downloads, no VS Code step.

param(
  [Parameter(Mandatory = $true)][string]$Tarball
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Tarball)) {
  Write-Error "verify_install: tarball not found: $Tarball"
}
$Tarball = (Resolve-Path $Tarball).Path

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$work = Join-Path ([System.IO.Path]::GetTempPath()) ("tusmo-verify-" + [System.Guid]::NewGuid().ToString("N").Substring(0, 8))
$sandboxHome = Join-Path $work "home"
$scratch = Join-Path $work "project"
New-Item -ItemType Directory -Force -Path $sandboxHome, $scratch | Out-Null

$script:pass = 0
$script:fail = 0
function Step($msg) { Write-Host "`n==> $msg" }
function Ok($msg)   { Write-Host "  [OK]   $msg"; $script:pass++ }
function Bad($msg)  { Write-Host "  [FAIL] $msg"; $script:fail++ }

# ---------------------------------------------------------------- install
Step "installing $Tarball into a sandbox LOCALAPPDATA"
$sandboxLocalAppData = Join-Path $sandboxHome "AppData\Local"
New-Item -ItemType Directory -Force -Path $sandboxLocalAppData | Out-Null
$env:TUSMO_INSTALL_FROM = $Tarball
$env:TUSMO_NO_VSCODE = "1"
$oldLocalAppData = $env:LOCALAPPDATA
$env:LOCALAPPDATA = $sandboxLocalAppData
$oldPath = $env:Path
$oldUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$oldUserTusmoHome = [Environment]::GetEnvironmentVariable("TUSMO_HOME", "User")
$oldUserTusmoCc = [Environment]::GetEnvironmentVariable("TUSMO_CC", "User")
$oldUserTusmoIncludeDir = [Environment]::GetEnvironmentVariable("TUSMO_INCLUDE_DIR", "User")
$oldUserTusmoLibDir = [Environment]::GetEnvironmentVariable("TUSMO_LIB_DIR", "User")

try {
  & pwsh -NoProfile -File (Join-Path $repoRoot "install.ps1") 2>&1 | Tee-Object -FilePath (Join-Path $work "install.log")
  if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
    Ok "install.ps1 completed"
  } else {
    Bad "install.ps1 exited with $LASTEXITCODE"
    Get-Content (Join-Path $work "install.log")
  }
} finally {
  $env:LOCALAPPDATA = $oldLocalAppData
  $env:Path = $oldPath
  Remove-Item Env:\TUSMO_INSTALL_FROM -ErrorAction SilentlyContinue
  Remove-Item Env:\TUSMO_NO_VSCODE -ErrorAction SilentlyContinue
}

$tusmoHome = Join-Path $sandboxLocalAppData "Tusmo"
$tusmoCmd = Join-Path $tusmoHome "bin\tusmo.cmd"

if (Test-Path $tusmoCmd) { Ok "bin\tusmo.cmd exists" } else { Bad "bin\tusmo.cmd missing"; Get-ChildItem -Recurse $tusmoHome -ErrorAction SilentlyContinue | Select-Object -First 40 }
if (Test-Path (Join-Path $tusmoHome "bin\tusmo-app.exe")) { Ok "bin\tusmo-app.exe exists" } else { Bad "bin\tusmo-app.exe missing" }

$expectedBinPath = Join-Path $tusmoHome "bin"
$installedUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (@($installedUserPath -split ';') -contains $expectedBinPath) {
  Ok "Tusmo bin directory was persisted in the user PATH"
} else {
  Bad "Tusmo bin directory was not persisted in the user PATH"
}

# The launcher must work with no environment set at all.
$env:TUSMO_HOME = $null
$env:TUSMO_CC = $null
$env:TUSMO_INCLUDE_DIR = $null
$env:TUSMO_LIB_DIR = $null

$versionLog = & $tusmoCmd --version 2>&1 | Out-String
if ($versionLog -match "Tusmo Version: 2\.0\.1-beta") {
  Ok "tusmo --version works without any environment set: $($versionLog.Trim())"
} else {
  Bad "tusmo --version failed: $versionLog"
}

$cc = Join-Path $tusmoHome "toolchain\cc.bat"
if (Test-Path $cc) {
  $ccLog = & $cc --version 2>&1 | Out-String
  if ($LASTEXITCODE -eq 0) { Ok "bundled toolchain works: $(($ccLog -split "`n")[0])" }
  else { Bad "bundled toolchain does not run: $ccLog" }
} else {
  Bad "toolchain\cc.bat missing from the bundle"
}

# Test the native compiler/linker directly before involving Tusmo. This keeps
# a Windows toolchain failure separate from a Tusmo code-generation failure.
Step "compiling and running a native C toolchain smoke test"
@"
#include <stdio.h>
int main(void) {
    puts("Tusmo toolchain smoke test");
    return 0;
}
"@ | Set-Content -Path (Join-Path $scratch "toolchain-smoke.c") -Encoding ASCII
$smokeExe = Join-Path $scratch "toolchain-smoke.exe"
$smokeLog = Join-Path $work "toolchain-smoke.log"
Push-Location $scratch
try {
  & $cc -O2 -o $smokeExe (Join-Path $scratch "toolchain-smoke.c") 2>&1 | Tee-Object -FilePath $smokeLog | Out-Null
  $smokeExit = $LASTEXITCODE
} finally { Pop-Location }
if ($smokeExit -eq 0 -and (Test-Path $smokeExe)) {
  $smokeOut = (& $smokeExe 2>&1 | Out-String).Trim()
  if ($smokeOut -eq "Tusmo toolchain smoke test") { Ok "bundled compiler and linker produced a runnable native binary" }
  else { Bad "native smoke-test output mismatch: '$smokeOut'" }
} else {
  Bad "bundled compiler/linker smoke test failed"
  Get-Content $smokeLog -ErrorAction SilentlyContinue
}

# Link Raylib without opening a window. This verifies that the release contains
# the native library and platform linker inputs required by Raylib programs.
Step "linking a Raylib program"
@"
#include "raylib/raylib.h"
int main(void) {
    InitWindow(1, 1, "Tusmo Raylib smoke test");
    CloseWindow();
    return 0;
}
"@ | Set-Content -Path (Join-Path $scratch "raylib-smoke.c") -Encoding ASCII
$raylibName = if ($env:TRIPLET -eq "windows-x86_64") { "libraylib.a.lib" } else { "libraylib.a" }
$raylib = Join-Path $tusmoHome "stdlib\raylib\$raylibName"
$raylibExe = Join-Path $scratch "raylib-smoke.exe"
$raylibLog = Join-Path $work "raylib-smoke.log"
$raylibArgs = @(
  "-O2",
  "-I$(Join-Path $tusmoHome "stdlib")",
  "-o",
  $raylibExe,
  (Join-Path $scratch "raylib-smoke.c"),
  $raylib
)
Push-Location $scratch
try {
  & $cc @raylibArgs 2>&1 | Tee-Object -FilePath $raylibLog | Out-Null
  $raylibExit = $LASTEXITCODE
} finally { Pop-Location }
if ($raylibExit -eq 0 -and (Test-Path $raylibExe)) {
  Ok "platform Raylib library links successfully"
} else {
  Bad "platform Raylib library failed to link"
  Get-Content $raylibLog -ErrorAction SilentlyContinue
}

if (Test-Path (Join-Path $tusmoHome "bin\tusmo-hover.exe")) {
  Ok "language server (bin\tusmo-hover.exe) is installed"
} else {
  Bad "bin\tusmo-hover.exe missing from the bundle"
}

# --------------------------------------------------- compile & run hello
Step "compiling and running a program (outside the install dir)"
@"
hawl main(): waxbo {
    qor("Salaan Tusmo!");
}
"@ | Set-Content -Path (Join-Path $scratch "hello.tus") -Encoding UTF8

Push-Location $scratch
try {
  & $tusmoCmd hello.tus 2>&1 | Tee-Object -FilePath (Join-Path $work "compile.log") | Out-Null
} finally { Pop-Location }

$helloBinary = Join-Path $scratch "hello.exe"
if (Test-Path $helloBinary) {
  Ok "native binary produced"
  $out = (& $helloBinary 2>&1 | Out-String).Trim()
  if ($out -eq "Salaan Tusmo!") { Ok "binary runs and prints: $out" }
  else { Bad "binary output mismatch: '$out'" }
} else {
  Bad "no hello binary produced"
  Get-ChildItem -Force $scratch | Format-Table -AutoSize | Out-String | Write-Host
  Get-Content (Join-Path $work "compile.log") -ErrorAction SilentlyContinue
}

# ------------------------------------- language features that pull in headers
Step "compiling a program that uses stdlib + embedded types"
@"
hawl main(): waxbo {
    keyd:tix:tiro lambiyada = [1, 2, 3];
    keyd:eray magac = "Tusmo";
    keyd:qaamuus qof = {"magac": "Ali", "da": 25};
    qor("Lambiyada:", dherer(lambiyada));
    qor("Erayga:", dherer(magac));
    qor("Nooca:", nooc(magac));
    qor("Qof:", qof);
}
"@ | Set-Content -Path (Join-Path $scratch "features.tus") -Encoding UTF8

Push-Location $scratch
try {
  & $tusmoCmd features.tus 2>&1 | Tee-Object -FilePath (Join-Path $work "features.log") | Out-Null
} finally { Pop-Location }

$featuresBinary = Join-Path $scratch "features.exe"
if (Test-Path $featuresBinary) {
  Ok "arrays/dicts/strings compile and link"
  $out = (& $featuresBinary 2>&1 | Out-String).Trim()
  Ok "feature program output: $($out -replace "`r?`n", ' ')"
} else {
  Bad "array/dict program failed to compile"
  Get-ChildItem -Force $scratch | Format-Table -AutoSize | Out-String | Write-Host
  Get-Content (Join-Path $work "features.log") -ErrorAction SilentlyContinue
}

# ------------------------------------------- broken programs must be rejected
Step "rejecting a program with a semantic error"
@"
hawl main(): waxbo {
    keyd:tiro x;
    qor(x);
}
"@ | Set-Content -Path (Join-Path $scratch "broken.tus") -Encoding UTF8

Remove-Item (Join-Path $scratch "broken.exe") -ErrorAction SilentlyContinue
Push-Location $scratch
try {
  & $tusmoCmd broken.tus 2>&1 | Tee-Object -FilePath (Join-Path $work "broken.log") | Out-Null
} finally { Pop-Location }

if (Test-Path (Join-Path $scratch "broken.exe")) {
  Bad "a program with an uninitialized variable produced a binary"
} else {
  Ok "no binary produced for an invalid program"
}

# --------------------------------------------------------------- summary
Write-Host "`n==> verify_install: $script:pass passed, $script:fail failed"
[Environment]::SetEnvironmentVariable("Path", $oldUserPath, "User")
[Environment]::SetEnvironmentVariable("TUSMO_HOME", $oldUserTusmoHome, "User")
[Environment]::SetEnvironmentVariable("TUSMO_CC", $oldUserTusmoCc, "User")
[Environment]::SetEnvironmentVariable("TUSMO_INCLUDE_DIR", $oldUserTusmoIncludeDir, "User")
[Environment]::SetEnvironmentVariable("TUSMO_LIB_DIR", $oldUserTusmoLibDir, "User")
Remove-Item -Recurse -Force $work -ErrorAction SilentlyContinue
if ($script:fail -ne 0) { exit 1 }
exit 0
