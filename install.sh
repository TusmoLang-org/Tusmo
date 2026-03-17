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
echo "Waxaa la soo dejinnaa $ASSET..."
curl -fsSL "https://github.com/$REPO/releases/latest/download/$ASSET" -o "$TMP/$ASSET"
tar -xzf "$TMP/$ASSET" -C "$TUSMO_HOME"

# Optional: install VS Code extension if VSIX asset exists and 'code' is available
VSIX="tusmo-vscode.vsix"
if command -v code >/dev/null 2>&1 || command -v codium >/dev/null 2>&1; then
  echo "Waxaa la soo dejinnaa VS Code extension..."
  if curl -fsSL "https://github.com/$REPO/releases/latest/download/$VSIX" -o "$TMP/$VSIX"; then
    CODE_BIN=$(command -v code || command -v codium)
    "$CODE_BIN" --install-extension "$TMP/$VSIX" --force >/dev/null 2>&1 || true
  fi
fi
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





# Nadiifi shaashadda
clear

# Midabada (ANSI Codes)
CYAN='\033[0;36m'
GREEN='\033[0;32m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color (Midab la'aan si loo joojiyo)

# Farshaxanka ASCII ee magaca "TUSMO"
asciiArt="
  _______ _    _  _____ __  __  ____  

 |__   __| |  | |/ ____|  \/  |/ __ \ 
    | |  | |  | | (___ | \  / | |  | |
    | |  | |  | |\___ \| |\/| | |  | |
    | |  | |__| |____) | |  | | |__| |
    |_|   \____/|_____/|_|  |_|\____/ 
"

# Ku daabac midab buluug ah (Cyan)
echo -e "${CYAN}${asciiArt}${NC}"

echo -e "${GRAY}==========================================${NC}"
echo -e "${GREEN}      Ku soo dhawaaw Luuqada Tusmo${NC}"
echo -e "${GRAY}==========================================${NC}"

