---
title: How Tusmo Works
description: Internal architecture of the Tusmo language compiler, from lexer to C code generation.
---

# How Tusmo Works

Tusmo language follows a classic compiler pipeline:

`Tusmo source (.tus) -> Lexer -> Parser -> AST -> Semantic Analysis -> C Code -> Native Binary`

## High-Level Architecture

```text
source.tus
   -> lexer (tokens)
   -> parser (AST)
   -> semantic checker (types + symbols)
   -> transpiler (C code)
   -> C compiler (binary)
   -> run
```

Tusmo is designed this way to keep the language readable in Somali while still producing fast executables.

## Stage 1: Lexing

The lexer reads source text and converts it into tokens.

Examples of Tusmo keywords:

- `keyd`
- `haddii`
- `soco`
- `keen`
- `isticmaal`

File: `compiler/frontend/lexer/lexer.py`

## Stage 2: Parsing

The parser converts tokens into AST nodes.

Examples of AST nodes include:

- variable declarations
- function declarations
- class declarations
- import nodes (`keen`, `isticmaal`)

Files:

- `compiler/frontend/parser/grammar_rules.py`
- `compiler/frontend/parser/ast_nodes.py`

## Stage 3: Import Resolution

Tusmo resolves imports before full semantic analysis.

### `keen`

`keen "module";`

- imports full module AST
- good for broad module usage

### `isticmaal`

`isticmaal {name, helper} kujira "module";`

- imports only selected top-level symbols
- helps reduce unused declarations in resulting AST
- gives tighter control for larger codebases

File: `compiler/processer.py`

## Stage 4: Semantic Analysis

The semantic checker validates code meaning:

- unknown identifiers
- type mismatches
- invalid function calls
- invalid class/member usage

File: `compiler/midend/semanticanalyzer.py`

## Stage 5: C Code Generation

The transpiler maps AST nodes into C.

- Tusmo functions -> C functions
- Tusmo classes -> C structs + methods
- Tusmo runtime calls -> C runtime APIs

Files:

- `compiler/backend/transpiler/c_code_generator.py`
- `compiler/backend/transpiler/*_generator.py`

## Stage 6: Runtime Linking and Build

Generated C is built together with runtime sources under `runtime/`.

Runtime provides:

- strings
- arrays
- dictionaries
- OS operations
- HTTP/sockets/websocket
- math/time/random helpers

Entry flow file: `tusmo.py`

## Why This Architecture Matters

For developers:

- readable Somali syntax
- strong compile-time checks
- predictable runtime performance

For teams and leadership:

- easier onboarding for Somali-speaking engineers
- production-friendly path via native binaries
- clear separation between language features and runtime implementation

## Summary

Tusmo is not an interpreter-only experiment. It is a real compiler pipeline with semantic validation and native output, making it a serious option for learning, tooling, and practical software in the Somali language ecosystem.
