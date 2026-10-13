# Tusmo

<p align="center">
  <img src="Extension/icons/tusmoLogo.svg" alt="Tusmo logo" width="180" />
</p>

<h3 align="center">Barnaamij ku qor Af-Soomaali. Dhis wax dhab ah.</h3>

<p align="center">
  <strong>Tusmo</strong> is a statically typed, general-purpose programming language designed around Somali keywords.
  It compiles <code>.tus</code> source files to C and then builds native executables using a C toolchain.
</p>

<p align="center">
  <a href="https://github.com/TusmoLang-org/Tusmo">Source code</a> ·
  <a href="https://github.com/TusmoLang-org/Tusmo/releases">Releases</a> ·
  <a href="https://tusmolang-org.github.io/Tusmo/">Documentation</a> ·
  <a href="https://github.com/TusmoLang-org/tusmo-examples">Examples</a>
</p>

<p align="center"><strong>[English](README.md) · [Af-Soomaali](README-so.md)</strong></p>

---

## What is Tusmo?

Tusmo is a programming language project that makes Somali a first-class language for writing code. Its keywords and core syntax use Somali words, while its compiler translates programs into C before producing a native executable.

The project aims to make programming more approachable for Somali speakers without giving up the ability to build real software. The repository includes a compiler, a standard-library collection, and a Visual Studio Code language-support extension.

**The compilation pipeline:**

` .tus source → lexer and parser → AST and semantic checks → generated C → native executable `

Tusmo is actively evolving. Language features, tooling, and platform support may change between releases.

> Tusmo is currently beta software. Linux source builds and Windows cross-compilation are testable; native Windows runtime testing is performed by the Windows GitHub Actions runner.

## Why Tusmo?

- **Somali-first syntax** — write program logic using Somali keywords such as `haddii`, `hawl`, and `soo_celi`.
- **Static typing** — declare data types and catch many mistakes during compilation.
- **Native compilation** — generate C code and use a C toolchain to build an executable.
- **Familiar programming building blocks** — functions, variables, conditions, loops, arrays, and more.
- **Standard-library modules** — the repository includes modules for common tasks such as strings, time, math, operating-system operations, and networking.
- **Developer tooling** — a VS Code extension provides Tusmo language support.

## Your first Tusmo program

Create a file named `hello.tus`:

```tusmo
hawl main() : waxbo {
    qor("Haye adduun!");
}

main();
```

Compile and run it with an installed Tusmo CLI:

```bash
tusmo hello.tus
```

For a source checkout, the repository also documents running the compiler through Python:

```bash
python3 tusmo.py hello.tus
```

Expected output:

```text
Haye adduun!
```

Tusmo also supports top-level scripting, so a small program can be written without defining `main`:

```tusmo
qor("Salaan, dunida!");
```

## A quick language tour

### Variables and types

Use `keyd` to declare a variable. A type follows the colon.

```tusmo
keyd:tiro da_da = 25;
keyd:eray magac = "Ayaan";
keyd:miyaa waa_diyaar = run;

qor(magac, " waa ", da_da, " jir.");
```

Common built-in types include:

| Tusmo type | Meaning |
| --- | --- |
| `tiro` | Integer |
| `jajab` | Floating-point number |
| `eray` | String |
| `miyaa` | Boolean (`run` or `been`) |
| `xaraf` | Character |

### Conditions

```tusmo
keyd:tiro dhibco = 85;

haddii (dhibco >= 90) {
    qor("A");
} ama_haddii (dhibco >= 80) {
    qor("B");
} haddii_kale {
    qor("Sii wad dadaalka.");
}
```

### Loops

```tusmo
soco i laga bilaabo 1..5 {
    qor("Tirada: ", i);
}
```

### Functions

```tusmo
hawl isku_dar(a: tiro, b: tiro) : tiro {
    soo_celi a + b;
}

hawl main() : waxbo {
    keyd:tiro natiijo = isku_dar(10, 20);
    qor("Wadarta: ", natiijo);
}

main();
```

> These examples introduce the syntax; consult the language documentation for the full grammar and current feature details.

## Platform support

| Platform | Support |
| --- | --- |
| Linux x86_64 | Source compiler and release installer |
| Windows x86_64 | Release installer and native CI tests |
| macOS ARM64 | Release installer |
| Linux → Windows | MinGW-w64 cross-compilation; Wine is optional |

Windows source builds require GCC/MinGW or the toolchain bundled with a release. Native Windows tests run on a `windows-latest` GitHub Actions runner.

## Installation

### One-line installer

Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

macOS (Apple Silicon / ARM64):

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

Windows PowerShell:

```powershell
iwr -useb https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```

Open a new terminal and verify the installation:

```bash
tusmo --version
```

The release installer provides the Tusmo CLI, runtime files, standard library, and the toolchain required by the release bundle.

### Download a release

Visit the [GitHub Releases page](https://github.com/TusmoLang-org/Tusmo/releases) to download a precompiled package directly. Current asset names are `tusmo-linux-x86_64.tar.gz`, `tusmo-macos-arm64.tar.gz`, and `tusmo-windows-x86_64.tar.gz`. The one-line installers above download and install the matching package automatically.

The [online documentation](https://tusmolang-org.github.io/Tusmo/) is deployed automatically from the `main` branch. Release packages are built by GitHub Actions when a version tag such as `v2.0.1` is pushed.

Release assets and platform support can change. Check the release notes and available files rather than assuming every platform has a current package.

### Build or run from source

To explore the compiler itself, clone the repository:

```bash
git clone https://github.com/TusmoLang-org/Tusmo.git
cd Tusmo
```

Linux developer setup:

```bash
sudo apt install python3 python3-pip gcc
python3 -m pip install ply requests
```

The source compiler is Python-based and invokes a C compiler/toolchain to build generated C code. For Windows source development, install Python and the MSYS2 MinGW toolchain, then run `python -m pip install ply requests`. Alternatively, use the Windows release bundle, which includes its compiler toolchain.

Try a program from the repository after reviewing the [Getting Started guide](docs/bilaabista.md).

## Compiler options

The CLI includes help and version commands, and can preserve generated C code for inspection.

```bash
tusmo --help
tusmo --version
tusmo hello.tus --c
```

- `--help` — show available commands and options.
- `--version` — show the installed compiler version.
- `--c` — keep the generated C source instead of removing it after compilation.

Compiling `main.tus` creates `main.exe` on Windows (and `main` on Unix-like systems). The generated `main.c` is removed after a successful compile unless `--c` is supplied.

The CLI also includes commands for discovering and managing supported libraries. Run `tusmo --help` for the options available in your installed version.

## Standard library and ecosystem

The repository's `stdlib/` directory contains Tusmo modules and runtime support. Depending on the module and platform, these include:

- **Core utilities** for common operations and type conversion.
- **Strings, arrays, and dictionaries** for working with data.
- **Math and time** utilities.
- **Operating-system and file operations.**
- **HTTP, TCP sockets, and WebSockets** for networking.
- **Raylib-related files** for graphics and game-development experiments or integrations.

Module availability and maturity differ. Check the module source and documentation before relying on a particular API in a production application.

### VS Code support

The `Extension/` directory contains Tusmo's VS Code language-support extension, including syntax highlighting and language configuration. See the [extension README](Extension/README.md) for its setup instructions.

To package it locally:

```bash
cd Extension
npm install
npx --yes @vscode/vsce package
```

Then select **Install from VSIX** in VS Code and choose the generated `.vsix` file. The extension provides `.tus` syntax highlighting, Tusmo file icons, hover documentation, and — when the language server is available — completion, diagnostics, go-to-definition, and document symbols.

## Testing

### Language test suite

```bash
python3 .github/scripts/run_tests.py
```

Every program in `test/` is compiled and checked against the baseline in `.github/scripts/test_baseline.json` (expected passes, expected compile errors, and known failures).

### Language-server tests

```bash
python3 Extension/server/test_server.py -v
```

These tests cover completion, definitions, diagnostics, document symbols, AST coordinates, and import caching.

### Native Windows tests

The GitHub Actions Windows workflow checks:

- Tusmo CLI startup;
- language-server tests;
- GCC compilation;
- `.exe` generation;
- execution and output of a Tusmo program.

Workflow: `.github/workflows/windows-test.yml`

### Windows cross-compilation from Linux

You do not need VMware to verify that Tusmo can produce a Windows executable from Linux. Install MinGW-w64 and Wine:

```bash
sudo apt install gcc-mingw-w64-x86-64 wine
./windows/test_linux_cross.sh
```

To verify only Windows executable generation without starting Wine:

```bash
CROSS_COMPILE_ONLY=1 ./windows/test_linux_cross.sh
```

## Repository structure

```text
compiler/                 Lexer, parser, semantic analyzer, transpiler
stdlib/                   Tusmo standard library and C runtime support
stdlib/raylib/            Raylib bindings and examples
stdlib/opencv/            OpenCV bridge
Extension/                VS Code extension and language server
test/                     Tusmo compiler/runtime test programs
windows/                  Windows smoke test and Linux cross-test
doc/                      Language reference
docs/                     Getting-started and project documentation
.github/workflows/        Release and CI workflows
.github/scripts/          Preflight, test runner, and release helpers
tusmo.py                  Compiler CLI entry point
```

## Documentation

The documentation is primarily written in Somali and covers the language from first steps through more advanced features.

- [Introduction](docs/index.md)
- [Getting started and installation](docs/bilaabista.md)
- [Language basics](docs/aasaaska.md)
- [Advanced language features](docs/heerka_sare.md)
- [Standard library](docs/maktabada.md)
- [Tools and development environment](docs/agabka.md)
- [Community and contributing](docs/bulshada.md)

For runnable examples, see the [Tusmo examples repository](https://github.com/TusmoLang-org/tusmo-examples).

## Contributing

Contributions, bug reports, documentation improvements, and example programs are welcome.

1. Explore the code and documentation before changing behavior.
2. Add or update tests when implementing a feature or bug fix.
3. Keep changes focused and include a small example or test where appropriate.
4. Explain how you tested the change and which platform/toolchain you used.
5. Do not commit generated files or local binaries.
6. Open an issue or pull request in this repository to discuss the change.

Please check the project's [community guide](docs/bulshada.md) before contributing.

## Project status

Tusmo is an evolving open-source language project. Features and tooling are under active development, and compatibility is not guaranteed across all versions. Known limitations:

- Native Windows execution should be verified on Windows CI or a Windows machine; Wine is only a compatibility check.
- Raylib and OpenCV APIs may depend on platform-specific toolchains and libraries.
- Some documentation and newer language features may change during beta development.

For the most accurate picture of what is currently available, consult the source code, documentation, and release notes.

## License

No repository-level license file is currently listed. Until a license is added, do not assume the source is licensed for unrestricted reuse, redistribution, or modification.

---

<p align="center">
  Built to bring programming closer to Somali speakers.
</p>
