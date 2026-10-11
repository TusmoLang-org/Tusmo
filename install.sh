#!/usr/bin/env bash
# Tusmo installer (Linux / macOS)
#
# Environment overrides (all optional):
#   TUSMO_INSTALL_FROM=<file.tar.gz>  install from a local tarball (no network)
#   TUSMO_HOME=<dir>                  install location (default: ~/.tusmo)
#   TUSMO_NO_LINK=1                   do not touch /usr/local/bin or ~/.local/bin
#   TUSMO_NO_RC=1                     do not modify ~/.bashrc / ~/.zshrc
#   TUSMO_NO_VSCODE=1                 skip the VS Code extension step
set -euo pipefail

REPO="TusmoLang-org/Tusmo"
OS=$(uname -s)
ARCH=$(uname -m)

case "$OS/$ARCH" in
  Linux/x86_64)  ASSET="tusmo-linux-x86_64.tar.gz" ;;
  Darwin/arm64)  ASSET="tusmo-macos-arm64.tar.gz" ;;
  Darwin/x86_64)
    echo "Nidaamkan lama taageero (Intel macOS). Taageero: macOS ARM64." >&2
    exit 1
    ;;
  *)
    echo "Nidaamkan lama taageero: $OS $ARCH" >&2
    echo "Taageerada hadda: Linux x86_64, macOS ARM64, Windows x86_64." >&2
    exit 1
    ;;
esac

TUSMO_HOME="${TUSMO_HOME:-$HOME/.tusmo}"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# ------------------------------------------------- 1. fetch the release asset
if [ -n "${TUSMO_INSTALL_FROM:-}" ]; then
  echo "Waxaa la isticmaalayaa faylka deegaanka: $TUSMO_INSTALL_FROM"
  if [ ! -f "$TUSMO_INSTALL_FROM" ]; then
    echo "Khalad: faylka ma jiro: $TUSMO_INSTALL_FROM" >&2
    exit 1
  fi
  cp "$TUSMO_INSTALL_FROM" "$TMP/$ASSET"
else
  echo "Waxaa la soo dejinnaa $ASSET..."
  if ! curl -fsSL --retry 3 --retry-delay 2 \
      "https://github.com/$REPO/releases/latest/download/$ASSET" -o "$TMP/$ASSET"; then
    echo "Khalad: soo dejinta '$ASSET' way fashilantay." >&2
    echo "Hubi in internet-ka la hubo ama in nooca ugu dambeeya ee Tusmo uu jiro:" >&2
    echo "  https://github.com/$REPO/releases" >&2
    exit 1
  fi
fi

# ------------------------------------- 2. unpack, then swap in atomically
# The old install location is only removed after a successful download and
# extraction, so a failed download can never leave a broken install behind.
mkdir -p "$TMP/extract"
if ! tar -xzf "$TMP/$ASSET" -C "$TMP/extract"; then
  echo "Khalad: faylka tar-ka waa xumaaday: $ASSET" >&2
  exit 1
fi
if [ ! -e "$TMP/extract/bin/tusmo" ] && [ ! -e "$TMP/extract/bin/tusmo.exe" ]; then
  echo "Khalad: tarball-ku ma jiro bin/tusmo - qalabkan waa xumaaday." >&2
  exit 1
fi
mkdir -p "$(dirname "$TUSMO_HOME")"
rm -rf "$TUSMO_HOME"
mkdir -p "$TUSMO_HOME"
# `.` (not `*`) so dot-files inside the bundle survive; no glob surprises.
cp -R "$TMP/extract"/. "$TUSMO_HOME"/

chmod +x "$TUSMO_HOME/bin/tusmo" 2>/dev/null || true
chmod +x "$TUSMO_HOME/toolchain/cc" 2>/dev/null || true
chmod +x "$TUSMO_HOME/toolchain/zig/zig" 2>/dev/null || true
chmod +x "$TUSMO_HOME/bin/tusmo-hover" 2>/dev/null || true

# ------------------------------------------------- 3. VS Code extension
VSIX="tusmo-vscode.vsix"
EXT_IDS=("tusmolang-org.tusmo-language-support" "TusmoLang-org.tusmo-language-support" "tusmo-official.tusmo-language-support")

find_code() {
  for c in "$(command -v code 2>/dev/null || true)" "$(command -v codium 2>/dev/null || true)" /usr/bin/code /snap/bin/code /usr/share/code/bin/code; do
    if [ -n "$c" ] && [ -x "$c" ]; then
      echo "$c"
      return 0
    fi
  done
  return 1
}

if [ "${TUSMO_NO_VSCODE:-0}" != "1" ]; then
  if CODE_BIN=$(find_code); then
    echo "Waxaa la soo dejinnaa VS Code extension..."
    for eid in "${EXT_IDS[@]}"; do
      "$CODE_BIN" --uninstall-extension "$eid" >/dev/null 2>&1 || true
    done
    rm -rf "$HOME/.vscode/extensions"/tusmo*-language-support-* 2>/dev/null || true
    ok=0
    if curl -fsSL --retry 2 "https://github.com/$REPO/releases/latest/download/$VSIX" -o "$TMP/$VSIX"; then
      if "$CODE_BIN" --install-extension "$TMP/$VSIX" --force >/dev/null 2>&1; then
        ok=1
      fi
    fi
    if [ "$ok" -ne 1 ]; then
      echo "Ma suurtagelin in VSIX si toos ah loo rakibo; waxa la keydiyay si gacanta loogu rakibo."
      if curl -fsSL --retry 2 "https://github.com/$REPO/releases/latest/download/$VSIX" -o "$TUSMO_HOME/$VSIX"; then
        echo "   Ku rakib: code --install-extension $TUSMO_HOME/$VSIX --force"
      fi
    fi
  else
    rm -rf "$HOME/.vscode/extensions"/tusmo*-language-support-* 2>/dev/null || true
    if curl -fsSL --retry 2 "https://github.com/$REPO/releases/latest/download/$VSIX" -o "$TUSMO_HOME/$VSIX"; then
      echo "VSIX waa la soo dejiyey: $TUSMO_HOME/$VSIX"
      echo "   Ku rakib gacanta: code --install-extension $TUSMO_HOME/$VSIX --force"
    fi
  fi
fi

# ------------------------------------------------- 4. PATH + environment
# The launcher in bin/tusmo already exports TUSMO_CC / TUSMO_INCLUDE_DIR /
# TUSMO_LIB_DIR, so a plain PATH entry is enough for `tusmo` to work.
if [ "${TUSMO_NO_LINK:-0}" != "1" ]; then
  linked=0
  if [ "$(id -u)" -eq 0 ]; then
    ln -sf "$TUSMO_HOME/bin/tusmo" /usr/local/bin/tusmo && linked=1
  elif command -v sudo >/dev/null 2>&1; then
    # Interactive terminal: allow a password prompt. Non-interactive (CI,
    # curl | bash with no tty): only use cached credentials so we never hang.
    if [ -t 0 ] && [ -t 1 ]; then
      if sudo ln -sf "$TUSMO_HOME/bin/tusmo" /usr/local/bin/tusmo; then
        linked=1
      fi
    elif sudo -n true >/dev/null 2>&1; then
      if sudo -n ln -sf "$TUSMO_HOME/bin/tusmo" /usr/local/bin/tusmo; then
        linked=1
      fi
    fi
  fi
  if [ "$linked" -ne 1 ]; then
    mkdir -p "$HOME/.local/bin"
    ln -sf "$TUSMO_HOME/bin/tusmo" "$HOME/.local/bin/tusmo"
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
      echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
      echo "Waxaan PATH-ka ku daray \$HOME/.local/bin (fadlan fur terminal-ka mar kale)."
    fi
  fi
fi

cat > "$TUSMO_HOME/env.sh" <<'EOF'
# Tusmo environment - source this file (install.sh can add it to your shell rc).
export TUSMO_HOME="${TUSMO_HOME:-$HOME/.tusmo}"
if [ -x "$TUSMO_HOME/toolchain/cc" ]; then
  export TUSMO_CC="$TUSMO_HOME/toolchain/cc"
fi
if [ -d "$TUSMO_HOME/stdlib" ]; then
  export TUSMO_INCLUDE_DIR="$TUSMO_HOME/stdlib"
fi
if [ -d "$TUSMO_HOME/lib" ]; then
  export TUSMO_LIB_DIR="$TUSMO_HOME/lib"
fi
case ":$PATH:" in
  *":$TUSMO_HOME/bin:"*) ;;
  *) export PATH="$TUSMO_HOME/bin:$PATH" ;;
esac
EOF

# Make TUSMO_HOME visible to GUI apps / the VS Code extension without requiring
# the user to remember to source anything.
if [ "${TUSMO_NO_RC:-0}" != "1" ]; then
  marker="# Tusmo environment"
  for rc in "$HOME/.bashrc" "$HOME/.profile" "$HOME/.zshrc"; do
    if [ ! -f "$rc" ]; then
      # Only ever create the rc file of the shell family that already exists.
      case "$rc" in
        *.zshrc) [ -n "${ZSH_VERSION:-}" ] || continue ;;
        *) continue ;;
      esac
      touch "$rc"
    fi
    if ! grep -qF "$marker" "$rc" 2>/dev/null; then
      {
        printf '\n%s\n' "# Tusmo environment"
        printf 'export TUSMO_HOME="%s"\n' "$TUSMO_HOME"
        printf 'if [ -f "$TUSMO_HOME/env.sh" ]; then . "$TUSMO_HOME/env.sh"; fi\n'
      } >> "$rc"
    fi
  done
fi

# ------------------------------------------------- 5. sanity check
installed=0
if "$TUSMO_HOME/bin/tusmo" --version >/dev/null 2>&1; then
  installed=1
fi
if [ "$installed" -ne 1 ]; then
  echo "Digniin: 'tusmo --version' ma shaqeeyn; fadlan xakamee $TUSMO_HOME" >&2
fi

# ------------------------------------------------- 6. banner
if [ -t 1 ] && command -v clear >/dev/null 2>&1; then
  clear 2>/dev/null || true
fi

CYAN='\033[0;36m'
GREEN='\033[0;32m'
GRAY='\033[0;90m'
NC='\033[0m'

asciiArt="
  _______ _    _  _____ __  __  ____  

 |__   __| |  | |/ ____|  \/  |/ __ \ 
    | |  | |  | | (___ | \  / | |  | |
    | |  | |  | |\___ \| |\/| | |  | |
    | |  | |__| |____) | |  | | |__| |
    |_|   \____/|_____/|_|  |_|\____/ 
"

echo -e "${CYAN}${asciiArt}${NC}"
echo -e "${GRAY}==========================================${NC}"
echo -e "${GREEN}      Ku soo dhawaaw Luuqada Tusmo${NC}"
echo -e "${GRAY}==========================================${NC}"
echo -e "${GRAY}  Isku day: tusmo --version${NC}"
if [ "$installed" -eq 1 ]; then
  echo -e "${GREEN}  Rakibaad: OK${NC}"
else
  echo -e "${GRAY}  Rakibaad: aan la xaqiijin${NC}"
fi
echo -e "${GRAY}==========================================${NC}"
