#!/usr/bin/env bash
set -euo pipefail

REPO="tusmo-official/Tusmo"
OS=$(uname -s)
ARCH=$(uname -m)

case "$OS/$ARCH" in
  Linux/x86_64) ASSET="tusmo-linux-x86_64.tar.gz" ;;
  Darwin/arm64) ASSET="tusmo-macos-arm64.tar.gz" ;;
  Darwin/x86_64)
    echo "Nidaamkan lama taageero (Intel macOS). Taageero: macOS ARM64." >&2
    exit 1
    ;;
  *) echo "Nidaamkan lama taageero: $OS $ARCH" >&2; exit 1 ;;
esac

TUSMO_HOME="$HOME/.tusmo"
mkdir -p "$TUSMO_HOME"
TMP=$(mktemp -d)
echo "La soo dejinnayo $ASSET..."
curl -fsSL "https://github.com/$REPO/releases/latest/download/$ASSET" -o "$TMP/$ASSET"
tar -xzf "$TMP/$ASSET" -C "$TUSMO_HOME"
rm -rf "$TMP"

if command -v sudo >/dev/null 2>&1; then
  sudo ln -sf "$TUSMO_HOME/bin/tusmo" /usr/local/bin/tusmo
else
  mkdir -p "$HOME/.local/bin"
  ln -sf "$TUSMO_HOME/bin/tusmo" "$HOME/.local/bin/tusmo"
  if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  fi
fi

cat > "$TUSMO_HOME/env.sh" <<'EOF'
export TUSMO_HOME="$HOME/.tusmo"
export TUSMO_CC="$TUSMO_HOME/toolchain/cc"
export TUSMO_LIB_DIR="$TUSMO_HOME/lib"
export TUSMO_INCLUDE_DIR="$TUSMO_HOME/runtime"
EOF

echo "Waxaa lagu shubay $TUSMO_HOME. Mar kale fur terminal-ka (shell) ka dibna qor 'tusmo'."
