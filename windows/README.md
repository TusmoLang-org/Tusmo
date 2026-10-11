# Windows tests

This directory contains the Windows smoke test used by CI.

The test verifies that:

- Python can load the Tusmo compiler;
- the compiler CLI starts on Windows;
- the language-server test suite passes;
- a `.tus` program compiles with GCC and produces a working `.exe`.

Run locally from PowerShell after installing Python, the Python dependencies,
and the MSYS2 MinGW GCC toolchain:

```powershell
python -m pip install ply requests
.\windows\test_windows.ps1
```

On Linux, the Windows target can be cross-compiled with MinGW-w64 and executed
with Wine, without using a virtual machine:

```bash
sudo apt install gcc-mingw-w64-x86-64 wine
./windows/test_linux_cross.sh
```

The Wine run has a 30-second timeout. Override it with `WINE_TIMEOUT=60` if
Wine needs longer to initialize on a new machine.

To only verify Windows executable generation, without starting Wine:

```bash
CROSS_COMPILE_ONLY=1 ./windows/test_linux_cross.sh
```
