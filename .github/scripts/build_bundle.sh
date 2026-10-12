#!/usr/bin/env bash
# build_bundle.sh - Assemble the Tusmo release bundle used by install.sh / install.ps1.
#
# This is the single source of truth for the on-disk layout of a release.
# The release-*.yml workflows and the local verification scripts all call it,
# so what CI tests is exactly what users download.
#
# Layout produced:
#   bundle/
#     bin/tusmo          POSIX launcher (Windows: bin/tusmo.cmd)
#     bin/tusmo-app      frozen PyInstaller app (Windows: tusmo-app.exe)
#     bin/tusmo-hover    frozen language server
#     stdlib/            copy of stdlib/ (headers + .tus modules + raylib assets)
#     toolchain/zig/     complete zig distribution (zig binary + lib/ + ...)
#     toolchain/cc       POSIX wrapper -> zig cc   (Windows: toolchain/cc.bat)
#     lib/               placeholder for TUSMO_LIB_DIR
#     env.sh             shell environment for users who prefer sourcing it
#
# Usage:
#   build_bundle.sh --dist <pyinstaller-dist-dir> --zig <zig-unpacked-dir> \
#                   --out <bundle-dir> --triplet <linux-x86_64|macos-arm64|windows-x86_64>
#
# Environment:
#   TUSMO_SKIP_ZIG=1   build the bundle without a bundled toolchain (falls back
#                      to the system compiler at runtime).

set -euo pipefail

DIST_DIR=""
ZIG_DIR=""
OUT_DIR=""
TRIPLET=""

while [ $# -gt 0 ]; do
  case "$1" in
    --dist)    DIST_DIR="$2"; shift 2 ;;
    --zig)     ZIG_DIR="$2"; shift 2 ;;
    --out)     OUT_DIR="$2"; shift 2 ;;
    --triplet) TRIPLET="$2"; shift 2 ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "build_bundle.sh: unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -n "$DIST_DIR" ] || { echo "build_bundle.sh: --dist is required" >&2; exit 2; }
[ -n "$OUT_DIR" ]  || { echo "build_bundle.sh: --out is required"  >&2; exit 2; }
[ -n "$TRIPLET" ]  || { echo "build_bundle.sh: --triplet is required" >&2; exit 2; }

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
[ -d "$REPO_ROOT/stdlib" ] || { echo "build_bundle.sh: stdlib/ not found in $REPO_ROOT" >&2; exit 1; }

case "$TRIPLET" in
  windows-*) IS_WINDOWS=1 ;;
  *)         IS_WINDOWS=0 ;;
esac

# ---------------------------------------------------------------- locate app
APP_SRC=""
# The language server is built as a separate one-file executable and lands
# next to the onedir app, i.e. dist/tusmo-hover beside dist/tusmo/.
HOVER_PARENT="$(dirname "$DIST_DIR")"
if [ "$IS_WINDOWS" = "1" ]; then
  HOVER_SRC="$HOVER_PARENT/tusmo-hover.exe"
  APP_DST="tusmo-app.exe"
  if [ -f "$DIST_DIR/tusmo.exe" ]; then
    APP_SRC="$DIST_DIR/tusmo.exe"
  fi
else
  HOVER_SRC="$HOVER_PARENT/tusmo-hover"
  APP_DST="tusmo-app"
  if [ -f "$DIST_DIR/tusmo" ]; then
    APP_SRC="$DIST_DIR/tusmo"
  fi
fi

if [ -z "$APP_SRC" ]; then
  echo "build_bundle.sh: frozen app not found in $DIST_DIR (expected tusmo or tusmo.exe)" >&2
  echo "build_bundle.sh: contents of $DIST_DIR:" >&2
  ls -la "$DIST_DIR" >&2 || true
  exit 1
fi

# ---------------------------------------------------------------- assemble
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR/bin" "$OUT_DIR/toolchain" "$OUT_DIR/lib" "$OUT_DIR/stdlib"

echo "==> copying frozen CLI"
if [ "$IS_WINDOWS" = "1" ]; then
  cp -r "$DIST_DIR"/. "$OUT_DIR/bin/"
  # Keep _internal/ next to the renamed executable: PyInstaller resolves it
  # relative to the executable, so a plain rename is safe.
  mv "$OUT_DIR/bin/tusmo.exe" "$OUT_DIR/bin/$APP_DST"
else
  cp -r "$DIST_DIR"/. "$OUT_DIR/bin/"
  mv "$OUT_DIR/bin/tusmo" "$OUT_DIR/bin/$APP_DST"
fi
chmod +x "$OUT_DIR/bin/$APP_DST" || true

echo "==> copying language server"
if [ -f "$HOVER_SRC" ]; then
  cp "$HOVER_SRC" "$OUT_DIR/bin/"
  chmod +x "$OUT_DIR/bin/$(basename "$HOVER_SRC")" 2>/dev/null || true
elif [ "${TUSMO_ALLOW_MISSING_HOVER:-0}" = "1" ]; then
  echo "build_bundle.sh: warning: $HOVER_SRC missing (TUSMO_ALLOW_MISSING_HOVER=1)" >&2
else
  echo "build_bundle.sh: the language server ($HOVER_SRC) is missing." >&2
  echo "build_bundle.sh: the VS Code extension will not work without it." >&2
  echo "build_bundle.sh: build it first, or set TUSMO_ALLOW_MISSING_HOVER=1 to ship without." >&2
  exit 1
fi

echo "==> copying stdlib"
cp -R "$REPO_ROOT/stdlib/." "$OUT_DIR/stdlib/"

# ------------------------------------------------------------- toolchain
if [ "${TUSMO_SKIP_ZIG:-0}" = "1" ]; then
  echo "==> TUSMO_SKIP_ZIG=1: no bundled toolchain (system compiler will be used)"
elif [ -n "$ZIG_DIR" ] && [ -d "$ZIG_DIR" ]; then
  echo "==> bundling zig toolchain from $ZIG_DIR"
  # The complete distribution is required: `zig cc` loads headers and compiler
  # resources from its sibling lib/ directory. Shipping only the binary breaks
  # every compile on a machine without a system toolchain.
  mkdir -p "$OUT_DIR/toolchain/zig"
  cp -R "$ZIG_DIR/." "$OUT_DIR/toolchain/zig/"
  ZIG_BIN="zig"
  [ -f "$OUT_DIR/toolchain/zig/zig.exe" ] && ZIG_BIN="zig.exe"
  [ -f "$OUT_DIR/toolchain/zig/$ZIG_BIN" ] || {
    echo "build_bundle.sh: zig binary ($ZIG_BIN) missing inside $ZIG_DIR" >&2
    ls -la "$ZIG_DIR" >&2
    exit 1
  }
  chmod +x "$OUT_DIR/toolchain/zig/$ZIG_BIN" || true
else
  echo "build_bundle.sh: warning: no zig directory given; bundle will rely on a system compiler" >&2
fi

# ------------------------------------------------------- toolchain wrapper
if [ "$IS_WINDOWS" = "1" ]; then
  cat > "$OUT_DIR/toolchain/cc.bat" <<'EOS'
@echo off
setlocal EnableExtensions EnableDelayedExpansion
set "TUSMO_ZIG=%~dp0zig\zig.exe"
if exist "%TUSMO_ZIG%" (
  rem Zig 0.11 does not support LTO with the Windows COFF object format.
  rem Tusmo passes -flto unconditionally, so remove that one flag here.
  set "TUSMO_ARGS=%*"
  set "TUSMO_ARGS=!TUSMO_ARGS:-flto=!"
  set "TUSMO_ARGS=!TUSMO_ARGS:-lGL=!"
  set "TUSMO_ARGS=!TUSMO_ARGS:-lX11=!"
  set "TUSMO_ARGS=!TUSMO_ARGS:-lpthread=!"
  set "TUSMO_ARGS=!TUSMO_ARGS:-ldl=!"
  set "TUSMO_ARGS=!TUSMO_ARGS:-lrt=!"
  set "TUSMO_ARGS=!TUSMO_ARGS:-lm=!"
  set "TUSMO_ARGS=!TUSMO_ARGS! -lopengl32 -lgdi32 -lwinmm -lshell32"
  "%TUSMO_ZIG%" cc !TUSMO_ARGS!
  exit /b !errorlevel!
)
where gcc >nul 2>nul && (gcc %* & exit /b !errorlevel!)
where clang >nul 2>nul && (clang %* & exit /b !errorlevel!)
echo Tusmo: ma jiro C compiler (zig/gcc/clang). Fadlan xakamee kaydka toolchain-ka. 1>&2
exit /b 1
EOS
else
  cat > "$OUT_DIR/toolchain/cc" <<'EOS'
#!/usr/bin/env bash
# Tusmo toolchain wrapper: bundled zig cc, with a system-compiler fallback.
here="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if [ -x "$here/zig/zig" ]; then
  args=()
  needs_raylib=0
  for arg in "$@"; do
    # Zig 0.11 does not support LTO with the Mach-O object format.
    # Tusmo passes -flto unconditionally, so remove that one flag on macOS.
    if [ "$(uname -s)" = "Darwin" ] && [ "$arg" = "-flto" ]; then
      continue
    fi
    case "$arg" in
      *libraylib.a) needs_raylib=1 ;;
    esac
    if [ "$(uname -s)" = "Darwin" ] && case "$arg" in -lGL|-lX11|-lpthread|-ldl|-lrt) true ;; *) false ;; esac; then
      continue
    fi
    args+=("$arg")
  done
  if [ "$(uname -s)" = "Darwin" ] && [ "$needs_raylib" -eq 1 ]; then
    args+=("-framework" "Cocoa" "-framework" "IOKit" "-framework" "OpenGL" "-framework" "CoreVideo" "-lobjc")
  fi
  exec "$here/zig/zig" cc "${args[@]}"
fi
for candidate in gcc clang cc; do
  if command -v "$candidate" >/dev/null 2>&1; then
    exec "$candidate" "$@"
  fi
done
echo "Tusmo: ma jiro C compiler (zig/gcc/clang)." >&2
exit 1
EOS
  chmod +x "$OUT_DIR/toolchain/cc"
fi

# --------------------------------------------------------------- launcher
if [ "$IS_WINDOWS" = "1" ]; then
  cat > "$OUT_DIR/bin/tusmo.cmd" <<'EOS'
@echo off
setlocal
rem Derive TUSMO_HOME from this script's own location so the launcher works
rem before any environment variable has been configured.
if not defined TUSMO_HOME for %%I in ("%~dp0..") do set "TUSMO_HOME=%%~fI"
if exist "%TUSMO_HOME%\toolchain\cc.bat" set "TUSMO_CC=%TUSMO_HOME%\toolchain\cc.bat"
if exist "%TUSMO_HOME%\stdlib" set "TUSMO_INCLUDE_DIR=%TUSMO_HOME%\stdlib"
if exist "%TUSMO_HOME%\lib" set "TUSMO_LIB_DIR=%TUSMO_HOME%\lib"
"%~dp0tusmo-app.exe" %*
exit /b %errorlevel%
EOS
else
  cat > "$OUT_DIR/bin/tusmo" <<'EOS'
#!/usr/bin/env bash
# Tusmo launcher. Works when invoked directly or through a symlink
# (e.g. /usr/local/bin/tusmo -> ~/.tusmo/bin/tusmo).
set -euo pipefail

self="$0"
# Resolve one level of symlinks (readlink -f is not available on macOS).
i=0
while [ -L "$self" ] && [ "$i" -lt 16 ]; do
  link="$(readlink "$self")"
  case "$link" in
    /*) self="$link" ;;
    *)  self="$(dirname "$self")/$link" ;;
  esac
  i=$((i + 1))
done

bin_dir="$(CDPATH= cd -- "$(dirname -- "$self")" && pwd)"
home_dir="$(dirname "$bin_dir")"

[ -n "${TUSMO_HOME:-}" ] || export TUSMO_HOME="$home_dir"
if [ -x "$TUSMO_HOME/toolchain/cc" ]; then
  export TUSMO_CC="$TUSMO_HOME/toolchain/cc"
fi
if [ -d "$TUSMO_HOME/stdlib" ]; then
  export TUSMO_INCLUDE_DIR="$TUSMO_HOME/stdlib"
fi
if [ -d "$TUSMO_HOME/lib" ]; then
  export TUSMO_LIB_DIR="$TUSMO_HOME/lib"
fi
exec "$bin_dir/tusmo-app" "$@"
EOS
  chmod +x "$OUT_DIR/bin/tusmo"
fi

# ----------------------------------------------------------------- env.sh
cat > "$OUT_DIR/env.sh" <<'EOS'
# Tusmo environment. Add to ~/.bashrc or ~/.zshrc, or let install.sh do it.
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
EOS

# ------------------------------------------------------------- tarball
TARBALL="$REPO_ROOT/tusmo-$TRIPLET.tar.gz"
echo "==> creating $TARBALL"
rm -f "$TARBALL"
tar -czf "$TARBALL" -C "$OUT_DIR" .

echo "==> bundle contents:"
if command -v du >/dev/null 2>&1; then du -sh "$OUT_DIR" "$TARBALL"; fi
ls -la "$OUT_DIR"
