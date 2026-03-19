# Tusmo

A Somali programming language that compiles to C.

## What is Tusmo?

Tusmo is a statically-typed programming language that uses Somali keywords and syntax. It compiles to C code, then to a binary using Zig (bundled).

## Quick Start

### Linux/macOS

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/Tusmolang/Tusmo/main/install.sh | bash

# Run
tusmo hello.tus
```

### Windows

```powershell
# Install (run in PowerShell as Administrator)
irm https://raw.githubusercontent.com/Tusmolang/Tusmo/main/install.ps1 | iex

# Run
tusmo hello.tus
```

```tus
// hello.tus
qor("Hello, Somaliland!");
```

## Features

- **Somali Syntax** - Native Somali keywords (`keyd`, `haddii`, `soco`, `koox`)
- **Static Typing** - Variables have explicit types
- **Object-Oriented** - Classes with inheritance
- **Garbage Collection** - Automatic memory management
- **Standard Library** - File I/O, HTTP, sockets, time, random

## Language Example

```tus
// Variables
keyd:eray magac = "Tusmo";
keyd:tiro da = 5;

// Conditionals
haddii (da > 3) {
    qor("Waa weyn!");
}

// Loops
soco i laga bilaabo 0 .. 5 {
    qor(i);
}

// Functions
hawl greet(name: eray) : waxbo {
    qor("Soo dhawow " + name);
}

// Classes
koox Qof {
    keyd:eray name;
    
    dhis(n: eray) : waxbo {
        kan.name = n;
    }
}

keyd:Qof p1 = Qof("Ali") cusub;
```

## Documentation

For full documentation, visit: **[Tusmo Docs](https://tusmolang.github.io/Tusmo/)**

### Getting Started
- [Installation](https://tusmolang.github.io/Tusmo/getting-started)
- [How It Works](https://tusmolang.github.io/Tusmo/how-it-works)

### Language Reference
- [Variables](https://tusmolang.github.io/Tusmo/variables)
- [Strings](https://tusmolang.github.io/Tusmo/strings)
- [Arrays](https://tusmolang.github.io/Tusmo/arrays)
- [Dictionaries](https://tusmolang.github.io/Tusmo/dictionaries)
- [Conditions](https://tusmolang.github.io/Tusmo/conditions)
- [Loops](https://tusmolang.github.io/Tusmo/loops)
- [Functions](https://tusmolang.github.io/Tusmo/functions)
- [Classes](https://tusmolang.github.io/Tusmo/classes)
- [Operators](https://tusmolang.github.io/Tusmo/operators)

### Standard Library
- [Stdlib Overview](https://tusmolang.github.io/Tusmo/stdlib)
- [OS Module](https://tusmolang.github.io/Tusmo/stdlib-os)
- [Wakhti (Time)](https://tusmolang.github.io/Tusmo/stdlib-wakhti)
- [Nasiib (Random)](https://tusmolang.github.io/Tusmo/stdlib-nasiib)
- [Xiriiriye (Sockets)](https://tusmolang.github.io/Tusmo/stdlib-xiriiriye)
- [WebXiriiriye (WebSocket)](https://tusmolang.github.io/Tusmo/stdlib-webxiriiriye)
- [HTTP](https://tusmolang.github.io/Tusmo/stdlib-http)

## Requirements

None! The bundled release includes:
- Zig compiler
- Boehm GC
- Runtime libraries

Just download and run.

## License

MIT

---

Made with ❤️ for the Somali developer community.
