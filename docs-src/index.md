# Tusmo Documentation

Welcome to Tusmo, a Somali programming language!

## What is Tusmo?

Tusmo is a statically-typed programming language that compiles to C, then to a binary using Zig. It uses Somali keywords and syntax, making it accessible to Somali developers.

## Quick Start

```bash
# Install Tusmo
curl -fsSL https://raw.githubusercontent.com/Tusmolang/Tusmo/main/install.sh | bash

# Run a Tusmo program
tusmo hello.tus
```

## How It Works

```
hello.tus  →  tusmo (parser)  →  hello.c  →  zig cc  →  hello (binary)  →  ./hello
```

Tusmo compiles `.tus` files to C code, then uses Zig (bundled) to compile to an executable.

The bundled release includes everything needed - no external dependencies required.

## Language Features

- **Static Typing** - Variables have explicit types
- **Somali Keywords** - Native Somali syntax (`keyd`, `haddii`, `soco`, etc.)
- **Object-Oriented** - Classes and inheritance
- **Garbage Collection** - Uses Boehm GC (bundled)
- **Built-in Standard Library** - File I/O, HTTP, sockets, time, random

## Documentation Sections

**Getting Started:**
- [Getting Started](getting-started) - Installation and first program
- [How It Works](how-it-works) - Internal architecture and compiler pipeline

**Language Reference:**
- [Variables](variables) - Data types and declarations
- [Strings](strings) - String operations
- [Arrays](arrays) - Array and 2D arrays
- [Dictionaries](dictionaries) - Key-value pairs
- [Conditions](conditions) - If/else statements
- [Loops](loops) - While, for, foreach
- [Functions](functions) - Function definitions
- [Classes](classes) - Object-oriented programming
- [Operators](operators) - Arithmetic and comparisons

**Standard Library:**
- [Standard Library](stdlib) - Overview
- [OS Module](stdlib-os) - File system and system operations
- [Wakhti Module](stdlib-wakhti) - Time and date functions
- [Nasiib Module](stdlib-nasiib) - Random number generation
- [Xiriiriye Module](stdlib-xiriiriye) - TCP socket programming
- [WebXiriiriye Module](stdlib-webxiriiriye) - WebSocket support
- [HTTP Module](stdlib-http) - HTTP server and requests
