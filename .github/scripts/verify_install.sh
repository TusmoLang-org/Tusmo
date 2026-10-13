#!/usr/bin/env bash
# verify_install.sh - End-to-end check that a Tusmo release tarball can be
# installed and used on a clean machine, exactly the way install.sh does it.
#
# Usage:  .github/scripts/verify_install.sh <tusmo-<triplet>.tar.gz>
#
# Runs entirely offline: no GitHub downloads, no VS Code step, no sudo, no
# shell-rc edits. Suitable for CI and for local testing of a release build.

set -euo pipefail

TARBALL="${1:-}"
if [ -z "$TARBALL" ]; then
  echo "usage: $0 <tusmo-<triplet>.tar.gz>" >&2
  exit 2
fi
if [ ! -f "$TARBALL" ]; then
  echo "verify_install: tarball not found: $TARBALL" >&2
  exit 2
fi

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

SANDBOX_HOME="$WORK/home"
SCRATCH="$WORK/project"
mkdir -p "$SANDBOX_HOME" "$SCRATCH"

TARBALL="$(cd "$(dirname "$TARBALL")" && pwd)/$(basename "$TARBALL")"

pass=0
fail=0
step() { printf '\n==> %s\n' "$1"; }
ok()   { printf '  [OK]   %s\n' "$1"; pass=$((pass+1)); }
bad()  { printf '  [FAIL] %s\n' "$1"; fail=$((fail+1)); }

# ---------------------------------------------------------------- install
step "installing $TARBALL into a sandbox HOME"
if HOME="$SANDBOX_HOME" \
   TUSMO_INSTALL_FROM="$TARBALL" \
   TUSMO_HOME="$SANDBOX_HOME/.tusmo" \
   TUSMO_NO_LINK=1 TUSMO_NO_RC=1 TUSMO_NO_VSCODE=1 \
   bash "$REPO_ROOT/install.sh" >"$WORK/install.log" 2>&1; then
  ok "install.sh exited 0"
else
  bad "install.sh exited non-zero"
  cat "$WORK/install.log"
fi

TUSMO_HOME_DIR="$SANDBOX_HOME/.tusmo"
TUSMO="$TUSMO_HOME_DIR/bin/tusmo"

if [ -x "$TUSMO" ]; then
  ok "bin/tusmo exists and is executable"
else
  bad "bin/tusmo missing or not executable"
  ls -la "$TUSMO_HOME_DIR" "$TUSMO_HOME_DIR/bin" 2>/dev/null || true
fi

# The launcher must set up the toolchain itself, with no env vars from us.
env -u TUSMO_CC -u TUSMO_INCLUDE_DIR -u TUSMO_LIB_DIR -u TUSMO_HOME "$TUSMO" --version >"$WORK/version.log" 2>&1 \
  && ok "tusmo --version works without any environment set" \
  || { bad "tusmo --version failed"; cat "$WORK/version.log"; }

if grep -q "Tusmo Version: 2\.0\.4-beta" "$WORK/version.log"; then
  ok "version string reported: $(grep -m1 'Tusmo Version' "$WORK/version.log")"
else
  bad "expected Tusmo Version: 2.0.4-beta"
  cat "$WORK/version.log"
fi

# The installer symlinks /usr/local/bin/tusmo -> ~/.tusmo/bin/tusmo, so the
# launcher has to resolve its own location through a symlink.
mkdir -p "$WORK/linkbin"
ln -sf "$TUSMO" "$WORK/linkbin/tusmo"
if env -u TUSMO_HOME -u TUSMO_CC "$WORK/linkbin/tusmo" --version >"$WORK/linked.log" 2>&1 \
   && grep -q "Tusmo Version" "$WORK/linked.log"; then
  ok "launcher works when invoked through a symlink"
else
  bad "launcher failed when invoked through a symlink"
  cat "$WORK/linked.log"
fi

# The bundled toolchain must actually be a working C compiler.
if [ -x "$TUSMO_HOME_DIR/toolchain/cc" ]; then
  if "$TUSMO_HOME_DIR/toolchain/cc" --version >"$WORK/cc.log" 2>&1; then
    ok "bundled toolchain works: $(head -1 "$WORK/cc.log")"
  else
    bad "bundled toolchain does not run"
    cat "$WORK/cc.log"
  fi
else
  bad "toolchain/cc missing from the bundle"
fi

# Test the native compiler/linker directly before involving Tusmo. This keeps
# a platform toolchain failure separate from a Tusmo code-generation failure.
step "compiling and running a native C toolchain smoke test"
cat > "$SCRATCH/toolchain-smoke.c" <<'C'
#include <stdio.h>
int main(void) {
    puts("Tusmo toolchain smoke test");
    return 0;
}
C
if (cd "$SCRATCH" && "$TUSMO_HOME_DIR/toolchain/cc" -O2 -o toolchain-smoke toolchain-smoke.c >"$WORK/toolchain-smoke.log" 2>&1); then
  if [ -x "$SCRATCH/toolchain-smoke" ] && [ "$("$SCRATCH/toolchain-smoke")" = "Tusmo toolchain smoke test" ]; then
    ok "bundled compiler and linker produced a runnable native binary"
  else
    bad "bundled compiler produced no runnable native binary"
    ls -la "$SCRATCH"
    cat "$WORK/toolchain-smoke.log" 2>/dev/null || true
  fi
else
  bad "bundled compiler/linker smoke test failed"
  cat "$WORK/toolchain-smoke.log" 2>/dev/null || true
fi

# Link Raylib without opening a window. This verifies that the release contains
# the native library and platform linker inputs required by Raylib programs.
step "linking a Raylib program"
cat > "$SCRATCH/raylib-smoke.c" <<'C'
#include "raylib/raylib.h"
int main(void) {
    InitWindow(1, 1, "Tusmo Raylib smoke test");
    CloseWindow();
    return 0;
}
C
raylib_flags=""
case "$(uname -s)" in
  Linux) raylib_flags="-lm -lGL -lX11 -lpthread -ldl -lrt" ;;
esac
if [ -f "$TUSMO_HOME_DIR/stdlib/raylib/libraylib.a" ] &&
   (cd "$SCRATCH" && "$TUSMO_HOME_DIR/toolchain/cc" -O2 \
      -I"$TUSMO_HOME_DIR/stdlib" -o raylib-smoke raylib-smoke.c \
      "$TUSMO_HOME_DIR/stdlib/raylib/libraylib.a" $raylib_flags \
      >"$WORK/raylib-smoke.log" 2>&1); then
  if [ -x "$SCRATCH/raylib-smoke" ]; then
    ok "platform Raylib library links successfully"
  else
    bad "Raylib linker produced no native binary"
    cat "$WORK/raylib-smoke.log" 2>/dev/null || true
  fi
else
  bad "platform Raylib library failed to link"
  cat "$WORK/raylib-smoke.log" 2>/dev/null || true
fi

# Exercise the real Tusmo metadata path from a project directory outside the
# installation. This catches regressions that a direct C link cannot detect.
step "compiling a Tusmo Raylib program from outside the installation"
cp "$REPO_ROOT/.github/scripts/raylib_link_smoke.tus" "$SCRATCH/raylib-link-smoke.tus"
if (cd "$SCRATCH" && env -u TUSMO_CC -u TUSMO_INCLUDE_DIR -u TUSMO_LIB_DIR -u TUSMO_HOME \
     "$TUSMO" raylib-link-smoke.tus >"$WORK/raylib-tusmo.log" 2>&1); then
  if [ -x "$SCRATCH/raylib-link-smoke" ]; then
    ok "Tusmo resolved and linked its installed Raylib library"
  else
    bad "Tusmo did not produce the Raylib smoke binary"
    cat "$WORK/raylib-tusmo.log"
  fi
else
  bad "Tusmo Raylib import/link smoke test failed"
  cat "$WORK/raylib-tusmo.log"
fi

# The VS Code extension needs the frozen language server next to the CLI.
if [ -x "$TUSMO_HOME_DIR/bin/tusmo-hover" ]; then
  ok "language server (bin/tusmo-hover) is installed"
else
  bad "bin/tusmo-hover missing from the bundle"
fi

# --------------------------------------------------- compile & run hello
step "compiling and running a program (outside the install dir)"
cat > "$SCRATCH/hello.tus" <<'TUS'
hawl main(): waxbo {
    qor("Salaan Tusmo!");
}
TUS

# Prove the *bundled* toolchain is used: shadow every system compiler with a
# script that fails. If compilation still succeeds, the machine needs no
# pre-installed C compiler.
FAKEBIN="$WORK/fakebin"
mkdir -p "$FAKEBIN"
for name in gcc cc clang x86_64-linux-gnu-gcc; do
  cat > "$FAKEBIN/$name" <<'FAKE'
#!/bin/sh
echo "system compiler was used - this should never happen" >&2
exit 1
FAKE
  chmod +x "$FAKEBIN/$name"
done

if (cd "$SCRATCH" && env -u TUSMO_CC -u TUSMO_INCLUDE_DIR -u TUSMO_LIB_DIR -u TUSMO_HOME \
     PATH="$FAKEBIN:$PATH" "$TUSMO" hello.tus >"$WORK/compile.log" 2>&1); then
  ok "tusmo hello.tus compiled with no usable system compiler (bundled toolchain)"
else
  bad "compilation failed"
  cat "$WORK/compile.log"
fi

if [ -x "$SCRATCH/hello" ]; then
  ok "native binary produced"
else
  bad "no binary next to the source"
  ls -la "$SCRATCH"
  echo "TUSMO_CC=${TUSMO_CC:-<unset>}"
  echo "TUSMO_HOME=${TUSMO_HOME:-<unset>}"
  echo "compiler output:"
  cat "$WORK/compile.log" 2>/dev/null || true
fi

out=""
if [ -x "$SCRATCH/hello" ] && out="$("$SCRATCH/hello" 2>&1)" && [ "$out" = "Salaan Tusmo!" ]; then
  ok "binary runs and prints: $out"
else
  out_display="$out"
  [ -n "$out_display" ] || out_display="<not produced>"
  bad "binary did not run or output mismatch: '$out_display'"
fi

# ------------------------------------- language features that pull in headers
step "compiling a program that uses stdlib + embedded types"
cat > "$SCRATCH/features.tus" <<'TUS'
hawl main(): waxbo {
    keyd:tix:tiro lambiyada = [1, 2, 3];
    keyd:eray magac = "Tusmo";
    keyd:qaamuus qof = {"magac": "Ali", "da": 25};
    qor("Lambiyada:", dherer(lambiyada));
    qor("Erayga:", dherer(magac));
    qor("Nooca:", nooc(magac));
    qor("Qof:", qof);
}
TUS

if (cd "$SCRATCH" && env -u TUSMO_CC -u TUSMO_INCLUDE_DIR -u TUSMO_LIB_DIR -u TUSMO_HOME \
     PATH="$FAKEBIN:$PATH" "$TUSMO" features.tus >"$WORK/features.log" 2>&1); then
  ok "arrays/dicts/strings compile"
else
  bad "array/dict program failed to compile"
  cat "$WORK/features.log"
fi

if [ -x "$SCRATCH/features" ]; then
  if out="$("$SCRATCH/features" 2>&1)"; then
    ok "feature program output: $(echo "$out" | tr '\n' ' ')"
  else
    bad "feature program crashed"
  fi
fi

# ------------------------------------------- broken programs must be rejected
step "rejecting a program with a semantic error"
cat > "$SCRATCH/broken.tus" <<'TUS'
hawl main(): waxbo {
    keyd:tiro x;
    qor(x);
}
TUS

rm -f "$SCRATCH/broken" "$SCRATCH/broken.c"
if (cd "$SCRATCH" && "$TUSMO" broken.tus >"$WORK/broken.log" 2>&1); then
  # tusmo may still exit 0 in some paths - the real contract is that no
  # binary is produced for a program that must not compile.
  if [ -x "$SCRATCH/broken" ]; then
    bad "a program with an uninitialized variable produced a binary"
  else
    ok "no binary produced for an invalid program"
  fi
else
  ok "invalid program rejected (non-zero exit)"
fi

# ------------------------------------- a failed install must not destroy it
step "a failed install leaves the previous install intact"
echo "keep-me" > "$TUSMO_HOME_DIR/previous-install.marker"
echo "this is not a tarball" > "$WORK/corrupt.tar.gz"
if HOME="$SANDBOX_HOME" \
   TUSMO_INSTALL_FROM="$WORK/corrupt.tar.gz" \
   TUSMO_HOME="$TUSMO_HOME_DIR" \
   TUSMO_NO_LINK=1 TUSMO_NO_RC=1 TUSMO_NO_VSCODE=1 \
   bash "$REPO_ROOT/install.sh" >"$WORK/corrupt.log" 2>&1; then
  bad "install.sh accepted a corrupt tarball"
else
  ok "install.sh failed on a corrupt tarball (non-zero exit)"
fi
if [ -f "$TUSMO_HOME_DIR/previous-install.marker" ]; then
  ok "previous installation survived the failed install"
else
  bad "previous installation was deleted by a failed install"
fi
if [ -x "$TUSMO" ]; then
  ok "tusmo still works after the failed install"
else
  bad "tusmo is broken after the failed install"
fi
rm -f "$TUSMO_HOME_DIR/previous-install.marker"

# --------------------------------------------------------------- summary
printf '\n==> verify_install: %d passed, %d failed\n' "$pass" "$fail"
if [ "$fail" -ne 0 ]; then
  exit 1
fi
