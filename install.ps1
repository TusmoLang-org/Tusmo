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

function Get-VSCodeCliPaths {
  $paths = @()
  foreach ($commandName in @("code", "code-insiders")) {
    $command = Get-Command $commandName -ErrorAction SilentlyContinue
    if ($command -and $command.Source -and (Test-Path $command.Source)) {
      $paths += $command.Source
    }
  }

  $candidates = @()
  if ($env:LOCALAPPDATA) {
    $candidates += Join-Path $env:LOCALAPPDATA "Programs\Microsoft VS Code\bin\code.cmd"
    $candidates += Join-Path $env:LOCALAPPDATA "Programs\Microsoft VS Code Insiders\bin\code-insiders.cmd"
  }
  if ($env:ProgramFiles) {
    $candidates += Join-Path $env:ProgramFiles "Microsoft VS Code\bin\code.cmd"
    $candidates += Join-Path $env:ProgramFiles "Microsoft VS Code Insiders\bin\code-insiders.cmd"
  }
  if (${env:ProgramFiles(x86)}) {
    $candidates += Join-Path ${env:ProgramFiles(x86)} "Microsoft VS Code\bin\code.cmd"
  }

  foreach ($candidate in $candidates) {
    if ((Test-Path $candidate) -and $paths -notcontains $candidate) {
      $paths += $candidate
    }
  }
  return $paths
}

function Broadcast-UserEnvironmentChange {
  $source = @"
using System;
using System.Runtime.InteropServices;
public static class TusmoEnvironmentNotifier {
  [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
  public static extern IntPtr SendMessageTimeout(
    IntPtr hWnd, UInt32 Msg, UIntPtr wParam, string lParam,
    UInt32 fuFlags, UInt32 uTimeout, out UIntPtr lpdwResult);
}
"@
  if (-not ("TusmoEnvironmentNotifier" -as [type])) {
    Add-Type -TypeDefinition $source
  }
  [UIntPtr]$result = [UIntPtr]::Zero
  [void][TusmoEnvironmentNotifier]::SendMessageTimeout(
    [IntPtr]0xffff, [uint32]0x001A, [UIntPtr]::Zero, "Environment",
    [uint32]0x0002, [uint32]5000, [ref]$result)
}

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
  $vsixPath = Join-Path $temp $vsix
  $vsixDownloaded = $false
  try {
    Write-Host "Waxaa la soo dejinnaa VS Code extension..."
    Invoke-WebRequest -Uri "https://github.com/$repo/releases/latest/download/$vsix" -OutFile $vsixPath -ErrorAction Stop -UseBasicParsing
    if (-not (Test-Path $vsixPath) -or (Get-Item $vsixPath).Length -lt 1024) {
      throw "VSIX-ka la soo dejiyey waa madhan ama ma dhammaystirna."
    }
    $vsixDownloaded = $true
  } catch {
    Write-Warning "VS Code extension lama soo dejin: $($_.Exception.Message)"
  }

  if ($vsixDownloaded) {
    $codeCliPaths = @(Get-VSCodeCliPaths)
    $extensionId = "tusmolang-org.tusmo-language-support"
    $installedInEditor = $false

    if ($codeCliPaths.Count -gt 0) {
      foreach ($codeCli in $codeCliPaths) {
        try {
          Write-Host "Waxaa Tusmo extension-ka lagu rakibayaa: $codeCli"
          $installOutput = & $codeCli --install-extension $vsixPath --force 2>&1
          $installExitCode = $LASTEXITCODE
          if ($installExitCode -ne 0) {
            Write-Warning "VS Code wuu diiday rakibidda extension-ka (exit $installExitCode): $installOutput"
            continue
          }

          $installedExtensions = & $codeCli --list-extensions 2>$null
          $listExitCode = $LASTEXITCODE
          if ($listExitCode -eq 0 -and @($installedExtensions) -contains $extensionId) {
            $installedInEditor = $true
            Write-Host "Tusmo syntax highlighter waa lagu rakibay VS Code. Dib u fur VS Code ama samee 'Developer: Reload Window'."
          } else {
            Write-Warning "VS Code ma xaqiijin in extension-ka '$extensionId' la rakibay."
          }
        } catch {
          Write-Warning "Rakibidda VS Code extension-ka way fashilantay: $($_.Exception.Message)"
        }
      }
    }

    if (-not $installedInEditor) {
      $fallback = Join-Path $tusmoHome $vsix
      Copy-Item $vsixPath $fallback -Force
      Write-Warning "VS Code CLI lama helin ama rakibiddu way fashilantay. VSIX-ku halkan ayuu yaal: $fallback"
      Write-Host "Gacanta ugu rakib: code --install-extension `"$fallback`" --force"
    }
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
  Write-Host "Waxaa Tusmo PATH-ka user-ka ku daray: $binPath"
}

# Update this PowerShell process too, so programs started from it can find Tusmo.
$processEntries = @($env:Path -split ';' | Where-Object { $_ })
if ($processEntries -notcontains $binPath) {
  $env:Path = if ($env:Path) { "$binPath;$env:Path" } else { $binPath }
}
$resolvedTusmo = Get-Command tusmo -ErrorAction SilentlyContinue
if ($resolvedTusmo -and $resolvedTusmo.Source -ieq "$binPath\tusmo.cmd") {
  Write-Host "Tusmo hadda waxaa laga heli karaa PowerShell iyo apps laga bilaabo shell-kan."
} else {
  Write-Warning "PowerShell ma helin tusmo.cmd gudaha PATH-ka cusub: $binPath"
}

[Environment]::SetEnvironmentVariable("TUSMO_HOME", $tusmoHome, "User")
[Environment]::SetEnvironmentVariable("TUSMO_CC", "$tusmoHome\toolchain\cc.bat", "User")
[Environment]::SetEnvironmentVariable("TUSMO_INCLUDE_DIR", "$tusmoHome\stdlib", "User")
[Environment]::SetEnvironmentVariable("TUSMO_LIB_DIR", "$tusmoHome\lib", "User")
try {
  Broadcast-UserEnvironmentChange
} catch {
  Write-Warning "Environment-ka user-ka waa la keydiyey, laakiin ogeysiinta Windows way fashilantay: $($_.Exception.Message)"
}

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

Write-Host "Waxaa la shubay $tusmoHome. Fur app cusub ama dib u bilow apps-ka furnaa ka hor intaadan qorin 'tusmo'."

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
