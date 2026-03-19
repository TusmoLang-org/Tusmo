# Getting Started

## Installation

### Linux/macOS

```bash
curl -fsSL https://raw.githubusercontent.com/Tusmolang/Tusmo/main/install.sh | bash
```

### Windows

```powershell
irm https://raw.githubusercontent.com/Tusmolang/Tusmo/main/install.ps1 | iex
```

## Your First Program

Create `hello.tus`:

```tus
qor("Hello, Somaliland!");
```

## Running Tusmo

Simply pass the `.tus` file to the tusmo command:

```bash
tusmo hello.tus
```

## Usage

```
tusmo <file.tus> [options]

Options:
  --c           Keep the generated C code file
  -h, --help    Show help
  -v, --version Show version
  -l, --libraries List supported libraries
  update        Update Tusmo to latest version
  install <lib> Install a library
```

## How It Works

```
hello.tus  →  tusmo (parser)  →  hello.c  →  zig cc  →  hello (binary)  →  ./hello
              ↓
         AST → semantic analysis → C code generation
              ↓
         runtime/*.c + stdlib/*.tus → linked
```

### Compilation Pipeline

1. **Lexing** - Tokenize Tusmo source code
2. **Parsing** - Build AST (Abstract Syntax Tree)
3. **Semantic Analysis** - Type checking, symbol resolution
4. **Code Generation** - Generate C code from AST
5. **Compilation** - Zig compiles C to binary executable
6. **Execution** - Run the binary

The bundled release includes:
- **Zig compiler** - Compiles C to binary
- **Boehm GC** - Garbage collector (prebuilt)
- **Runtime library** - String, array, dictionary support
- **Standard library** - OS, HTTP, sockets, etc.

You do NOT need to install GCC or libgc manually.

### Keep C Code

Use `--c` flag to keep the generated C file:

```bash
tusmo hello.tus --c
```

This produces `hello.c` in the same directory.

## Code Example

```tus
// My first Tusmo program
keyd:eray magac = "Tusmo";
keyd:tiro da = 5;

qor($"Hello, {magac}!");
qor($"Age: {da}");
```

Output:
```
Hello, Tusmo!
Age: 5
```

## Requirements

None! The bundled release includes everything needed:
- Zig compiler
- Boehm GC
- Runtime libraries

Just download and run.
