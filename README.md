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
  <a href="https://github.com/TusmoLang-org/Tusmo/tree/main/docs">Documentation</a> ·
  <a href="https://github.com/TusmoLang-org/tusmo-examples">Examples</a>
</p>

---

## What is Tusmo?

Tusmo is a programming language project that makes Somali a first-class language for writing code. Its keywords and core syntax use Somali words, while its compiler translates programs into C before producing a native executable.

The project aims to make programming more approachable for Somali speakers without giving up the ability to build real software. The repository includes a compiler, a standard-library collection, and a Visual Studio Code language-support extension.

**The compilation pipeline:**

` .tus source → lexer and parser → AST and semantic checks → generated C → native executable `

Tusmo is actively evolving. Language features, tooling, and platform support may change between releases.

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
soco keyd:tiro i laga bilaabo 1 ilaa 5 {
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

## Installation

### Download a release

Visit the [GitHub Releases page](https://github.com/TusmoLang-org/Tusmo/releases) and choose an available package for your operating system. Follow the instructions included with that release.

Release assets and platform support can change. Check the release notes and available files rather than assuming every platform has a current package.

### Build or run from source

To explore the compiler itself, clone the repository:

```bash
git clone https://github.com/TusmoLang-org/Tusmo.git
cd Tusmo
```

The source compiler is Python-based and invokes a C compiler/toolchain to build generated C code. On Linux, a development environment commonly needs Python 3, Git, and a supported C toolchain such as GCC. Exact requirements may vary by branch and platform.

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
2. Keep changes focused and include a small example or test where appropriate.
3. Explain how you tested the change and which platform/toolchain you used.
4. Open an issue or pull request in this repository to discuss the change.

Please check the project's [community guide](docs/bulshada.md) before contributing.

## Project status

Tusmo is an evolving open-source language project. Features and tooling are under active development, and compatibility is not guaranteed across all versions. For the most accurate picture of what is currently available, consult the source code, documentation, and release notes.

## License

No repository-level license file is currently listed. Until a license is added, do not assume the source is licensed for unrestricted reuse, redistribution, or modification.

---

<p align="center">
  Built to bring programming closer to Somali speakers.
</p>
