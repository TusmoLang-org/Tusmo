---
title: Getting Started
description: Install Tusmo, write your first Somali program, and understand the Tusmo CLI workflow.
---

# Getting Started with Tusmo

This page helps you go from zero to running your first Tusmo program in a few minutes.

Tusmo is a **Somali programming language** that compiles to C and then to a native binary.

## 1. Install Tusmo

### Linux/macOS

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```

## 2. Verify Installation

```bash
tusmo --version
```

You should see a Tusmo version printed in the terminal.

## 3. Create Your First Program

Create `hello.tus`:

```tus
qor("Hello, Somali Developers!");
```

Run it:

```bash
tusmo hello.tus
./hello
```

Expected output:

```text
Hello, Somali Developers!
```

## 4. Understand the CLI

General format:

```bash
tusmo <file.tus> [options]
```

Common commands:

- `tusmo -h` / `tusmo --help`: Show help
- `tusmo -v` / `tusmo --version`: Show installed version
- `tusmo -l` / `tusmo --libraries`: List supported libraries
- `tusmo app.tus --c`: Keep generated C file
- `tusmo update`: Update Tusmo
- `tusmo dagso <library>`: Install a library package

## 5. Keep Generated C Code

To inspect what Tusmo generates:

```bash
tusmo hello.tus --c
```

This leaves `hello.c` in your working directory.

## 6. Example: Variables + Interpolation

```tus
keyd:eray magac = "Tusmo";
keyd:tiro version = 1;

qor($"Hello, {magac}!");
qor($"Version: {version}");
```

## 7. Recommended Editor Setup

Use VS Code for better productivity:

- Syntax highlighting
- Hover documentation
- Better readability for Tusmo files

## 8. What to Read Next

- [How Tusmo Works](how-it-works.md)
- [Variables](variables.md)
- [Functions](functions.md)
- [Classes](classes.md)
- [Standard Library](stdlib.md)
