#!/bin/bash
# Update docs after editing .md files

echo "Building MkDocs site..."
mkdocs build

echo "Copying to docs folder..."
cp -r site/* docs/

echo "Cleaning up..."
rm -rf site/

echo "Done! Commit and push the changes:"
echo "  git add docs/"
echo '  git commit -m "Update documentation"'
echo "  git push origin main"
