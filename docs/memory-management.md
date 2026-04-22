# Maareynta Xusuusta ee Tusmo (Memory Management)

Tusmo waa luqad loogu talagalay xawaaraha ugu sarreeya ee suurtagal ah. Si loo gaaro xawaarahaas, Tusmo ma isticmaasho Garbage Collector (GC), ee waxay isticmaashaa nidaamka **Ownership Tracking** (Raad-raaca Milkiyadda).

---

## 1. Mishiinka "GC-Free"
Dhammaan qaybihii ay Tusmo kaga tiirsanayd maktabadda Boehm GC waa laga saaray. Hadda luqaddu waxay si toos ah ula xiriirtaa xusuusta mishiinka (Hardware) iyadoo isticmaalaysa `malloc` iyo `free` si "Silent" ah.

### Faa'iidada:
*   **Speed:** Ma jiro barnaamij istaagaya si uu xusuus u nadiifiyo.
*   **Independence:** Barnaamijka Tusmo wuxuu hadda ordi karaa PC kasta isagoon u baahnayn maktabado dheeraad ah.
*   **Legacy Speed:** Tusmo waxay hadda xawaare ahaan bar-bardhigi kartaa ama ka dheerayn kartaa C iyo Rust.

---

## 2. Xeerarka Milkiyadda (Ownership & Move)

Xog kasta oo weyn (Heap data) waxay leedahay hal milkiile. Markaad xogtaas siiso variable kale, milkiilihii hore wuu dhimanayaa.

### Tusaale:
```tusmo
hawl tijaabo() {
    keyd:tix:tiro a = [1, 2, 3]; // 'a' ayaa leh xogtan
    keyd:tix:tiro b = a;         // MILKIYADDII waxay u wareegtay 'b' (Move)

    qor(b); // SAX
    qor(a); // KHALAD! 'a' waa dhimatay gacantaada.
}
```

---

## 3. TUSMO_XIDID (Auto Linker)

Haddii aad rabto inaad Tusmo ku dhex isticmaasho kood C ah oo aad horay u dhisatay, waxaad isticmaalaysaa keyword-ka **`TUSMO_XIDID`**.

### Sida loo isticmaalo:
```tusmo
TUSMO_XIDID ".lib/libmymath"; // Wuxuu si otomaatig ah u link-garaynayaa libmymath.a ama .lib

hawl xisaabi(x: tiro) => tiro {
    soo_celi ___c__call_("my_c_math_function", x);
}
```

---

## 4. Tracing Logic (Sidee xusuusta loo nadiifiyaa?)

Compiler-ka Tusmo ayaa baaraya koodkaaga ka hor intaan la bilaabin. Wuxuu ogaanayaa meesha ugu dambaysa ee variable kasta loobaahan yahay, ka dibna isagaa si aamusan ugu daraya amarka xoreynta (`free`).

### Tusaale:
```tusmo
hawl salaan() {
    keyd:eray magac = "Somaaliya"; 
    qor(magac);
} // Compiler-ka ayaa halkan ku daraya free(magac) isagoon la arkin.
```

---

## 5. Summary: Maxay Tusmo kaga dheeraysaa Rust?

Tusmo waxay xawaaraheeda 6-laabka ah ku gaartay:
1.  **Static Bounds Check:** Inay iska saartay hubinta xadadka ee rari jirtay Processor-ka.
2.  **Manual Memory Injection:** Inay xusuusta u nadiifiso si la mid ah C-da laakiin si otomaatig ah.
3.  **Low-Level Linking:** Isticmaalka `TUSMO_XIDID` oo si toos ah u xididaya koodka C-da oo dhammaystiran.
