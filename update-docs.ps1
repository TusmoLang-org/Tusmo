# Update docs after editing .md files (Windows PowerShell version)
# Source .md files are in docs-src/, built output goes to docs/

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$SRC_DIR = Join-Path $SCRIPT_DIR "docs-src"
$OUTPUT_DIR = Join-Path $SCRIPT_DIR "docs"

Write-Host "Building MkDocs site from $SRC_DIR..." -ForegroundColor Cyan

# Check if source directory exists
if (-not (Test-Path -Path $SRC_DIR)) {
    Write-Host "Error: docs-src/ directory not found" -ForegroundColor Red
    Write-Host "Create docs-src/ with your .md source files"
    exit 1
}

# Build to site directory
# Hubi in mkdocs uu ku rakiban yahay Python-kaaga
mkdocs build --site-dir site

Write-Host "Copying to docs folder..." -ForegroundColor Yellow
if (-not (Test-Path -Path $OUTPUT_DIR)) { New-Item -ItemType Directory -Path $OUTPUT_DIR }

# Copy built site to docs folder
Copy-Item -Path "site\*" -Destination $OUTPUT_DIR -Recurse -Force

# Add favicon if exists
if (Test-Path -Path "$SRC_DIR\favicon.svg") {
    Copy-Item -Path "$SRC_DIR\favicon.svg" -Destination $OUTPUT_DIR -Force
}

Write-Host "Cleaning up..." -ForegroundColor Gray
Remove-Item -Path "site" -Recurse -Force

Write-Host "Done! Commit and push the changes:" -ForegroundColor Green
Write-Host "  git add docs/"
Write-Host '  git commit -m "Update documentation"'
Write-Host "  git push origin main"