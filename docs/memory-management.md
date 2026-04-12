# Maareynta Xusuusta ee Tusmo (Memory Management)

Tusmo waxay isticmaashaa nidaam casri ah oo loo yaqaanno **Ownership Tracking** (Raad-raaca Milkiyadda) si ay u maareyso xusuusta PC-ga (RAM). Nidaamkani wuxuu ka dhigayaa barnaamijka mid aad u dheereeya, isla markaana ammaan ah, isagoo ka hortagaya in xusuustu ay buuxsanto ama barnaamijku u crash-gareeyo si lama filaan ah.

---

## 1. Stack vs Heap (Xusuusta Fudud iyo Tan Culus)

Luqadda Tusmo waxay u qaybisaa xogta labo meelood:

*   **Stack (Xusuusta Tooska ah):** Halkan waxaa lagu kaydiyaa xogta fudud ee cabbirkeeda la yaqaan (sida `tiro`, `jajab`, `xaraf`, iyo `miyaa`). Processor-ka ayaa si otomaatig ah u xoreeya xogtan isla marka ay dhammaato hawsha (function) ay ku dhex jirtay.
*   **Heap (Xusuusta weyn):** Halkan waxaa lagu kaydiyaa xogta cabbirkeedu isbeddelo (sida `tix`, `eray`, `qaamuus`, iyo `koox`). Xogtan waxay u baahan tahay in si taxadar leh loo maareeyo waayo si otomaatig ah u dhiman mayso.

---

## 2. Xeerarka Milkiyadda (Ownership Rules)

Si Tusmo ay u noqoto mid "Silent" ah (oo aan user-ka ka dalban inuu manual ahaan u xoreeyo xusuusta), waxay raacdaa xeerarkan:

1.  **Halkan Milkiile:** Xog kasta oo Heap-ka lagu dhex dhisay, waxaa leh hal Variable oo kaliya oo loo yaqaanno "Owner" (Milkiile).
2.  **Wareejin (Move):** Haddii xogta loo dhiibo Variable kale, Milkiilihii hore wuu dhimanayaa, mana isticmaali karo xogtaas mar kale.
3.  **Xoreyn Otomaatig ah:** Isla marka uu Milkiiluhu gaaro meesha ugu dambaysa ee koodka looga baahnaa, Compiler-ka ayaa si otomaatig ah u xoreynaya xogtaas (`free`).

---

## 3. Tracing (Raad-raaca Cimriga Variable-ka)

Compiler-ka Tusmo wuxuu leeyahay mishiin la yiraahdo **Lifetime Tracker**. Isagu wuxuu koodka u akhriyaa qaab "Bottom-up" (hoos ilaa kor) si uu u ogaado halka uu Variable kasta ku dhimanayo.

### Tusaale:
```tusmo
hawl salaan() {
    keyd:eray magac = "Tusmo"; // 1. Xogta ayaa dhalatay (Heap)
    qor(magac);                // 2. Markii ugu dambaysay ee la isticmaalo
}                              // 3. Compiler-ka ayaa halkan ku daraya free(magac)
```

### Haddii xogta la "soo celiyo" (Return):
```tusmo
hawl hel_xog() : tix {
    keyd:tix t = [1, 2];
    soo_celi t; // Milkiyaddii waxaa la wareegaya qofka u yeeray hawshan (Handoff)
}
```

---

## 4. Faa'iidooyinka

1.  **Xawaare sare:** Ma jiro Garbage Collector (GC) oo barnaamijka joojinaya si uu xusuusta u nadiifiyo.
2.  **Badbaado:** Waxaad ka badbaadaysaa **Memory Leaks** (RAM-ka oo buuxsama) iyo **Segfaults** (Crash).
3.  **Fududaan:** User-ku uma baahna inuu qoro `free()` ama `delete`, koodkiisuna wuxuu u muuqdaa mid nadiif ah.

---

## 5. Tracing Logic (Sidee Compiler-ku u shaqeeyaa?)

1.  **AST Analysis:** Compiler-ku wuxuu dhex maraa geedka koodka (Abstract Syntax Tree).
2.  **Dependency Map:** Wuxuu dhisayaa liis ay ku qoran yihiin dhammaan meelaha variable kasta lagu magacaabay.
3.  **Last-Use Detection:** Wuxuu calaamadeeyaa meesha ugu dambaysa ee Variable-ka la isticmaalo.
4.  **C-Code Injection:** Marka uu koodka u beddelayo C, wuxuu dhex gelinayaa amarka `free()` isla marka laga gudbo meeshii ugu dambaysay.
