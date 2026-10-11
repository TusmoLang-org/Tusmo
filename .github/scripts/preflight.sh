#!/usr/bin/env bash
# preflight.sh - Fail fast when the repository is not in a buildable state.
#
# Runs before every build so that a missing source file produces a clear
# message instead of a cryptic PyInstaller or Python traceback half way
# through a release.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

errors=0
warnings=0

fail() { printf '  [FAIL] %s\n' "$1"; errors=$((errors + 1)); }
warn() { printf '  [WARN] %s\n' "$1"; warnings=$((warnings + 1)); }
ok()   { printf '  [ok]   %s\n' "$1"; }

echo "==> repository preflight"

# ------------------------------------------------------------- source files
# Every one of these is required for `python3 tusmo.py program.tus` to work.
required_paths=(
  tusmo.py
  tusmo_cli.py
  compiler
  compiler/processer.py
  compiler/frontend/lexer/lexer.py
  compiler/frontend/parser/parser.py
  compiler/midend/semanticanalyzer.py
  compiler/backend/transpiler/__init__.py
  stdlib
  stdlib/core.tus
  stdlib/tusmo_runtime.h
  stdlib/tusmo_types.h
  install.sh
  install.ps1
  Extension/package.json
  .github/scripts/build_bundle.sh
  .github/scripts/verify_install.sh
  .github/scripts/run_tests.py
)

missing=()
for p in "${required_paths[@]}"; do
  if [ ! -e "$p" ]; then
    missing+=("$p")
  fi
done
if [ ${#missing[@]} -eq 0 ]; then
  ok "all required source files are present"
else
  for p in "${missing[@]}"; do
    fail "missing: $p"
  done
fi

# ------------------------------------------------- files must reach a clone
# A file can exist locally and still be missing from every clone because
# .gitignore excludes it. That breaks GitHub Actions, so check git itself.
if git rev-parse --git-dir >/dev/null 2>&1; then
  ignored=()
  untracked=()
  for p in tusmo.py tusmo_cli.py install.sh install.ps1 .github/scripts/build_bundle.sh .github/scripts/verify_install.sh; do
    [ -e "$p" ] || continue
    if git check-ignore -q "$p"; then
      ignored+=("$p")
    elif ! git ls-files --error-unmatch "$p" >/dev/null 2>&1; then
      untracked+=("$p")
    fi
  done
  if [ ${#ignored[@]} -eq 0 ]; then
    ok "required files are not excluded by .gitignore"
  else
    for p in "${ignored[@]}"; do
      fail "$p is excluded by .gitignore - clones and CI will not have it"
    done
  fi
  if [ ${#untracked[@]} -eq 0 ]; then
    ok "required files are tracked by git"
  else
    for p in "${untracked[@]}"; do
      warn "$p is not tracked yet - remember to git add it before pushing"
    done
  fi
else
  warn "not a git checkout - skipping tracked-file checks"
fi

# ---------------------------------------------------- stale runtime/ refs
# runtime/ was removed from the language (everything lives in stdlib/ now).
# A regression here silently breaks all three release workflows.
stale_refs=$(grep -rn \
  -e 'runtime:' \
  -e 'cp -r runtime' \
  -e 'TUSMO_HOME/runtime' \
  -e '"runtime;' \
  -e '"runtime:' \
  .github/workflows install.sh install.ps1 2>/dev/null || true)
if [ -n "$stale_refs" ]; then
  printf '%s\n' "$stale_refs" | sed 's/^/  [FAIL] stale runtime\/ reference: /'
  errors=$((errors + $(printf '%s\n' "$stale_refs" | grep -c .)))
else
  ok "no stale runtime/ references"
fi

# -------------------------------------------------------- python dependencies
if python3 -c "import ply" >/dev/null 2>&1; then
  ok "python module: ply"
else
  fail "python module 'ply' is missing (python3 -m pip install ply)"
fi
if python3 -c "import requests" >/dev/null 2>&1; then
  ok "python module: requests"
else
  warn "python module 'requests' is missing (tusmo.py imports it at startup)"
fi

# --------------------------------------------------- compiler must import
if python3 -c "
import sys
sys.path.insert(0, '.')
import tusmo_cli  # noqa: F401
import compiler.processer  # noqa: F401
" >/dev/null 2>&1; then
  ok "compiler imports cleanly"
else
  fail "the compiler does not import - python3 -c 'import tusmo_cli' failed"
fi

# ------------------------------------------------------------ C compiler
if [ -n "${TUSMO_CC:-}" ]; then
  ok "TUSMO_CC is set: $TUSMO_CC"
elif command -v gcc >/dev/null 2>&1; then
  ok "system C compiler: $(command -v gcc)"
elif command -v clang >/dev/null 2>&1; then
  ok "system C compiler: $(command -v clang)"
else
  warn "no system C compiler found (release bundles ship their own toolchain)"
fi

echo "==> preflight: $errors error(s), $warnings warning(s)"
if [ "$errors" -ne 0 ]; then
  exit 1
fi
