# Bilaabista Degdegga ah (Getting Started)

Boggan wuxuu kugu hagayaa sida aad kombuyuutarkaaga ugu rakibi lahayd **Tusmo** iyadoo aan loo baahnayn wax shuruudo ah oo hore, iyo sida aad u qori lahayd barnaamijkaagii ugu horreeyay.

---

## Eeber-Shuruudood (Zero-Dependency Architecture)

Luuqadda Tusmo waxaa loo dhisay hab casri ah oo **Eeber-Shuruudood ah (Zero-Dependency)**. Maadaama aan diyaarinay nidaam otomaatig ah oo GitHub Workflows ah, uma baahnid inaad kombuyuutarkaaga ku sii rakibto Python, GCC, ama aalado kale oo C compiler ah. 

Markaad soo degsato faylka la soo xiray ee Tusmo ee ka soo baxa GitHub Releases, waxaad helaysaa:

1. **Tusmo CLI Executable (`bin/tusmo`)**: Barnaamij iskiis u istaagaya oo precompiled ah (lagu dhisay PyInstaller), kaas oo aan u baahnayn in Python ku rakiban yahay kombuyuutarkaaga.
2. **Qalab-dhisid Diyaarsan (Built-in Zig Toolchain)**: Waxaa la socda compiler-ka **Zig** oo self-contained ah, kaas oo u shaqeeya sidii C compiler-ka rasmiga ah oo dhalinaya executable files aad u dheereeya nidaam kasta (Linux, macOS, iyo Windows).

---

## Sida loo Rakibo (Installation Guide)

### 1. Rakibaadda Caadiga ah (Precompiled Releases)
Kani waa habka loogu talagalay dadka raba inay Tusmo isticmaalaan. Looma baahna in repository-ga la clone-gareeyo ama Python, GCC, ama Zig gooni loo rakibo. Installer-ku wuxuu soo dejinayaa release-ka precompiled-ka ah, wuxuuna ku rakibayaa kombiyuutarkaaga.

#### Linux (x86_64)

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

#### macOS (Apple Silicon / ARM64)

```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

#### Windows (x86_64, PowerShell)

```powershell
iwr -useb https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```

Marka rakibiddu dhammaato, fur terminal cusub oo hubi:

```bash
tusmo --version
```

Haddii aad rabto inaad release-ka gacanta ka doorato, ka soo degso [GitHub Releases](https://github.com/TusmoLang-org/Tusmo/releases) faylka ku habboon:

| Nidaamka | Release asset |
| --- | --- |
| Linux x86_64 | `tusmo-linux-x86_64.tar.gz` |
| macOS ARM64 | `tusmo-macos-arm64.tar.gz` |
| Windows x86_64 | `tusmo-windows-x86_64.tar.gz` |

Intel macOS hadda lama taageero. Habka hoose ee `git clone` waa keliya dadka raba inay source-ka wax ka beddelaan ama horumariyaan.

---

### 2. Habka Horumarinta (Developer / Source Build Mode)
Haddii aad tahay borogaraamye raba inuu wax ka beddelo compiler-ka laftiisa ama koodhka ka socodsiiyo source-ka, marka hore clone-garee repository-ga:

#### A. Linux (Debian, Ubuntu, Kali, Fedora)
```bash
sudo apt update
sudo apt install python3 python3-pip gcc make build-essential
git clone https://github.com/TusmoLang-org/Tusmo.git
cd Tusmo
```

#### B. macOS (Homebrew)
```bash
brew install gcc python
git clone https://github.com/TusmoLang-org/Tusmo.git
cd Tusmo
```

#### C. Windows
Soo degso [Python Windows Installer](https://www.python.org/downloads/) (hubi inaad calaamadeyso **"Add Python to PATH"**) iyo [MSYS2](https://www.msys2.org/) oo ku rakib GCC adoo orodaya:
```bash
pacman -S mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-make
```

---

## Barnaamijkii Ugu Horreeyay

Aan qorno barnaamijkeenii ugu horreeyay ee Tusmo!

### Tallaabada 1: Qor Koodhka
Abuur fayl cusub oo lagu magacaabo `hello.tus` adigoo isticmaalaya VS Code ama tifaftire kasta, kuna qor koodhka soo socda:

```tusmo
hawl main() : waxbo {
    qor("Hambalyo! Koodhkaagii ugu horreeyay ee Tusmo waa uu shaqeeyay.");
}
main();
```

> [!TIP]
> Haddii aad rabto inaad si toos ah u orodsiiso koodh adigoon abuurin shaqo, waxaad isticmaali kartaa **Global Scripting Mode** oo koodhka toos u qori kartaa:

```tusmo
qor("Hambalyo! Koodhkaagii ugu horreeyay ee Tusmo waa uu shaqeeyay.");
```

### Tallaabada 2: Keydi Faylka
Hubi in magaca faylku ku dhammaado `.tus` (fidinta rasmiga ah ee koodhka luuqadda Tusmo).

### Tallaabada 3: Kici Barnaamijka
Fur terminal-kaaga, u guur galkii aad ku keydisay faylka `hello.tus`, ka dibna orod amarkan:

```bash
# Haddii aad isticmaalayso Precompiled Release
tusmo hello.tus

# Haddii aad ku jirto Source/Developer Mode
python3 tusmo.py hello.tus
```

### Maxaa Dhacaya Markaad Kiciso?
1. **Dhalinta C Code-ka**: Compiler-ka Tusmo wuxuu akhriyayaa faylka `hello.tus`, wuxuu hubinayaa naxwaha iyo ammaanka koodhka, ka dibna wuxuu dhalinayaa fayl C ah oo la yiraahdo `hello.c`.
2. **Isku-darka (C Compilation)**: Wuxuu si toos ah u wacaa built-in compiler-ka (`zig cc` ama `gcc`) si uu faylka `hello.c` ugu beddelo binary orod gaar ah leh (`hello` ee Linux/macOS ama `hello.exe` ee Windows).
3. **Socodsiinta**: Wuxuu orodsiinayaa executable file-kaas si uu kuugu muujiyo natiijada shaashadda!

Shaashaddaada waxaa ku soo bixi doona:
```text
Hambalyo! Koodhkaagii ugu horreeyay ee Tusmo waa uu shaqeeyay.
```

---

## Compilation-ka Gaarka ah (Custom Compile Options)

Haddii aad rabto inaad koodhkaaga u compile-gareyso executable file gaar ah oo aad hadhow ordi karto adigoon dib u wacin compiler-ka, waxaad ordi kartaa:

```bash
# Soo saar executable la yiraahdo "barnaamij_kayga"
tusmo hello.tus -o barnaamij_kayga

# Source Mode ahaan
python3 tusmo.py hello.tus -o barnaamij_kayga
```

Hambalyo! Waxaad si guul leh u baratay deegaanka iyo rakibaadda luuqadda Tusmo. Hadda u gudub bogga xiga ee **Aasaaska Luuqada** si aad u barato naxwaha iyo qorista koodhka.
