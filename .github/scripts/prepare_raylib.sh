#!/usr/bin/env bash
# Install the native Raylib library matching the release platform.

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

VERSION="6.0"
case "$TRIPLET" in
  linux-x86_64)
    ASSET="raylib-6.0_linux_amd64.tar.gz"
    SHA256="b64ba618a19e7da9e9c0e09bb398ecfd477a77d2d7231901bafc8739d27c08d2"
    ;;
  macos-arm64)
    ASSET="raylib-6.0_macos.tar.gz"
    SHA256="6ae5947fbd36aee4c280e3a2b3e1893316c433e292bda6e94e0f2b037498ad70"
    ;;
  windows-x86_64)
    ASSET="raylib-6.0_win64_mingw-w64.zip"
    SHA256="69688e025812c8132634c609c30938eda4a3fa14d63c4031108873a4d797e2d3"
    ;;
  *)
    echo "prepare_raylib: unsupported triplet: $TRIPLET" >&2
    exit 2
    ;;
esac

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
ARCHIVE="$WORK/$ASSET"
URL="https://github.com/raysan5/raylib/releases/download/$VERSION/$ASSET"

curl --fail --silent --show-error --location --retry 5 --retry-delay 3 \
  "$URL" -o "$ARCHIVE"

python - "$ARCHIVE" "$WORK/raylib.a" <<'PY'
import hashlib
import pathlib
import sys
import tarfile
import zipfile

archive = pathlib.Path(sys.argv[1])
output = pathlib.Path(sys.argv[2])

if archive.suffix == ".zip":
    with zipfile.ZipFile(archive) as package:
        member = next(name for name in package.namelist() if name.endswith("/lib/libraylib.a"))
        output.write_bytes(package.read(member))
else:
    with tarfile.open(archive) as package:
        member = next(info for info in package.getmembers() if info.name.endswith("/lib/libraylib.a"))
        stream = package.extractfile(member)
        if stream is None:
            raise SystemExit("Raylib archive member could not be read")
        output.write_bytes(stream.read())

print(f"extracted {output} ({output.stat().st_size} bytes)")
PY

ACTUAL="$(python - "$ARCHIVE" <<'PY'
import hashlib
import pathlib
import sys
print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
PY
)"
if [ "$ACTUAL" != "$SHA256" ]; then
  echo "prepare_raylib: SHA-256 mismatch for $ASSET" >&2
  echo "expected: $SHA256" >&2
  echo "actual:   $ACTUAL" >&2
  exit 1
fi

DEST="$BUNDLE/stdlib/raylib/libraylib.a"
mkdir -p "$(dirname "$DEST")"
NATIVE_LIBRARY="$WORK/raylib.a"
if [ "$TRIPLET" = "macos-arm64" ]; then
  if ! command -v lipo >/dev/null 2>&1; then
    echo "prepare_raylib: lipo is required to select the macOS arm64 archive slice" >&2
    exit 1
  fi
  lipo "$WORK/raylib.a" -thin arm64 -output "$WORK/raylib-arm64.a"
  # Repack the thin archive so Zig 0.11 does not have to consume the
  # universal archive's platform-specific symbol-table format.
  mkdir "$WORK/raylib-objects"
  (
    cd "$WORK/raylib-objects"
    ar -x "$WORK/raylib-arm64.a"
  )
  libtool -static -o "$WORK/raylib-arm64-repacked.a" "$WORK"/raylib-objects/*.o
  NATIVE_LIBRARY="$WORK/raylib-arm64-repacked.a"
fi
cp "$NATIVE_LIBRARY" "$DEST"
echo "installed Raylib $VERSION for $TRIPLET at $DEST"
file "$DEST" 2>/dev/null || true
