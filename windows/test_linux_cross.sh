#!/usr/bin/env bash
set -Eeuo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sample="$project_root/test/test_main.tus"
binary="${sample%.tus}.exe"
wine_prefix="$(mktemp -d "${TMPDIR:-/tmp}/tusmo-wine.XXXXXX")"

cleanup() {
    rm -f "$binary" "${sample%.tus}.c"
    rm -rf "$wine_prefix"
}
trap cleanup EXIT

command -v x86_64-w64-mingw32-gcc >/dev/null || {
    echo 'Missing x86_64-w64-mingw32-gcc.' >&2
    exit 1
}
command -v wine >/dev/null || {
    echo 'Missing wine.' >&2
    exit 1
}

cd "$project_root"
export TUSMO_CC=x86_64-w64-mingw32-gcc

echo 'Cross-compiling Tusmo for Windows...'
python3 tusmo.py "$sample"

if [[ ! -f "$binary" ]]; then
    echo "Compiler did not produce $binary." >&2
    exit 1
fi

if [[ "${CROSS_COMPILE_ONLY:-0}" == '1' ]]; then
    echo 'Linux Windows cross-compilation passed.'
    exit 0
fi

echo 'Running the Windows executable under Wine...'
wine_log="$(mktemp "${TMPDIR:-/tmp}/tusmo-wine-log.XXXXXX")"
set +e
timeout --foreground --kill-after=5s "${WINE_TIMEOUT:-30}s" \
    env WINEPREFIX="$wine_prefix" WINEDEBUG=-all wine "$binary" >"$wine_log" 2>&1
status=$?
set -e
wineserver -k >/dev/null 2>&1 || true
output="$(<"$wine_log")"
rm -f "$wine_log"

if [[ $status -ne 0 ]]; then
    echo "$output"
    if [[ $status -eq 124 || $status -eq 137 ]]; then
        echo 'Wine execution timed out.' >&2
    fi
    exit "$status"
fi

echo "$output"
grep -F 'Aad iyo aad!' <<<"$output" >/dev/null || {
    echo 'Unexpected output from the Windows executable.' >&2
    exit 1
}

echo 'Linux Windows-cross-test passed.'
