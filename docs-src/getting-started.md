# Bilaabista

## Rakibidda (Installation)

### Linux/macOS

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

### Windows

```powershell
irm https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```
## Talo Muhiim ah
Markaad la soo dagto tusmo waa inaad isticmaasho ***VScode*** si aad u hesho **syntax highlighter** iyo **hover documentation** kuwaaso si automatic ah kugu soo dagi doono xiliga installation-ka haddii vscode uu kugu jiray horey.

## Barnaamijkaagii ugu Horreeyay

Sameey `hello.tus`:

```tus
qor("Hello, Soomali Developers!");
```

## Sida loo run loo dhaho Tusmo

Kaliya u gudbi faylka `.tus` amarka tusmo:

```bash
tusmo hello.tus
```

## Isticmaalka (Usage)

```
tusmo <fayl.tus> [doorashooyin]

Doorashooyinka (Options):
  --c           Hayso faylka code-ka C ee la sameeyay
  -h, --help    Kutusinaysa cawimaad (help)
  -v, --version Kutusinaysa version-ka aad haysato iyo in uu jiro version cusub
  -l, --libraries Liiska maktabadaha (libraries) ee la taageero
  update        Cusboonaysiinta Tusmo oo soo dajinaysa version-kii ugu dambeeyay
  install <lib> soo dajinta (install) maktabadaha (library)
```

## Sida ay u Shaqeyso

```
hello.tus  →  tusmo (parser)  →  hello.c  →  zig cc  →  hello (binary)  →  ./hello
                       ↓  
              ↓      iyadoo la isticmaalayo python
         AST → semantic analysis → C code generation
              ↓
         runtime/*.c + stdlib/*.tus → la xiriiriyay (linked)
```

### Pipeline-ka Turjumidda (Compilation Pipeline)

1. **Lexing** - Token-ka laga soosaraya code-ka Tusmo
2. **Parsing** - Dhis AST (Abstract Syntax Tree)
3. **Semantic Analysis** - Hubinta nooca (type checking), xallinta astaanta (symbol resolution)
4. **Code Generation** - Samee code-ka C iyadoo la isticmaalayo AST
5. **Compilation** - Zig wuxuu u beddelaa C-code-ka binary la fulin karo
6. **Execution** - Run-kareynta binary-ga

Siidaynta (release) la socota waxaa ku jira:
- **Zig compiler** - Wuxuu C u beddelaa binary
- **Boehm GC** - Qashin-ururiye (Garbage collector) (horay loo dhisay)
- **Runtime library** - Taageerada erayga (string), tixda (array), qaamuuska (dictionary)
- **Standard library** - OS, HTTP, sockets, iwm.

Uma baahnid inaad soo dagsato GCC ama libgc gacantaada.

### Hayso Code-ka C (Keep C Code)

U isticmaal calanka (flag) `--c` si aad u haysato faylka C ee la sameeyay:

```bash
tusmo hello.tus --c
```

Tani waxay soo saaraysaa `hello.c` isla directory-ga dhexdiisa.

## Tusaale Code

```tus
// Barnaamijkaygii ugu horreeyay ee Tusmo
keyd:eray magac = "Tusmo";
keyd:tiro da'da = 5;

qor($"Hello, {magac}!");
qor($"Da'da: {da'da}");
```

Natiijada (Output):
```
Hello, Tusmo!
Da'da: 5
```

## Shuruudaha (Requirements)

Haddii aad ula soo dageyso luqadan adigoo umaraayo install.sh ama install.ps1 uma baahnid:
- Zig compiler
- Boehm GC
- Maktabadaha Runtime (Runtime libraries)

Kaliya soo dagso luuqada adigoo u maraayo 
### Windows / MacOs
```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

### Windows

```powershell
irm https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```
kadib horey ugal qorista code-ka tusmo 
