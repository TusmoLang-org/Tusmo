# Tusmo Programming Language 🇸🇴

Tusmo waa luuqad barnaamijyeed (programming language) casri ah oo ku qoran Af-Soomaali. Waxay isku daraysaa xawaaraha C/C++ iyo badbaadada xusuusta (memory safety) ee luuqadaha casriga ah sida Rust, iyadoo aan xitaa isticmaalin Garbage Collector (GC) culeys keena.

Waxaa loo dhisay in lagu sameeyo barnaamijyo waaweyn, ciyaaro (games), iyo adeegyo xawaare sare u baahan.

## Astaamaha Ugu Waaweyn (Key Features)

🚀 **Xawaare Sare (High Performance):** Tusmo waxay si toos ah isugu beddeshaa koodka C (`Transpiler`), waxaana la dhisay iyadoo la isticmaalayo `gcc -O3` si ay u ordo xawaaraha ugu sarreeya ee kumbuyuutarkaagu oggol yahay.

🛡️ **Badbaadada Xusuusta (Memory Safety):** Waxay leedahay nidaam xusuus-ilaalineed oo aad u casri ah (Lifetime Tracking iyo Move Semantics). Koodkaagu waligiis ma yeelanayo "Memory Leaks" ama shilal (Crashes) aan la garanayn.

🏗️ **Qaabdhismeed Casri ah (OOP & Structs):** 
- `qaab` (Structs): Qaabdhismeedyo xawaare sare leh oo si toos ah xusuusta (stack) u fadhiisanaya sidii C.
- `koox` (Classes): Barnaamijyo casri ah oo wata dhaxal (Inheritance) iyo faham buuxa oo Object-Oriented ah.

🎮 **Ciyaaraha & Garaafikada (Game Engine Ready):** Waxaa si buuxda ugu dhex jirta maktabadda garaafikada ee **Raylib**, taas oo boqolkiiba boqol loo tarjumay Af-Soomaali.

🧩 **Ku-darka VS Code (Extension):** Tusmo waxay leedahay extension u gooni ah oo leh *Syntax Highlighting*, *Auto-complete*, iyo *Hover documentation* oo ku tusiya macluumaadka shaqo kasta inta aadan qorin!

## Habka Loogu Yeero (Module System)
Tusmo waxay leedahay nidaam soo-dejineed oo aad u awood badan:
- `keen "module";` – Waxay soo wadataa module-ka oo dhan.
- `isticmaal {hawl1, koox2} kujira "module";` – Waxay soo qaadataa oo keliya waxaad u baahan tahay, iyadoo tirtiraysa wixii "Dead Code" ah si barnaamijkaagu u noqdo mid fudud.

---

## 📥 Sida Loo Rakibo (Installation Guide)

### Windows
Fur **PowerShell** (Run as Administrator) oo ku qor:
```powershell
iwr -useb https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex
```

### Linux / macOS
Fur **Terminal** oo ku qor:
```bash
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash
```

Kadib markaad rakibto, fur terminal cusub oo tijaabi adigoo qoraya:
```bash
tusmo -v
```

---

## 📖 Sida Loo Qoro Tusmo (Quick Documentation)

Tusmo waxay leedahay naxwe (syntax) aad u fudud oo la fahmi karo. Halkan waxaa ah aasaaska luuqadda:

### 1. Keydiyaha & Noocyada Xogta (Variables & Data Types)
Si aad xog u keydiso, isticmaal erayga `keyd` iyo nooca xogta (`tiro`, `jajab`, `eray`, `xaraf`, `miyaa`, ama `walbo`).

```tus
// Keydinta tirooyinka (Integers & Floats)
keyd:tiro daDaada = 20;
keyd:jajab miisaanka = 65.5;

// Keydinta qoraalka (Strings & Chars)
keyd:eray magaca = "Axmed";
keyd:xaraf xarafkaHore = 'A';

// Keydinta Haa/Been (Booleans)
keyd:miyaa waaArday = run;  // run (true) ama been (false)
```

### 2. Qeexidda Ma-beddelayaasha (Constants)
Haddii aad rabto xog aan waligeed is-beddelayn (Constants/Macros), isticmaal `qeex`. Tani xawaaraha ayay badisaa maxaa yeelay toos ayaa loogu beddelaa C.

```tus
qeex PI = 3.14159;
qeex MAGACA_BARTA = "Tusmo Hub";

hawl main(): waxbo {
    keyd:jajab goobo = PI * 10.0;
    qor(MAGACA_BARTA);
}
```

### 3. Wareegyada (Loops)
Tusmo waxay leedahay qaabab kala duwan oo wareeg (Loops) loo sameeyo.

**Wareegga Tirooyinka (For Range):**
```tus
// Waxay qoraysaa tirooyinka 1 ilaa 5
soco i laga bilaabo 1..5 {
    qor("Tirada waa: ", i);
}
```

**Wareegga Shuruudda (While Loop):**
```tus
keyd:tiro x = 0;
inta ay (x < 3) {
    qor("Wali wuu socdaa...");
    x = x + 1;
}
```

### 4. Qaabdhismeedka (Structs)
`qaab` waa hab lagu ururiyo xogo kala duwan oo hal meel ku wada jira. Waa (Value Type) oo xawaare aad u sarreeya ku orda!

```tus
// 1. Dhisida Qaabka (Defining the Struct)
qaab Qof {
    keyd:eray magac;
    keyd:tiro da;
}

hawl main(): waxbo {
    // 2. Abuurida (Instantiation)
    keyd:Qof qof1 = (Qof){"Cali", 25};
    
    // 3. Isticmaalka (Usage)
    qor("Magacu waa: ", qof1.magac);
    qor("Da'diisu waa: ", qof1.da);
}

main();
```

---

## 🎮 Tusaale Ciyaar (Game Example with Raylib)
Tusmo waxay diyaar u tahay dhisidda ciyaaraha! Halkan waa tusaale fudud oo muujinaya daaqad:

```tus
// Soo daji qaybaha Raylib adigoo isticmaalaya "isticmaal" si aadan memory-ga u buuxin
isticmaal {bilowDaaqada, xaddidFps, daaqadaMaXirantahay, bilowSawirka, dhameeySawirka, xirDaaqada} kujira "stdlib/raylib/window";
isticmaal {nadiifiShaashada, sawirGoob} kujira "stdlib/raylib/graphics";
isticmaal {kuqor, helFar} kujira "stdlib/raylib/text";
isticmaal {Midab, Boos2D, AfarGees} kujira "stdlib/raylib/types";

qeex MADOW = (Midab){0, 0, 0, 255};
qeex CAGAAR = (Midab){0, 228, 48, 255};
qeex CAD = (Midab){255, 255, 255, 255};

hawl main(): waxbo {
    bilowDaaqada(800, 600, "Ciyaartayda Koowaad!");
    xaddidFps(60);

    // Soo ruriso farta (Load Font)
    // Tusaale ahaan: qeex MAGACA_FARTA = "font_kasta.ttf";
    keyd:walbo far = helFar("stdlib/raylib/fonts/Tinos-Bold.ttf");

    inta ay (daaqadaMaXirantahay() == been) {
        bilowSawirka();
        nadiifiShaashada(MADOW);
        
        sawirGoob(400.0, 300.0, 50.0, CAGAAR);
        
        keyd:Boos2D booska = (Boos2D){250.0, 400.0};
        kuqor(far, "Tusmo waa cajiib!", booska, 30.0, CAD);
        
        dhameeySawirka();
    }
    xirDaaqada();
}

main();
```

## Sida Loo Isticmaalo (Usage)
Kadib markaad rakibto, fur Terminal-ka oo ku qor:
```bash
tusmo magaca_faylkaaga.tus
```

## Faylasha Halkan Ku Jira (Repository Structure)
- `/compiler` – Maskaxda luuqadda: Qaybta turjumeysa (Transpiler) iyo falanqeeyaha naxwaha (Semantic Analyzer & Lifetime Tracker).
- `/runtime` – Koodka C ee asalka u ah Tusmo, xakameynaya xusuusta, tixaha (arrays), qaamuusyada (dictionaries), iyo I/O.
- `/stdlib` – Maktabadaha caadiga ah ee Tusmo (Sida Raylib, OS, HTTP, WebSockets).
- `/Extension` – Ku-darka VS Code ee rasmiga ah oo ay ku jirto *Tusmo Language Server Protocol (LSP)*.