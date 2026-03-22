# Sida Tusmo u Shaqeyso

Dukumiintigan wuxuu sharaxayaa shaqada gudaha ee compiler-ka Tusmo.

## Dulmarka Qaab-dhismeedka (Architecture Overview)

```
source.tus  →  Lexer  →  Parser  →  AST  →  Semantic  →  Transpiler  →  Code-ka C
                                     ↓                                         ↓
                               Symbol Table                              zig cc
                                                                              ↓
                                                                        binary-ga
```

## Pipeline-ka Turjumidda (Compilation Pipeline)

### 1. Lexing (Tokenization)

Lexer-ku wuxuu u beddelaa code-ka Tusmo tokens:

```python
# compiler/frontend/lexer/lexer.py
keywords = {
    'haddii': 'HADDII',
    'keen': 'KEEN',
    'tiro': 'TIRO',
    'eray': 'ERAY',
    '___c__call_': 'C_CALL',
    # ... keyword-yo badan
}
```

### 2. Parsing (AST Generation)

Parser-ku wuxuu ka dhisaa Abstract Syntax Tree (AST) tokens-ka:

```
Program
  └── VariableDeclaration (keyd:tiro x = 5)
        ├── magac: "x"
        ├── nooca: "tiro"
        └── qiimaha: 5 (IntegerLiteral)
```

### 3. Semantic Analysis


- Diiwaangelinta: Magacyada variable-da waxaa lagu keydiyaa Jadwalka Astaamaha (Symbol Table).

- Badbaadada Nooca (Type Safety):
Waxay hubisaa in hawlgalada (operations) ay is-waafaqsan yihiin.
Tusaale: Ma ogolaanayso in tiro lagu daro eray (5 + "Tusmo"), waayo taasi waxay jebinaysaa badbaadada nooca.

- Ansixinta Hawlaha : Marka function loogu yeero (call), waxay hubisaa:
In function-kaas uu jiro.
In tirada xogta la siiyay (arguments) ay la mid tahay intii uu u baahnaa (parameters).
In noocyada xogta (types) ay sax yihiin.


### 4. Code Generation (Transpilation)

Transpiler-ku wuxuu u beddelaa AST-ka → C code:

```c
// Code-ka C ee laga sameeyay keyd:tiro x = 5;
int x;
x = 5;
```

## Fikradaha Muhiimka ah

### Keyword-ka `keen` (Import)

Keyword-ka `keen` wuxuu soo import-kareyaa modules-ka. Compiler-ku wuxuu raadiyaa in uu soo helo module-ka la soo import-kareeyay:

```tus
keen "os";
```

Nidaamka sida uu u raadin doono:
1. Directory-ga hadda la joogo
2. Directory-ga `.lib/` 
3. Directory-ga `stdlib/` (ee ku dhex dhisan)

AST-ga module-ka la soo import-kareeyay waxaa lagu darayaa ama lagu biirinayaa main AST-ga.

### Hawsha `___c__call_`

Tani waa mid gaar ah oo ku dhex dhisan oo si toos ah uga wacda hawlaha(Functions-ka) C code-ka Tusmo dhexdeeda:

```tus
// Gudaha stdlib/os.tus
hawl halkee() : eray {
    soo_celi ___c__call_("tusmo_os_cwd"); // tusmo_os_cwd waa function laga leeyahay c  waxaana looga dhex wacay tusmo dhexdeeda
}
```

**Sida ay u shaqeyso:**
1. Parser-ku wuxuu sameeyaa in function-ka C uu ku daro `CCallNode` ee ast-ga
2. Transpiler-ku wuxuu soo saaraa: `tusmo_os_cwd()`
3. Hawsha(function-ka) C waa inay ka jirtaa runtime-ka

**Maxaa loo isticmaalaa?**
- In lagu waco hawlaha(functions-ka) C runtime sida(file I/O, sockets, wakhti)
- Helitaanka shaqooyinka ilaa heerka nidaam (system-level)
- Hawlgallada muhiimka u ah waxqabadka (performance)

### Hawsha `___c__code_`

Si toos ah u dhex geli code C file tusmo ah:

```tus
___c_code_("#include <math.h>"); // kani waa code c ah lkn ku dhex qoran tusmo file
```

Tani waxay si toos ah ugu koobiyaysaa code-ka C ee la abuuri dooono .

### Runtime Linking

Tusmo waxay si otomaatig ah u ogaataa features runtime ee loo baahan yahay:

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

Runtime-ka waxaa ku jira:
- `runtime/string.c` - Hawlgallada erayga (String)
- `runtime/array.c` - Hawlgallada tixda (Array)
- `runtime/dictionary.c` - Hawlgallada qaamuuska (Dictionary)
- `runtime/os.c` - Hawlaha OS
- `runtime/time.c` - Hawlaha wakhtiga
- `runtime/socket.c` - Hawlaha socket
- `runtime/http.c` - Server-ka HTTP

## Qaab-dhismeedka Code-ka C ee la Sameeyay

```c
#include "tusmo_runtime.h"

int main(void) {
    GC_INIT();
    
    // Code-kaaga halkan geli
    
    return 0;
}
```

Header-ka runtime-ka wuxuu bixiyaa:
- GC_INIT() - Bilaabista qashin-ururiyaha (garbage collector)
- TusmoString - Nooca erayga
- TusmoTixTiro - Nooca tixda integer-ka
- TusmoQaamuus - Nooca qaamuuska
- Hawlaha caawiyaha ah

## Hirgelinta Kooxda (Class Implementation)

Kooxaha (classes) waxaa loo hirgeliyaa sidii C structs oo leh function pointers:

```c
// Sidee Loo sameeyay koox Qof { keyd:eray magac; } marka la joogo C
typedef struct Qof {
    char* magac;
    // ... meelo kale
} Qof;

// Habka (Method)
void Qof_setName(Qof* kan, char* magac) {
    kan->magac = magac;
}
```

## Maareynta Memory-ga (Memory Management)

Tusmo waxay isticmaashaa Boehm garbage collector:

```c
#include <gc.h>

int main(void) {
    GC_INIT();
    // Dhammaan qoondaynta waa otomaatig
}
```

Uma baahna `malloc`/`free` gacanta ah!

## Hawlaha C ee Adiga kuu Gaar ah

Waxaad ku dari kartaa hawlahaaga C runtime-ka:

1. Abuur `.c` oo ku dar hawlaha (function-ka) kadib file-ka waa in lagaliyaa `runtime/`
2. Ku sheeg gudaha file-ka `runtime/tusmo_runtime.h` oo ku cadeey halkaas hawlaha(functions-ka) uu ka koobanyahay faylka aad abuurtay
3. Ka wac Tusmo adigoo isticmaalaya `___c__call_("hawshaada")`

Tusaale:

```c
// runtime/math.c
int tusmo_my_add(int a, int b) {
    return a + b;
}
```

```c
// runtime/tusmo_runtime.h
extern int tusmo_my_add(int a, int b);
```

```tus
// Gudaha faylkaaga xisaab.tus
keyd:tiro natiijo = ___c__call_("tusmo_my_add", 3, 4);
```

## Nidaamka Dhisidda (Build Process)

Markaad socodsiiso `tusmo hello.tus`:

1. Turjum `hello.tus` + dhammaan module-lada la (import-kareeyay) iyadoo loo turjumaayo C
2. Dhis AST
3. Hubi nooca (Type check)
4. Samee `hello.c`
5. U Turjum binary: `zig cc hello.c runtime/*.c -lgc -o hello` from C to binary
6. run-garee `./hello`

Siidaynta la socota waxaa ku jira wax kasta oo loo baahan yahay - ma jiraan waxyaabo ka baxsan oo loogu baahan yahay.
