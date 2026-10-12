# Tusmo

Tusmo waa luuqad barnaamij-sameyn oo naxwaha Af-Soomaaliga ku dhisan. Compiler-ku wuxuu Tusmo u turjumaa C, ka dibna wuxuu soo saaraa barnaamij native ah oo ku shaqeeya nidaamka hawlgalka isticmaalaha.

Tusmo waxaa loogu talagalay in lagu barto laguna dhiso barnaamijyo nidaam, adeegyo shabakad, qalab utility ah, iyo ciyaaro 2D/3D ah.

> Tusmo weli waa beta. Linux source builds iyo Windows cross-compilation waa la tijaabin karaa; Windows runtime testing waxaa xaqiijiya GitHub Actions runner-ka Windows.

[English](README.md) | [Af-Soomaali](README-so.md)

## Astaamaha

- Naxwe iyo ereyo muhiim ah oo Af-Soomaali ah.
- Tusmo-to-C transpilation, oo lagu dhiso GCC ama compiler-ka ku jira release-ka.
- Semantic analysis iyo checks la xiriira noocyada xogta iyo lifetime-ka.
- Functions, lambdas, arrays, dictionaries, classes, inheritance, modules, iyo embedded C.
- Standard library loogu talagalay I/O, waqtiga, OS, HTTP, sockets, WebSockets, xisaab, iyo random values.
- Raylib bindings loogu talagalay daaqado, graphics, input, audio, iyo ciyaaro.
- VS Code extension leh syntax highlighting, icons, iyo language-server support.

## Platform support

| Platform | Taageero |
| --- | --- |
| Linux x86_64 | Source compiler iyo release installer |
| Windows x86_64 | Release installer iyo native CI tests |
| macOS ARM64 | Release installer |
| Linux → Windows | MinGW-w64 cross-compilation; Wine waa optional |

Windows source builds waxay u baahan yihiin GCC/MinGW ama toolchain-ka ku jira release-ka. Windows native tests waxay ku shaqeeyaan `windows-latest` GitHub Actions runner.

## Rakibidda release-ka

### Linux

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

### macOS (Apple Silicon / ARM64)

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

### Windows PowerShell

```powershell
iwr -useb https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```

Kadib fur terminal cusub oo hubi rakibidda:

```bash
tusmo --version
```

Release installer-ku wuxuu bixiyaa Tusmo CLI, runtime files, standard library, iyo toolchain-ka loo baahan yahay marka release asset-ka la isticmaalo.

Haddii aad rabto inaad release-ka gacanta ka soo dejisato, ka dooro [GitHub Releases](https://github.com/TusmoLang-org/Tusmo/releases) asset-ka ku habboon: `tusmo-linux-x86_64.tar.gz`, `tusmo-macos-arm64.tar.gz`, ama `tusmo-windows-x86_64.tar.gz`. Installer-rada kore ayaa soo dejinaya oo rakibaya package-ka saxda ah.

## Source development

Linux developer setup:

```bash
sudo apt install python3 python3-pip gcc
python3 -m pip install ply requests
git clone https://github.com/TusmoLang-org/Tusmo.git
cd Tusmo
```

Windows developer setup wuxuu isticmaali karaa Python iyo MSYS2 MinGW:

```bash
python -m pip install ply requests
```

Kadib ku rakib MSYS2 MinGW GCC, ama isticmaal Windows release bundle-ka.

## Barnaamijka ugu horreeya

Samee `hello.tus`:

```tusmo
hawl main(): waxbo {
    qor("Salaan Tusmo!");
}
```

Ku compile-garee source mode:

```bash
python3 tusmo.py hello.tus
```

Compiler-ku wuxuu soo saaraa executable native ah. Faylka C-ga ku hay si aad u baarto adigoo isticmaalaya:

```bash
python3 tusmo.py hello.tus --c
```

## Testing

### Language-server tests

```bash
python3 Extension/server/test_server.py -v
```

Tijaabadani waxay hubisaa completion, definitions, diagnostics, document symbols, AST coordinates, iyo import caching.

### Windows native tests

GitHub Actions workflow-ku wuxuu ku shaqeeyaa Windows wuxuuna hubiyaa:

- Tusmo CLI startup;
- language-server tests;
- GCC compilation;
- `.exe` generation;
- execution iyo output-ka barnaamij Tusmo ah.

Workflow-ga: `.github/workflows/windows-test.yml`

### Windows cross-compilation from Linux

Haddii aad Linux isticmaalayso, VMware looma baahna si loo xaqiijiyo in Windows executable la abuuri karo. Ku rakib MinGW-w64 iyo Wine:

```bash
sudo apt install gcc-mingw-w64-x86-64 wine
./windows/test_linux_cross.sh
```

Haddii aad rabto kaliya compile test, adigoon Wine isticmaalin:

```bash
CROSS_COMPILE_ONLY=1 ./windows/test_linux_cross.sh
```

## VS Code extension

Extension-ku wuxuu ku yaal `Extension/`.

```bash
cd Extension
npm install
npx vsce package
```

Kadib VS Code ka dooro **Install from VSIX** oo rakib `.vsix` faylka la sameeyay.

Extension-ku wuxuu bixiyaa:

- `.tus` syntax highlighting;
- Tusmo file icon;
- hover/document tooling;
- completion, diagnostics, definitions, iyo document symbols marka language server la heli karo.

## Qaab-dhismeedka repository-ga

```text
compiler/                 Lexer, parser, semantic analyzer, transpiler
stdlib/                   Tusmo standard library iyo C runtime support
stdlib/raylib/            Raylib bindings iyo examples
stdlib/opencv/            OpenCV bridge
Extension/                VS Code extension iyo language server
test/                     Tusmo compiler/runtime test programs
windows/                  Windows smoke test iyo Linux cross-test
doc/                      Language reference
docs/                     Getting-started iyo project documentation
.github/workflows/        Release iyo CI workflows
tusmo.py                  Compiler CLI entry point
```

## Limitations

- Compiler-ka iyo standard library-gu weli way horumarayaan.
- Native Windows execution waa in lagu xaqiijiyaa Windows CI ama Windows machine; Wine kaliya waa compatibility check.
- API-yada Raylib iyo OpenCV waxay ku xirnaan karaan toolchain iyo libraries-ka platform-ka.
- Documentation-ka qaar iyo language features cusub waxay noqon karaan kuwo is beddelaya inta beta development-ku socdo.

## Contributing

1. Samee branch cusub.
2. Ku dar ama cusboonaysii tests marka aad feature ama bug fix samaynayso.
3. Orod language-server tests iyo platform test-ka ku habboon.
4. Hubi in generated files iyo local binaries aan la commit-gareyn.

Pull requests iyo bug reports waa lagu soo dhaweynayaa.

## License

Mashruucan waxaa lagu qaybiyay MIT License.
