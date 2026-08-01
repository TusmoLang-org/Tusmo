# Bilaabista Degdegga ah (Getting Started)

Boggan wuxuu kugu hagayaa sida aad kombuyuutarkaaga ugu rakibi lahayd **Tusmo** iyadoo aan loo baahnayn wax shuruudo ah oo hore, iyo sida aad u qori lahayd barnaamijkaagii ugu horreeyay.

---

## 🚀 Eeber-Shuruudood (Zero-Dependency Architecture)

Luuqadda Tusmo waxaa loo dhisay hab casri ah oo **Eeber-Shuruudood ah (Zero-Dependency)**. Maadaama aan diyaarinay nidaam otomaatig ah oo GitHub Workflows ah, uma baahnid inaad kombuyuutarkaaga ku sii rakibto Python, GCC, ama aalado kale oo C compiler ah. 

Markaad soo degsato faylka la soo xiray ee Tusmo ee ka soo baxa GitHub Releases, waxaad helaysaa:

1. **Tusmo CLI Executable (`bin/tusmo`)**: Barnaamij iskiis u istaagaya oo precompiled ah (lagu dhisay PyInstaller), kaas oo aan u baahnayn in Python ku rakiban yahay kombuyuutarkaaga.
2. **Qalab-dhisid Diyaarsan (Built-in Zig Toolchain)**: Waxaa la socda compiler-ka **Zig** oo self-contained ah, kaas oo u shaqeeya sidii C compiler-ka rasmiga ah oo dhalinaya executable files aad u dheereeya nidaam kasta (Linux, macOS, iyo Windows).

---

## 📦 Sida loo Rakibo (Installation Guide)

### 1. Rakibaadda Caadiga ah (Precompiled Releases)
Kani waa habka ugu habboon ee loogu talagalay dhammaan isticmaalayaasha:

1. Booqo bogga **GitHub Releases** ee mashruuca Tusmo.
2. Soo degso faylka u dhigma nidaamkaaga hawlgalka:
   - **Linux**: `tusmo-linux-x86_64.tar.gz`
   - **macOS**: `tusmo-mac-x86_64.tar.gz`
   - **Windows**: `tusmo-windows-x86_64.zip`
3. Soo saar (extract) faylka aad soo dejisay.
4. Ku dar galka `bin/` nidaamkaaga **Environment Path (PATH)** si aad amarka `tusmo` uga waci karto terminal kasta.

---

### 🛠️ 2. Habka Horumarinta (Developer / Source Build Mode)
Haddii aad tahay borogaraamye raba inuu wax ka beddelo compiler-ka laftiisa ama koodhka ka socodsiiyo source-ka:

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

## ✍️ Barnaamijkii Ugu Horreeyay

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

### ⚙️ Maxaa Dhacaya Markaad Kiciso?
1. **Dhalinta C Code-ka**: Compiler-ka Tusmo wuxuu akhriyayaa faylka `hello.tus`, wuxuu hubinayaa naxwaha iyo ammaanka koodhka, ka dibna wuxuu dhalinayaa fayl C ah oo la yiraahdo `hello.c`.
2. **Isku-darka (C Compilation)**: Wuxuu si toos ah u wacaa built-in compiler-ka (`zig cc` ama `gcc`) si uu faylka `hello.c` ugu beddelo binary orod gaar ah leh (`hello` ee Linux/macOS ama `hello.exe` ee Windows).
3. **Socodsiinta**: Wuxuu orodsiinayaa executable file-kaas si uu kuugu muujiyo natiijada shaashadda!

Shaashaddaada waxaa ku soo bixi doona:
```text
Hambalyo! Koodhkaagii ugu horreeyay ee Tusmo waa uu shaqeeyay.
```

---

## 🛠️ compilation-ka Gaarka ah (Custom Compile Options)

Haddii aad rabto inaad koodhkaaga u compile-gareyso executable file gaar ah oo aad hadhow ordi karto adigoon dib u wacin compiler-ka, waxaad ordi kartaa:

```bash
# Soo saar executable la yiraahdo "barnaamij_kayga"
tusmo hello.tus -o barnaamij_kayga

# Source Mode ahaan
python3 tusmo.py hello.tus -o barnaamij_kayga
```

Hambalyo! Waxaad si guul leh u baratay deegaanka iyo rakibaadda luuqadda Tusmo. Hadda u gudub bogga xiga ee **Aasaaska Luuqada** si aad u barato naxwaha iyo qorista koodhka.
