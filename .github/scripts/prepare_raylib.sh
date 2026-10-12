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
BUNDLE_ABS="$(cd "$BUNDLE" && pwd)"
case "$TRIPLET" in
  linux-x86_64|macos-arm64|windows-x86_64) ;;
  *) echo "prepare_raylib: unsupported triplet: $TRIPLET" >&2; exit 2 ;;
esac

RAYLIB_VERSION="6.0"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

if [ "$TRIPLET" = "linux-x86_64" ]; then
  # The official Linux archive already matches the Linux runner ABI and was
  # the previously passing path. Keep it isolated from the native rebuilds
  # required by Windows and macOS.
  ASSET="raylib-6.0_linux_amd64.tar.gz"
  ASSET_SHA256="b64ba618a19e7da9e9c0e09bb398ecfd477a77d2d7231901bafc8739d27c08d2"
  ARCHIVE="$WORK/$ASSET"
  curl --fail --silent --show-error --location --retry 5 --retry-delay 3 \
    "https://github.com/raysan5/raylib/releases/download/$RAYLIB_VERSION/$ASSET" \
    -o "$ARCHIVE"
  ACTUAL="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
  [ "$ACTUAL" = "$ASSET_SHA256" ] || {
    echo "prepare_raylib: Linux Raylib SHA-256 mismatch" >&2
    exit 1
  }
  DEST="$BUNDLE/stdlib/raylib/libraylib.a"
  mkdir -p "$(dirname "$DEST")"
  tar -xOzf "$ARCHIVE" "raylib-6.0_linux_amd64/lib/libraylib.a" > "$DEST"
  echo "installed native Raylib $RAYLIB_VERSION at $DEST"
  file "$DEST" 2>/dev/null || true
  exit 0
fi

if [ "$TRIPLET" = "macos-arm64" ]; then
  ASSET="raylib-6.0_macos.tar.gz"
  ASSET_SHA256="6ae5947fbd36aee4c280e3a2b3e1893316c433e292bda6e94e0f2b037498ad70"
  ARCHIVE="$WORK/$ASSET"
  curl --fail --silent --show-error --location --retry 5 --retry-delay 3 \
    "https://github.com/raysan5/raylib/releases/download/$RAYLIB_VERSION/$ASSET" \
    -o "$ARCHIVE"
  ACTUAL="$(shasum -a 256 "$ARCHIVE" | awk '{print $1}')"
  [ "$ACTUAL" = "$ASSET_SHA256" ] || {
    echo "prepare_raylib: macOS Raylib SHA-256 mismatch" >&2
    exit 1
  }
  tar -xOzf "$ARCHIVE" "raylib-6.0_macos/lib/libraylib.a" > "$WORK/raylib-universal.a"
  lipo "$WORK/raylib-universal.a" -thin arm64 -output "$WORK/raylib-arm64.a"
  mkdir "$WORK/raylib-objects"
  (cd "$WORK/raylib-objects" && ar -x "$WORK/raylib-arm64.a")
  DEST="$BUNDLE_ABS/stdlib/raylib/libraylib.a"
  mkdir -p "$(dirname "$DEST")"
  libtool -static -o "$DEST" "$WORK"/raylib-objects/*.o
  echo "installed native Raylib $RAYLIB_VERSION at $DEST"
  file "$DEST" 2>/dev/null || true
  exit 0
fi

SOURCE_DIR="$WORK/raylib"
echo "checking out Raylib tag $RAYLIB_VERSION"
git clone --depth 1 --branch "$RAYLIB_VERSION" --single-branch \
  https://github.com/raysan5/raylib.git "$SOURCE_DIR"
SRC="$SOURCE_DIR/src"
BUILD="$WORK/raylib-build"
mkdir -p "$BUILD"

ZIG="$BUNDLE_ABS/toolchain/zig/zig"
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
BUILD_CC="$ZIG cc"
BUILD_AR="$ZIG ar"
if [ "$TRIPLET" = "macos-arm64" ] && command -v clang >/dev/null 2>&1; then
  # Raylib's GLFW backend is Objective-C on macOS. Apple Clang is the native
  # compiler for that source; the arm64 objects remain compatible with the
  # bundled Zig linker used when Tusmo programs are compiled.
  BUILD_CC="$(command -v clang)"
  BUILD_AR="$(command -v ar)"
fi
PLATFORM_ARGS=()
if [ "$TRIPLET" = "windows-x86_64" ]; then
  # Use Raylib's native Win32 backend. It avoids importing a prebuilt GLFW
  # object archive and is linkable with the bundled Zig GNU target.
  PLATFORM_ARGS+=("PLATFORM=PLATFORM_DESKTOP_WIN32")
fi
"$MAKE_BIN" -C "$SRC" \
  CC="$BUILD_CC" \
  AR="$BUILD_AR" \
  RAYLIB_RELEASE_PATH="$BUILD" \
  RAYLIB_LIBTYPE=STATIC \
  RAYLIB_BUILD_MODE=RELEASE \
  RAYLIB_MODULE_AUDIO=TRUE \
  RAYLIB_MODULE_MODELS=TRUE \
  "${PLATFORM_ARGS[@]}" \
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
