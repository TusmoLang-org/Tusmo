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
ZIG="$ZIG.exe"
[ -x "$ZIG" ] || { echo "prepare_raylib: bundled Zig not found: $ZIG" >&2; exit 1; }
echo "building Raylib $RAYLIB_VERSION for $TRIPLET with bundled Zig"
NATIVE_LIBRARY="$BUILD/libraylib.a"

# Compile the native Win32 backend directly to absolute output paths. On this
# runner, Make/MinGW changes the effective working directory for compiler jobs,
# which leaves the objects outside Raylib's source tree and breaks its archive
# recipe. Explicit input and output paths avoid that ambiguity.
AR_BIN="$(command -v ar)"
RAYLIB_OBJECTS=()
for module in rcore rshapes rtextures rtext rmodels raudio; do
  object="$BUILD/$module.o"
  echo "compiling Raylib $module.c"
  "$ZIG" cc -c "$SRC/$module.c" -o "$object" \
    -fno-stack-protector \
    -Wall -D_GNU_SOURCE \
    -DPLATFORM_DESKTOP_WIN32 -DGRAPHICS_API_OPENGL_33 \
    -Wno-missing-braces -Werror=pointer-arith -fno-strict-aliasing \
    -std=c99 -DUNICODE -D_WIN32_WINNT=0x0A00 -I"$SRC"
  [ -f "$object" ] || {
    echo "prepare_raylib: compiler did not create $object" >&2
    exit 1
  }
  RAYLIB_OBJECTS+=("$object")
done
"$AR_BIN" rcs "$NATIVE_LIBRARY" "${RAYLIB_OBJECTS[@]}"
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
