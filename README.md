# Tusmo Programming Language 🇸🇴

Tusmo waa luuqad (programming language) casri ah oo ku qoran Af-Soomaali. Waxay isku daraysaa xawaaraha C/C++ iyo badbaadada Memory-ga (memory safety) ee luuqadaha casriga ah sida Rust, iyadoo aan xitaa isticmaalin Garbage Collector (GC) culeys keena.

Waxaa loo dhisay in lagu sameeyo barnaamijyo waaweyn, ciyaaro (games), iyo adeegyo xawaare sare u baahan.

## Astaamaha Ugu Waaweyn (Key Features)

**Xawaare Sare (High Performance):** Tusmo waxay si toos ah isugu beddeshaa koodka C (`Transpiler`), waxaana la dhisay iyadoo la isticmaalayo `gcc -O3 ama zig` si ay u ordo xawaaraha ugu sarreeya ee kumbuyuutarkaagu oggol yahay.

**Badbaadada Xusuusta (Memory Safety):** Waxay leedahay nidaam xusuus-ilaalineed oo aad u casri ah. Koodkaagu waligiis ma yeelanayo "Memory Leaks" ama shilal (Crashes) aan la garanayn.

**Qaabdhismeed Casri ah (OOP & Structs):** 
- `qaab` (Structs): Qaabdhismeedyo xawaare sare leh oo si toos ah xusuusta (stack) u fadhiisanaya sidii C.
- `koox` (Classes): Luqadan waxay leedahay `koox`(class) casri ah oo wata dhaxal (Inheritance) iyo faham buuxa oo Object-Oriented ah.

**Desktop Development, Ciyaaraha 2D games, & Garaafikada (Game Engine Ready):** Waxaa si buuxda ugu dhex jirta maktabadda garaafikada **Raylib**, taas oo boqolkiiba boqol loo tarjumay Af-Soomaali (sida `bilowDaaqada()`, `sawirAfarGees()`).

**VS Code (Extension):** Tusmo waxay leedahay extension u gooni ah oo leh *Syntax Highlighting*, *Auto-complete dropdowns*, iyo *Hover documentation* oo ku tusiya macluumaadka shaqo kasta inta aadan qorin!

## Habka Loogu Yeero (Module System)
Tusmo waxay leedahay nidaam soo-dejineed ee lagu yaqaano afka qalaad (module import) oo aad u awood badan:
- `keen "module";` – Waxay soo uruurisaa dhamaan code-ka ku qoran module-ka(faylka la keenayo).
- `isticmaal {hawl1, koox2, varibale3} kujira "module";` – Waxay soo qaadataa oo keliya waxaad u baahan tahay, iyadoo iska indho tiraysa wax yaabaha aadan u baahneen si looga fogaado "Dead Code" si uu u noqdo program mid xawaare leh, size-kisu yaryahay.

## Tusaale Degdeg ah (Quick Example)
Halkan waa tusaale fudud oo muujinaya daaqad ciyaar oo raylib ah:

```tus
keen "stdlib/raylib/core";

qeex BALLAC = 800;
qeex DHEER = 600;

hawl main(): waxbo {
    bilowDaaqada(BALLAC, DHEER, "Tusmo Raylib Tijaabo");
    XaddidFps(60);

    inta ay (daaqadaMaXirantahay() == been) {
        bilowSawirka();
        nadiifiShaashada(MADOW);
        
        sawirGoobo(400.0, 300.0, 50.0, CAGAAR);
        qoraalKuQor("Tusmo waa cajiib!", 250, 400, 30, CAD);
        
        dhameeySawirka();
    }
    xirDaaqada();
}

main();
```

## Sida Loo Isticmaalo (Usage)
Si aad ugu shaqeysiiso koodkaaga Tusmo, fur Terminal-ka oo ku qor:
```bash
tusmo magaca_faylkaaga.tus
```

## Faylasha Halkan Ku Jira (Repository Structure)
- `/compiler` – Maskaxda luuqadda: Qaybta turjumeysa (Transpiler) iyo falanqeeyaha naxwaha.
- `/runtime` – Koodka C ee asalka u ah Tusmo, xakameynaya xusuusta, tixaha (arrays), qaamuusyada (dictionaries), iyo I/O.
- `/stdlib` – Maktabadaha caadiga ah ee Tusmo (Sida Raylib, OS, HTTP, WebSockets).
- `/Extension` – VS Code Extension-ka ee rasmiga ah oo ay ku jirto *Tusmo Language Server Protocol (LSP)*.
-beddelayn (Constants/Macros), isticmaal `qeex`. Tani xawaaraha ayay badisaa maxaa yeelay toos ayaa loogu beddelaa C.

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

## Tusaale Degdeg ah (Quick Example)
Halkan waa tusaale fudud oo muujinaya daaqad ciyaar oo raylib ah:

```tus
keen "stdlib/raylib/core";

qeex BALLAC = 800;
qeex DHEER = 600;

hawl main(): waxbo {
    bilowDaaqada(BALLAC, DHEER, "Tusmo Raylib Tijaabo");
    XaddidFps(60);

    inta ay (daaqadaMaXirantahay() == been) {
        bilowSawirka();
        nadiifiShaashada(MADOW);
        
        sawirGoobo(400.0, 300.0, 50.0, CAGAAR);
        qoraalKuQor("Tusmo waa cajiib!", 250, 400, 30, CAD);
        
        dhameeySawirka();
    }
    xirDaaqada();
}

main();
```

## Sida Loo Isticmaalo (Usage)
Si aad ugu shaqeysiiso koodkaaga Tusmo, fur Terminal-ka oo ku qor:
```bash
tusmo.py magaca_faylkaaga.tus
```

## Faylasha Halkan Ku Jira (Repository Structure)
- `/compiler` – Maskaxda luuqadda: Qaybta turjumeysa (Transpiler) iyo falanqeeyaha naxwaha.
- `/runtime` – Koodka C ee asalka u ah Tusmo, xakameynaya xusuusta, tixaha (arrays), qaamuusyada (dictionaries), iyo I/O.
- `/stdlib` – Maktabadaha caadiga ah ee Tusmo (Sida Raylib, OS, HTTP, WebSockets).
- `/Extension` – VS Code Extension-ka ee rasmiga ah oo ay ku jirto *Tusmo Language Server Protocol (LSP)*.
