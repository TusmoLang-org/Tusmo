#!/usr/bin/env bash
# Build Raylib with the same native Zig toolchain shipped by Tusmo.

set -euo pipefail

BUNDLE=""
TRIPLET=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --bundle)  BUNDLE="$2"; shift 2 ;;
    --triplet) TRIPLET="$2"; shift 2 ;;
    *) echo "usage: $0 --bundle <dir> --triplet <triplet>" >&2; exit 2 ;;
  esac
done

[ -n "$BUNDLE" ] || { echo "prepare_raylib: --bundle is required" >&2; exit 2; }
[ -n "$TRIPLET" ] || { echo "prepare_raylib: --triplet is required" >&2; exit 2; }
case "$TRIPLET" in
  linux-x86_64|macos-arm64|windows-x86_64) ;;
  *) echo "prepare_raylib: unsupported triplet: $TRIPLET" >&2; exit 2 ;;
esac

RAYLIB_VERSION="6.0"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
SOURCE_DIR="$WORK/raylib"
echo "checking out Raylib tag $RAYLIB_VERSION"
git clone --depth 1 --branch "$RAYLIB_VERSION" --single-branch \
  https://github.com/raysan5/raylib.git "$SOURCE_DIR"
SRC="$SOURCE_DIR/src"
BUILD="$WORK/raylib-build"
mkdir -p "$BUILD"

ZIG="$BUNDLE/toolchain/zig/zig"
if [ "$TRIPLET" = "windows-x86_64" ]; then ZIG="$ZIG.exe"; fi
[ -x "$ZIG" ] || { echo "prepare_raylib: bundled Zig not found: $ZIG" >&2; exit 1; }
MAKE_BIN="make"
if ! command -v "$MAKE_BIN" >/dev/null 2>&1 && command -v mingw32-make >/dev/null 2>&1; then
  MAKE_BIN="mingw32-make"
fi
command -v "$MAKE_BIN" >/dev/null 2>&1 || {
  echo "prepare_raylib: make or mingw32-make is required to build Raylib" >&2
  exit 1
}

echo "building Raylib $RAYLIB_VERSION for $TRIPLET with bundled Zig"
"$MAKE_BIN" -C "$SRC" \
  CC="$ZIG cc" \
  AR="$ZIG ar" \
  RAYLIB_RELEASE_PATH="$BUILD" \
  RAYLIB_LIBTYPE=STATIC \
  RAYLIB_BUILD_MODE=RELEASE \
  RAYLIB_MODULE_AUDIO=TRUE \
  RAYLIB_MODULE_MODELS=TRUE \
  clean all

NATIVE_LIBRARY="$BUILD/libraylib.a"
[ -f "$NATIVE_LIBRARY" ] || {
  echo "prepare_raylib: Raylib build did not produce $NATIVE_LIBRARY" >&2
  exit 1
}

if [ "$TRIPLET" = "windows-x86_64" ]; then
  # Tusmo metadata ends in .a and Windows normalizes it to .lib.
  DEST="$BUNDLE/stdlib/raylib/libraylib.a.lib"
else
  DEST="$BUNDLE/stdlib/raylib/libraylib.a"
fi
mkdir -p "$(dirname "$DEST")"
cp "$NATIVE_LIBRARY" "$DEST"
echo "installed native Raylib $RAYLIB_VERSION at $DEST"
file "$DEST" 2>/dev/null || true
