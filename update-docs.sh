#!/bin/bash
# Update docs after editing .md files
# Source .md files are in docs-src/, built output goes to docs/

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/docs-src"
OUTPUT_DIR="$SCRIPT_DIR/docs"

echo "Building MkDocs site from $SRC_DIR..."

# Check if source directory exists
if [ ! -d "$SRC_DIR" ]; then
    echo "Error: docs-src/ directory not found"
    echo "Create docs-src/ with your .md source files"
    exit 1
fi

# Build to site directory
mkdocs build --site-dir site

echo "Copying to docs folder..."
cp -r site/* "$OUTPUT_DIR/"

# Add favicon
cp "$SRC_DIR/favicon.svg" "$OUTPUT_DIR/" 2>/dev/null || true

echo "Cleaning up..."
rm -rf site/

echo "Done! Commit and push the changes:"
echo "  git add docs/"
echo '  git commit -m "Update documentation"'
echo "  git push origin main"
