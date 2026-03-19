# How Tusmo Works

This document explains the internal workings of the Tusmo compiler.

## Architecture Overview

```
source.tus  →  Lexer  →  Parser  →  AST  →  Semantic  →  Transpiler  →  C Code
                                     ↓                                         ↓
                               Symbol Table                              zig cc
                                                                              ↓
                                                                        binary
```

## Compilation Pipeline

### 1. Lexing (Tokenization)

The lexer converts Tusmo source code into tokens:

```python
# compiler/frontend/lexer/lexer.py
keywords = {
    'haddii': 'HADDII',
    'keen': 'KEEN',
    'tiro': 'TIRO',
    'eray': 'ERAY',
    '___c__call_': 'C_CALL',
    # ... more keywords
}
```

### 2. Parsing (AST Generation)

The parser builds an Abstract Syntax Tree (AST) from tokens:

```
Program
  └── VariableDeclaration (keyd:tiro x = 5)
        ├── name: "x"
        ├── type: "tiro"
        └── value: 5 (IntegerLiteral)
```

### 3. Semantic Analysis

Type checking and symbol resolution:

- Variable names are registered in the symbol table
- Type checking ensures type safety
- Function calls are validated

### 4. Code Generation (Transpilation)

The transpiler converts AST to C code:

```c
// Generated C code from keyd:tiro x = 5;
int x;
x = 5;
```

## Key Concepts

### The `keen` Keyword (Import)

The `keen` keyword imports modules. The compiler resolves the path:

```tus
keen "os";
```

Resolution order:
1. Current directory
2. `.lib/` directory
3. `lib/` directory
4. `stdlib/` directory (built-in)

The imported module's AST is merged with the main program's AST.

### The `___c__call_` Function

This is a special builtin that calls C functions directly from Tusmo code:

```tus
// In stdlib/os.tus
hawl halkee() : eray {
    soo_celi ___c__call_("tusmo_os_cwd");
}
```

**How it works:**
1. Parser creates a `CCallNode` with the C function name
2. Transpiler generates: `tusmo_os_cwd()`
3. The C function must exist in the runtime

**Why use it?**
- Call C runtime functions (file I/O, sockets, time)
- Access system-level functionality
- Performance-critical operations

### The `___c__code_` Function

Embed raw C code directly:

```tus
___c_code_("#include <math.h>");
```

This copies the C code directly into the generated output.

### Runtime Linking

Tusmo automatically detects which runtime features are needed:

```python
# compiler/backend/transpiler/expression_generator.py

def _generate_ccall(self, node):
    c_function_name = node.c_function_name
    
    if "tusmo_os" in c_function_name:
        self.main_generator.used_features.add("os")
    elif "tusmo_time" in c_function_name:
        self.main_generator.used_features.add("wakhti")
    elif "tusmo_socket" in c_function_name:
        self.main_generator.used_features.add("socket")
```

The runtime includes:
- `runtime/string.c` - String operations
- `runtime/array.c` - Array operations
- `runtime/dictionary.c` - Dictionary operations
- `runtime/os.c` - OS functions
- `runtime/time.c` - Time functions
- `runtime/socket.c` - Socket functions
- `runtime/http.c` - HTTP server

## Generated C Code Structure

```c
#include "tusmo_runtime.h"

int main(void) {
    GC_INIT();
    
    // Your code here
    
    return 0;
}
```

The runtime header provides:
- GC_INIT() - Initialize garbage collector
- TusmoString - String type
- TusmoTixTiro - Integer array type
- TusmoQaamuus - Dictionary type
- Helper functions

## Class Implementation

Classes are implemented as C structs with function pointers:

```c
// Generated for koox Qof { keyd:eray name; }
typedef struct Qof {
    char* name;
    // ... more fields
} Qof;

// Method
void Qof_setName(Qof* kan, char* name) {
    kan->name = name;
}
```

## Memory Management

Tusmo uses the Boehm garbage collector:

```c
#include <gc.h>

int main(void) {
    GC_INIT();
    // All allocations are automatic
}
```

No manual `malloc`/`free` needed!

## Custom C Functions

You can add your own C functions to the runtime:

1. Add function to a `.c` file in `runtime/`
2. Declare in `runtime/tusmo_runtime.h`
3. Call from Tusmo with `___c__call_("your_function")`

Example:

```c
// runtime/myext.c
int tusmo_my_add(int a, int b) {
    return a + b;
}
```

```c
// runtime/tusmo_runtime.h
extern int tusmo_my_add(int a, int b);
```

```tus
// In your .tus file
keyd:tiro result = ___c__call_("tusmo_my_add", 3, 4);
```

## Build Process

When you run `tusmo hello.tus`:

1. Parse `hello.tus` + all imports
2. Build AST
3. Type check
4. Generate `hello.c`
5. Compile: `zig cc hello.c runtime/*.c -lgc -o hello`
6. Execute `./hello`

The bundled release includes everything needed - no external dependencies.
