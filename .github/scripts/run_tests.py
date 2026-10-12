#!/usr/bin/env python3
"""Tusmo language test runner.

Compiles every test program in test/ and checks the outcome against a
checked-in baseline (.github/scripts/test_baseline.json).

Expectations used in the baseline:

  pass            compiles into a native binary and the binary exits 0
  compile-error   must NOT produce a binary (negative / diagnostics tests)
  run-error       compiles, but the program is expected to exit non-zero
  known-fail      currently broken: still executed, a failure is tolerated
                  (reported as xfail) and a success is reported as xpass so
                  the baseline can be refreshed when the language catches up
  skip            not run at all, with a human readable "reason"
                  (GUI, network server, interactive input, missing module, ...)

Note: `tusmo.py` currently exits 0 even when the C backend fails, therefore
this runner never trusts the exit code alone - the produced binary is the
contract.

Usage:
  python3 .github/scripts/run_tests.py                 # full run against baseline
  python3 .github/scripts/run_tests.py --suite core    # only CI-blocking tests
  python3 .github/scripts/run_tests.py --only arrays   # substring filter
  python3 .github/scripts/run_tests.py --update-baseline
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEST_DIR = REPO_ROOT / "test"
BASELINE_PATH = Path(__file__).resolve().parent / "test_baseline.json"

COMPILE_TIMEOUT = 60
RUN_TIMEOUT = 15

# Files a test may need at runtime (fixtures). Binaries and generated .c files
# that live in test/ are deliberately not copied.
DATA_SUFFIXES = {
    ".tus",
    ".txt",
    ".json",
    ".csv",
    ".dat",
    ".md",
    ".html",
    ".htm",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".wav",
    ".mp3",
    ".py",
}

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_baseline() -> dict:
    if not BASELINE_PATH.exists():
        return {"tests": {}}
    with BASELINE_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def discover_tests() -> list[str]:
    """Only the top level of test/, so nested fixtures are not compiled twice."""
    if not TEST_DIR.is_dir():
        return []
    return sorted(p.name for p in TEST_DIR.glob("*.tus"))


def prepare_workspace(workdir: Path) -> None:
    """Mirror the source fixtures of test/ into a throwaway directory.

    Compiling inside test/ would litter the repository with binaries and .c
    files; compiling elsewhere keeps `keen "stdlib/..."` imports working
    because the compiler is always invoked with cwd=REPO_ROOT.
    """
    if not TEST_DIR.is_dir():
        return
    for path in TEST_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in DATA_SUFFIXES:
            continue
        target = workdir / path.relative_to(TEST_DIR)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def compile_test(src: Path, workdir: Path, timeout: int) -> tuple[bool, Path, str]:
    """Compile *src* (already inside *workdir*) using the real CLI.

    The compiler is run with cwd=REPO_ROOT so that `keen "stdlib/..."` and
    `keen "opengl/..."` style imports resolve the same way they do for users
    running from the repository root.
    """
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tusmo.py"), str(src)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        timeout=timeout,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    binary = src.with_suffix("")
    if sys.platform == "win32" and not binary.exists():
        exe = Path(str(binary) + ".exe")
        if exe.exists():
            binary = exe
    return binary.exists(), binary, output


def run_binary(binary: Path, timeout: int) -> tuple[int | None, str]:
    try:
        proc = subprocess.run(
            [str(binary)],
            cwd=str(binary.parent),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return None, "<timeout>"
    except OSError as exc:
        return None, f"<cannot execute: {exc}>"


def classify(name: str, entry: dict, workdir: Path) -> tuple[str, str]:
    """Return (status, detail) where status is ok|mismatch|error."""
    expect = entry.get("expect", "pass")
    src = workdir / name
    if not src.exists():
        return "error", f"{name} is not present in the test workspace"

    if expect == "skip":
        return "skip", entry.get("reason", "")

    try:
        produced, binary, compile_out = compile_test(src, workdir, COMPILE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "mismatch", f"compile timed out after {COMPILE_TIMEOUT}s"
    except OSError as exc:
        return "error", f"runner failure: {exc}"

    if expect == "compile-error":
        if produced:
            binary.unlink(missing_ok=True)
            return "mismatch", "expected a compile error but a binary was produced"
        return "ok", "rejected as expected"

    if not produced:
        head = next(
            (ln for ln in compile_out.splitlines() if ln.strip()),
            "<no diagnostics>",
        )
        detail = f"no binary produced: {head.strip()[:160]}"
        # Keep expected-pass failures actionable in CI. Known-fail tests retain
        # the compact one-line output so the suite stays readable.
        if entry.get("expect", "pass") == "pass" and compile_out.strip():
            detail += "\n" + compile_out.strip()[-4000:]
        return "mismatch", detail

    if entry.get("run", True) is False:
        return "ok", "compiled (run disabled in baseline)"

    code, run_out = run_binary(binary, RUN_TIMEOUT)
    if code is None:
        return "mismatch", f"run failed: {run_out.strip()[:160]}"
    if expect == "run-error":
        if code == 0:
            return "mismatch", "expected a non-zero exit code"
        return "ok", f"exited {code} as expected"
    if code != 0:
        tail = run_out.strip().splitlines()[-1] if run_out.strip() else ""
        return "mismatch", f"exit code {code}: {tail[:160]}"
    return "ok", "compiled and ran"


def infer_expectation(status: str, detail: str, entry: dict) -> dict:
    """Turn an observed result into a baseline entry (used by --update-baseline)."""
    if status == "ok":
        if "rejected as expected" in detail:
            return {"expect": "compile-error"}
        if "exited" in detail and "as expected" in detail:
            return {"expect": "run-error"}
        if "compiled (run disabled" in detail:
            return {"expect": "pass", "run": False}
        return {"expect": "pass"}
    if status in ("mismatch", "error"):
        if "no binary produced" in detail:
            return {"expect": "known-fail", "reason": detail.replace("\n", " ")[:200]}
        if detail.startswith("run failed"):
            # hung / needs a display / waits for network - do not run in CI
            return {"expect": "skip", "reason": detail.replace("\n", " ")[:200]}
        if detail.startswith("exit code"):
            return {"expect": "known-fail", "reason": detail.replace("\n", " ")[:200]}
        return {
            "expect": "known-fail",
            "reason": detail.replace("\n", " ")[:200],
        }
    return entry


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the Tusmo language tests.")
    ap.add_argument("--only", metavar="SUBSTRING", help="run tests whose name contains SUBSTRING")
    ap.add_argument(
        "--suite",
        choices=["core", "all"],
        default="all",
        help="core = everything except skipped tests (CI gate)",
    )
    ap.add_argument("--list", action="store_true", help="list tests and their baseline expectation")
    ap.add_argument("--update-baseline", action="store_true", help="rewrite the baseline from this run")
    args = ap.parse_args()

    baseline = load_baseline()
    tests: dict = baseline.setdefault("tests", {})
    names = discover_tests()

    unknown = [n for n in names if n not in tests]
    if unknown and not args.update_baseline:
        print(
            "Note: these tests are not in the baseline yet (they are treated as "
            "'pass'). Re-run with --update-baseline and review the results:\n  "
            + "\n  ".join(unknown),
            file=sys.stderr,
        )

    if args.list:
        for n in names:
            e = tests.get(n, {})
            print(f"{n:40s} {e.get('expect', '?'):15s} {e.get('reason', '')}")
        return 0

    if args.only:
        names = [n for n in names if args.only in n]

    MARKS = {
        "ok": "  ok  ",
        "skip": " skip ",
        "xfail": " xfail",
        "xpass": " XPASS",
        "mismatch": " FAIL ",
        "error": " ERR ",
    }

    results = []
    work_root = Path(tempfile.mkdtemp(prefix="tusmo-tests-"))
    prepare_workspace(work_root)
    started = time.time()
    try:
        for name in names:
            entry = tests.get(name, {"expect": "pass"})
            is_new = name not in tests
            if args.suite == "core" and entry.get("expect") == "skip":
                continue
            t0 = time.time()
            status, detail = classify(name, entry, work_root)
            elapsed = time.time() - t0
            if entry.get("expect") == "known-fail":
                if status == "ok":
                    status = "xpass"
                    detail = "now passes - refresh the baseline (--update-baseline)"
                elif status in ("mismatch", "error"):
                    status = "xfail"
            if args.update_baseline and is_new:
                tests[name] = infer_expectation(status, detail, entry)
            results.append((name, status, detail, tests.get(name, {}).get("expect", "pass"), elapsed))
            print(f"[{MARKS[status]}] {name:38s} {detail}", flush=True)
    finally:
        shutil.rmtree(work_root, ignore_errors=True)

    passed = sum(1 for r in results if r[1] == "ok")
    skipped = sum(1 for r in results if r[1] == "skip")
    xfails = sum(1 for r in results if r[1] == "xfail")
    xpasses = [r for r in results if r[1] == "xpass"]
    mismatches = [r for r in results if r[1] == "mismatch"]
    errors = [r for r in results if r[1] == "error"]

    print()
    print(
        f"total={len(results)} passed={passed} skipped={skipped} "
        f"known-fail={xfails} now-passing={len(xpasses)} "
        f"failed={len(mismatches)} errors={len(errors)} "
        f"time={time.time() - started:.1f}s"
    )

    if args.update_baseline:
        baseline["generated_by"] = ".github/scripts/run_tests.py"
        with BASELINE_PATH.open("w", encoding="utf-8") as fh:
            json.dump(baseline, fh, indent=2, ensure_ascii=False, sort_keys=True)
            fh.write("\n")
        print(f"baseline written to {BASELINE_PATH}")

    if xpasses:
        print("\nThese tests now pass and should be promoted to 'pass' in the baseline:")
        for name, _, detail, _, _ in xpasses:
            print(f"  {name}: {detail}")

    if mismatches or errors:
        print("\nUnexpected results:")
        for name, status, detail, expect, _ in mismatches + errors:
            print(f"  {name}: expected {expect}, got {status} - {detail}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
