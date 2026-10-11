# Tusmo installer (Windows PowerShell)
#
# Environment overrides (all optional):
#   $env:TUSMO_INSTALL_FROM = "C:\path\tusmo-windows-x86_64.tar.gz"  # local tarball
#   $env:TUSMO_HOME         = "D:\Tusmo"                            # install location
#   $env:TUSMO_NO_VSCODE    = "1"                                   # skip VS Code step
$ErrorActionPreference = "Stop"

$repo = "TusmoLang-org/Tusmo"
$asset = "tusmo-windows-x86_64.tar.gz"
$tusmoHome = if ($env:TUSMO_HOME) { $env:TUSMO_HOME } else { "$env:LOCALAPPDATA\Tusmo" }
$temp = New-TemporaryFile
Remove-Item $temp
New-Item -ItemType Directory -Force -Path $temp | Out-Null

# --------------------------------------------- 1. fetch the release asset
if ($env:TUSMO_INSTALL_FROM) {
  Write-Host "Waxaan isticmaalayaa faylka deegaanka: $env:TUSMO_INSTALL_FROM"
  if (-not (Test-Path $env:TUSMO_INSTALL_FROM)) {
    Write-Error "Khalad: faylka ma jiro: $env:TUSMO_INSTALL_FROM"
  }
  Copy-Item $env:TUSMO_INSTALL_FROM "$temp\$asset" -Force
} else {
  Write-Host "Waxaa la soo dejinnaa $asset..."
  try {
    Invoke-WebRequest -Uri "https://github.com/$repo/releases/latest/download/$asset" -OutFile "$temp\$asset" -UseBasicParsing
  } catch {
    Write-Error "Khalad: soo dejinta '$asset' way fashilantay. Hubi internet-ka ama booqo https://github.com/$repo/releases"
  }
}

# ---------------------------------- 2. unpack, then swap in atomically
# The previous install is only removed after a successful extraction so a
# failed download can never leave a broken install behind.
$extract = Join-Path $temp "extract"
New-Item -ItemType Directory -Force -Path $extract | Out-Null
tar -xf "$temp\$asset" -C $extract
if ($LASTEXITCODE -ne 0) { Write-Error "Khalad: faylka tar-ka waa xumaaday: $asset" }
if (-not ((Test-Path "$extract\bin\tusmo.cmd") -or (Test-Path "$extract\bin\tusmo.exe"))) {
  Write-Error "Khalad: tarball-ku ma jiro bin\tusmo - qalabkan waa xumaaday."
}

Remove-Item -Recurse -Force $tusmoHome -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $tusmoHome | Out-Null
Get-ChildItem -Force -Path $extract | Move-Item -Destination $tusmoHome

# ------------------------------------------------- 3. VS Code extension
if ($env:TUSMO_NO_VSCODE -ne "1") {
  $vsix = "tusmo-vscode.vsix"
  if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "Waxaa la soo dejinnaa VS Code extension..."
    $vsixPath = Join-Path $temp $vsix
    try {
      Invoke-WebRequest -Uri "https://github.com/$repo/releases/latest/download/$vsix" -OutFile $vsixPath -ErrorAction Stop -UseBasicParsing
      $ids = @("tusmolang-org.tusmo-language-support","TusmoLang-org.tusmo-language-support","tusmo-official.tusmo-language-support")
      foreach ($id in $ids) { code --uninstall-extension $id *> $null }
      Get-ChildItem -Path "$env:USERPROFILE\.vscode\extensions" -Directory -Filter "tusmo*-language-support*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
      try {
        code --install-extension $vsixPath --force | Out-Null
      } catch {
        $fallback = Join-Path $tusmoHome $vsix
        Copy-Item $vsixPath $fallback -Force
        Write-Host "Ma suurtagelin in VSIX si toos ah loo rakibo. Ku rakib: code --install-extension `"$fallback`" --force"
      }
    } catch {}
  } else {
    Get-ChildItem -Path "$env:USERPROFILE\.vscode\extensions" -Directory -Filter "tusmo*-language-support*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $vsixPath = Join-Path $tusmoHome $vsix
    try {
      Invoke-WebRequest -Uri "https://github.com/$repo/releases/latest/download/$vsix" -OutFile $vsixPath -ErrorAction Stop -UseBasicParsing
      Write-Host "VSIX waa la soo dejiyey: $vsixPath"
      Write-Host "   Ku rakib gacanta: code --install-extension `"$vsixPath`" --force"
    } catch {}
  }
}

# ------------------------------------- 4. PATH + environment (user level)
# Only touch the *user* PATH: merging $env:Path (user + machine) back into the
# user hive would duplicate every system entry on the first install.
$binPath = "$tusmoHome\bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$userEntries = @($userPath -split ';' | Where-Object { $_ })
if ($userEntries -notcontains $binPath) {
  $newUserPath = if ($userEntries.Count -gt 0) { "$binPath;$userPath" } else { $binPath }
  [Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
  $env:Path = "$binPath;$env:Path"
  Write-Host "Waxaa PATH-ka user-ka ku daray $binPath (fur terminal cusub si ay u shaqeeyo)."
}

[Environment]::SetEnvironmentVariable("TUSMO_HOME", $tusmoHome, "User")
[Environment]::SetEnvironmentVariable("TUSMO_CC", "$tusmoHome\toolchain\cc.bat", "User")
[Environment]::SetEnvironmentVariable("TUSMO_INCLUDE_DIR", "$tusmoHome\stdlib", "User")
[Environment]::SetEnvironmentVariable("TUSMO_LIB_DIR", "$tusmoHome\lib", "User")

# --------------------------------------------- 5. sanity check (current session)
$env:TUSMO_HOME = $tusmoHome
$env:TUSMO_CC = "$tusmoHome\toolchain\cc.bat"
$env:TUSMO_INCLUDE_DIR = "$tusmoHome\stdlib"
$env:TUSMO_LIB_DIR = "$tusmoHome\lib"
$installed = $false
try {
  & "$binPath\tusmo.cmd" --version | Out-Null
  if ($LASTEXITCODE -eq 0) { $installed = $true }
} catch {}
if (-not $installed) {
  Write-Warning "Digniin: 'tusmo --version' ma shaqeeyn; fadlan xakamee $tusmoHome"
}

Remove-Item -Recurse -Force $temp -ErrorAction SilentlyContinue

Write-Host "Waxaa la shubay $tusmoHome. Mar kale fur terminal-ka (shell) ka dibna qor 'tusmo'."

# ------------------------------------------------- banner
try { Clear-Host } catch {}

$asciiArt = @"
  _______ _    _  _____ __  __  ____  

 |__   __| |  | |/ ____|  \/  |/ __ \ 
    | |  | |  | | (___ | \  / | |  | |
    | |  | |  | |\___ \| |\/| | |  | |
    | |  | |__| |____) | |  | | |__| |
    |_|   \____/|_____/|_|  |_|\____/ 
"@

Write-Host $asciiArt -ForegroundColor Cyan

Write-Host "==========================================" -ForegroundColor Gray
Write-Host "      Ku soo dhawaaw Luuqada Tusmo" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Gray
if ($installed) {
  Write-Host "  Rakibaad: OK" -ForegroundColor Green
} else {
  Write-Host "  Rakibaad: aan la xaqiijin" -ForegroundColor Yellow
}
Write-Host "==========================================" -ForegroundColor Gray
