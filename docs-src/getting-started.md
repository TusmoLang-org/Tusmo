# Bilaabista kooban

## Dagsasho (Installation)

### Linux/macOS

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

### Windows

```powershell
irm https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```
## Talo Muhiim ah
Markaad la soo dagto tusmo waa inaad isticmaasho ***VScode*** si aad u hesho **syntax highlighter** iyo **hover documentation** kuwaaso si automatic ah kugu soo dagi doono xiliga installation-ka Tusmo haddii vscode uu kugu jiray horey.

## Barnaamijkaagii ugu Horreeyay

Sameey `hello.tus`,  fayl extension-ka tusmo waa `.tus`

```tus
qor("Hello, Soomali Developers!");
```

## Sida run loo dhaho Tusmo

Kaliya u gudbi faylka `.tus` compiler-ka Tusmo:

```bash
tusmo hello.tus
```
Kadib compiler-ka `tusmo` wuxuu sameyn donaa soo saari donaa fayl binary ah kaaso oo wata isla magacii faylkii aad run kareysay tusaale annaga hadda waxaa run-gareenay fayl tusmo ah oo lagu magacaabo `hello.tus` anagoo adeegsaneyna `tusmo hello.tus` waxaa la soosaari donaa binary fayl lagu magacaabo `hello`

### Run-dheh fayl-ka binary
```
./hello
```
kadib waxaa terminal-ka ka soo bixi dooono output-ka
```output
Hello, Soomali Developers!
```

## 📋 Isticmaalka (Usage)

Qaabka guud ee amarka: 
`tusmo <fayl.tus> [doorashooyin]`

### Doorashooyinka (Options)

| Amarka (Short/Long) | Shaqada (Description) | Tusaale |
| :--- | :--- | :--- |
| `-h`, `--help` / `-c` | Bandhigga macluumaadka caawimaadda | `tusmo -c` |
| `-v`, `--version` / `-n` | Tusidda nooca (version) aad haysato | `tusmo -n` |
| `-l`, `--libraries` / `-m` | Tirinta dhamaan maktabadaha la heli karo | `tusmo -m` |
| `--c` | Keydinta faylka **C** ee la sameeyay | `tusmo hello.tus --c` |
| `dagso` / `download` | Soo dejinta maktabad (library) cusub | `tusmo dagso [magac]` |
| `update` / `cusboonaysii` | Inaad is-casriyeyso (Tusmo update) | `tusmo update` |

## Sida ay u Shaqeyso Compilerka Tusmo

```
hello.tus
   ↓
tusmo(lexer)
   ↓
tusmo (parser)
   ↓
AST(Abstract Syntax Tree)
   ↓
semantic analysis
   ↓
C code generation 
   ↓
hello.c + runtime/*.c + stdlib/*.tus
   ↓  
zig cc
   ↓
hello (binary)  →  ./hello


```

### Pipeline-ka Turjumidda (Compilation Pipeline)

1. **Lexing** -  Code-ka Tusmo ayaa loo badalayaa token
2. **Parsing** - Waxaa la Dhisayaa AST (Abstract Syntax Tree)
3. **Semantic Analysis** - Hubinta noocyadda (type checking), hubinta variable-da, functions-ka scope-yadooda
4. **Code Generation** - Sameynta code-ka C.
5. **Compilation** - Zig wuxuu u beddelaa C-code-ka binary la fulin karo (Excuteable)
6. **Execution** - Run-kareynta binary-ga



### Hayso Code-ka C (Keep C Code)

U isticmaal `--c` flag si aad u haysato faylka C ee la sameeyay haddii aad rabto, madaama compiler-ka tusmo uu tirtiri doono fayl-ka C aadan arki karin:

```bash
tusmo hello.tus --c
```

Tani waxay soo saaraysaa `hello.c` isla directory-ga dhexdiisa.

## Tusaale Code

```tus
// Barnaamijkaygii ugu horreeyay ee Tusmo
keyd:eray magac = "Tusmo";
keyd:tiro version = 20;

qor($"Hello, {magac}!");
qor($"Version: V{version}");
```

Natiijada (Output):
```
Hello, Tusmo!
Version: V20
```
## sharxidda Code-ka
`keyd` keyword-kan waa sida `var` , `let` ama `const` oo kale, waxaa loola jeedaa *keedin* si uu u muujiyo in wax la keydinaayo
`eray` keyword-kan waa sida `string` oo kale kaaasi oo sheegaya nooca xogta la keydinaayo.  
`tiro` keyword-kan waa sida `int` oo kale kaaasi oo sheegaya nooca xogta la keydinaayo.


