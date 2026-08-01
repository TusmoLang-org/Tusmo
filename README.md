# 🌌 Tusmo Programming Language

**Tusmo** waa luuqad heer-nidaam ah (system programming language) oo 100% ku qoran **Af-Soomaali**. Waxay si gaar ah isugu darsatay **xawaaraha hufan ee C/C++** iyo **nabadgelyada memory-ga (memory safety) ee Rust**, iyadoo aan gabi ahaanba isticmaalin Garbage Collector (GC).

Luuqadan waxaa loo dhisay si ay u noqoto mid ay fududahay in lagu barto lagu dhiso softweerro waaweyn, mareegaha shabakada (web development), codsiyada shabakadaha (networking), iyo ciyaaraha 2D/3D iyadoo la adeegsanayo naxwaha Af-Soomaaliga.

---

## 🚀 Astaamaha Ugu Waaweyn (Key Features)

*   **Xawaare Sare (High Performance):** Tusmo waxay koodhka u turjumtaa (transpile) C code aad u nadiif ah, waxaana lagu dhisay compiler-ka `gcc -O3` ama `zig` si ay u hesho xawaaraha ugu sarreeya ee hardware-kaagu awoodo.
*   **Lifetime Tracker (No GC):** Waxay leedahay nidaam compile-time ah oo la socda badbaadada xusuusta (Rust-like Lifetime Tracker). Waxay si toos ah u dhalisaa code-ka xusuusta nadiifinaya (`tusmo_free`) marka uu scope-ku dhammaado.
*   **Object-Oriented Programming (OOP):** Waxay taageertaa habdhismeedka Class-yada (`koox`) oo leh dhaxal (`dhaxlaya`) iyo Struct-yada (`qaab`).
*   **Anonymous Functions & Lambdas:** Waxay si buuxda u taageertaa concise arrow lambdas iyo block anonymous functions.
*   **🎮 Ciyaaraha & Garaafikada (Raylib Native):** Waxaa si toos ah ugu dhex jira maktabadda ciyaaraha caanka ah ee Raylib oo 100% loo Soomaaliyeeyay!
*   **🧩 VS Code Tooling (LSP Server):** Horumarin dhammaystiran oo ay ku jiraan Autocomplete, Hover docs, Go to Definition (Ctrl+Click), Document Symbols (Outline), iyo Real-time Diagnostics.

---

## 📥 Habka Rakibaadda (Installation Guide)

### 🐧 Linux / macOS
Fur **Terminal-kaaga** oo ku qor amarkan si aad si toos ah ugu rakibto:
```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

### 🪟 Windows
Fur **PowerShell** (ku orodsii adigoo ah Administrator) oo ku qor:
```powershell
iwr -useb https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```

Marka uu rakibaaddu dhammaado, xaqiiji adigoo ku qoraya terminal cusub:
```bash
tusmo -v
```

---

## 📖 Deep Documentation Menu (doc/)

Haddii aad rabto inaad si qoto dheer u barato luuqada Tusmo oo aad dhisato softweer ama ciyaaro, fadlan booqo dukumiintiyada rasmiga ah ee ku dhex jira folder-ka [doc/](file:///home/mubaarak/Desktop/Tusmo/doc/):

*   **📘 [Qaybta 1: Aasaaska Luuqadda](file:///home/mubaarak/Desktop/Tusmo/doc/aasaaska.md)** - Primitives, Variables (`keyd`), Constants (`qeex`), iyo Operations.
*   **🚦 [Qaybta 2: Xakamaynta Socodka](file:///home/mubaarak/Desktop/Tusmo/doc/xakamaynta.md)** - Shuruudaha (`haddii/haddii_kale/kale`) iyo Loops (`inta ay`, `soco...laga bilaabo`).
*   **📦 [Qaybta 3: Habaynta Xogta](file:///home/mubaarak/Desktop/Tusmo/doc/xogta.md)** - Tixaha (`Arrays` - `keyd:tiro[]`) iyo Qaamuusyada (`Dictionaries`).
*   **⚙️ [Qaybta 4: Hawlaha & Lambdas](file:///home/mubaarak/Desktop/Tusmo/doc/hawlaha.md)** - Hawlaha, Function pointers, iyo Anonymous Lambdas.
*   **🏗️ [Qaybta 5: Object-Oriented Programming (OOP)](file:///home/mubaarak/Desktop/Tusmo/doc/oop.md)** - Structs (`qaab`) iyo Classes (`koox`) oo leh Dhaxalka (`dhaxlaya`).
*   **🛡️ [Qaybta 6: Badbaadada Xusuusta (Memory Safety)](file:///home/mubaarak/Desktop/Tusmo/doc/memory.md)** - Ownership model, Move Semantics, iyo Lifetime tracking.
*   **🔌 [Qaybta 7: Module System](file:///home/mubaarak/Desktop/Tusmo/doc/modules.md)** - Isticmaalka ereyada `keen` iyo `isticmaal...kujira`.
*   **🎮 [Qaybta 8: Maktabadaha Dhex-dhisan (Standard Library)](file:///home/mubaarak/Desktop/Tusmo/doc/stdlib.md)** - Raylib (Gaming), OS, HTTP, iyo WebSockets Deep APIs.

---

## 🛠️ Wax-ku-biirinta & Tijaabooyinka (Contribution & Testing)

Orodso amarkan si aad u tijaabiso LSP server-ka iyo compiler-ka ka hor inta aanad push-gareyn koodhka:
```bash
python3 Extension/server/test_server.py -v
```

Dhammaan tijaabooyinka waa inay soo saaraan natiijadan si guul leh:
```text
test_doc_entry_coordinates ... ok
test_import_caching ... ok
test_lsp_completion ... ok
test_lsp_definition ... ok
test_lsp_diagnostics ... ok
test_lsp_document_symbols ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.007s

OK
```

---

## 📄 Ruqsadda (License)

Mashruucan waxaa lagu daabacay ruqsadda rasmiga ah ee **MIT License**.

*Waxaa dhisay oo curiyay Bulshada Soomaaliyeed ee Horumarinta Softweerka (Somali Software Developers Community).* 🇸🇴