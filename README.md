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
tusmo.py magaca_faylkaaga.tus
```

## Faylasha Halkan Ku Jira (Repository Structure)
- `/compiler` – Maskaxda luuqadda: Qaybta turjumeysa (Transpiler) iyo falanqeeyaha naxwaha.
- `/runtime` – Koodka C ee asalka u ah Tusmo, xakameynaya xusuusta, tixaha (arrays), qaamuusyada (dictionaries), iyo I/O.
- `/stdlib` – Maktabadaha caadiga ah ee Tusmo (Sida Raylib, OS, HTTP, WebSockets).
- `/Extension` – VS Code Extension-ka ee rasmiga ah oo ay ku jirto *Tusmo Language Server Protocol (LSP)*.
