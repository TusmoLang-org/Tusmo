$ErrorActionPreference = "Stop"

$repo = "TusmoLang-org/Tusmo"
$asset = "tusmo-windows-x86_64.tar.gz"
$tusmoHome = "$env:LOCALAPPDATA\Tusmo"
$temp = New-TemporaryFile
Remove-Item $temp
New-Item -ItemType Directory -Force -Path $temp | Out-Null

Write-Host "Waxaa la soo dejinnaa $asset..."
Invoke-WebRequest -Uri "https://github.com/$repo/releases/latest/download/$asset" -OutFile "$temp\$asset"

tar -xf "$temp\$asset" -C $temp
Remove-Item -Recurse -Force "$tusmoHome" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $tusmoHome | Out-Null
Move-Item "$temp\*" $tusmoHome

# Optional VS Code extension
$vsix = "tusmo-vscode.vsix"
if (Get-Command code -ErrorAction SilentlyContinue) {
  Write-Host "Waxaa la soo dejinnaa VS Code extension..."
  $vsixPath = "$temp\$vsix"
  try {
    Invoke-WebRequest -Uri "https://github.com/$repo/releases/latest/download/$vsix" -OutFile $vsixPath -ErrorAction Stop
    # Remove old IDs (both old/new publishers, casing variants)
    $ids = @("tusmolang-org.tusmo-language-support","TusmoLang-org.tusmo-language-support","tusmo-official.tusmo-language-support")
    foreach ($id in $ids) { code --uninstall-extension $id *> $null }
    # Remove stale folders if they remain
    Get-ChildItem -Path "$env:USERPROFILE\\.vscode\\extensions" -Directory -Filter "tusmo*-language-support*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    try {
      code --install-extension $vsixPath --force | Out-Null
    } catch {
      # fallback: keep the VSIX for manual install
      $fallback = "$env:TUSMO_HOME\\$vsix"
      Copy-Item $vsixPath $fallback -Force
      Write-Host "Ma suurtagelin in VSIX si toos ah loo rakibo. Ku rakib: code --install-extension $fallback --force"
    }
  } catch {}
} else {
  # Haddii code aanu jirin, tirtir galalka oo soo dejiso VSIX si gacanta loogu rakibo
  Get-ChildItem -Path "$env:USERPROFILE\\.vscode\\extensions" -Directory -Filter "tusmo*-language-support*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
  $vsixPath = "$env:TUSMO_HOME\\$vsix"
  try {
    Invoke-WebRequest -Uri "https://github.com/$repo/releases/latest/download/$vsix" -OutFile $vsixPath -ErrorAction Stop
    Write-Host "VSIX waa la soo dejiyey: $vsixPath"
    Write-Host "   Ku rakib gacanta: code --install-extension $vsixPath --force"
  } catch {}
}

Remove-Item -Recurse -Force $temp

$binPath = "$tusmoHome\bin"
if (-not ($env:Path -split ';' | Where-Object { $_ -eq $binPath })) {
  [Environment]::SetEnvironmentVariable("Path", "$binPath;$env:Path", "User")
}

[Environment]::SetEnvironmentVariable("TUSMO_HOME", $tusmoHome, "User")
[Environment]::SetEnvironmentVariable("TUSMO_CC", "$tusmoHome\toolchain\cc.bat", "User")
[Environment]::SetEnvironmentVariable("TUSMO_LIB_DIR", "$tusmoHome\lib", "User")
[Environment]::SetEnvironmentVariable("TUSMO_INCLUDE_DIR", "$tusmoHome\runtime", "User")

Write-Host "Waxaa lagu shubay $tusmoHome. Mar kale fur terminal-ka (shell) ka dibna qor 'tusmo'."

# Nadiifi shaashadda
Clear-Host

# Farshaxanka ASCII ee magaca "TUSMO"
$asciiArt = @"
  _______ _    _  _____ __  __  ____  

 |__   __| |  | |/ ____|  \/  |/ __ \ 
    | |  | |  | | (___ | \  / | |  | |
    | |  | |  | |\___ \| |\/| | |  | |
    | |  | |__| |____) | |  | | |__| |
    |_|   \____/|_____/|_|  |_|\____/ 
"@

# Ku daabac midab buluug ah (Cyan)
Write-Host $asciiArt -ForegroundColor Cyan

Write-Host "==========================================" -ForegroundColor Gray
Write-Host "      Ku soo dhawaaw Luuqada Tusmo" -ForegroundColor Green -Object
Write-Host "==========================================" -ForegroundColor Gray
