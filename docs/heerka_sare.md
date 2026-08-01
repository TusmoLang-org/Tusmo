# Heerka Sare (Advanced Concepts)

Boggan wuxuu ku saabsan yahay nidaamyada iyo astaamaha heerka sare ah ee luuqadda **Tusmo**—sida dhisidda fasallada (Classes), qaab-dhismeedka xogta (Structs), shaqooyinka aan magaca lahayn (Lambdas), maamulka xusuusta ee automatic-ga ah (Memory Management), iyo sida ay luuqaddu u maamusho badbaadada koodhka (Memory Safety).

---

## Object-Oriented Coding (OOP)

Tusmo waxay si buuxda u taageertaa habka casriga ah ee u-habaynta walxaha (Object-Oriented Programming). Waxay leedahay laba qaab oo loo dhiso xogta:

### 1. Qaab-dhismeedka Fudud (`qaab` - Struct)
`qaab` waxaa loo adeegsadaa in lagu ururiyo dhowr xogood oo isku xiran laakiin aan lahayn methods ama hab-dhaqan adag. Waa mid fudud oo xusuusta ku kaydsan si toos ah (stack-allocated).

```tusmo
qaab Boos {
    keyd:tiro x;
    keyd:tiro y;
}

hawl main() : waxbo {
    keyd:Boos b;
    b.x = 10;
    b.y = 20;
    qor("Barta booska: x =", b.x, ", y =", b.y);
}
```

### 2. Fasallada Casriga ah (`koox` - Class)
`koox` waa laf-dhabarta OOP ee Tusmo. Waxay yeelan kartaa sifooyin (properties/fields) ku bilowda `keyd`, dhiseyaal (constructors) lagu magacaabo `dhis`, iyo shaqooyin dhex-dhisan (methods) oo lagu magacaabo `shaqo` ama `hawl`.

*Fiiro gaar ah: Dhexdeeda, fasalku wuxuu u isticmaalaa erey-furaha **`kan`** si uu u tilmaamo naftiisa (oo u dhiganta `this` ama `self` ee luuqadaha kale).*

```tusmo
koox Qof {
    keyd:eray Magac;
    keyd:tiro Da;

    // Dhisaha (Constructor)
    dhis(m: eray, d: tiro) : waxbo {
        kan.Magac = m;
        kan.Da = d;
    }

    // Shaqo (Method)
    shaqo isbar() : waxbo {
        qor("Magacaygu waa ", kan.Magac, ", waxaan jiraa ", kan.Da, " sano.");
    }
}

hawl main() : waxbo {
    // Abuurista shay cusub oo class ah adoo adeegsanaya "cusub"
    keyd:Qof macmiil = Qof("Axmed", 30) cusub;
    macmiil.isbar(); // Wuxuu daabacayaa isbarashada
}
```

### 3. Dhaxalka (`dhaxlaya` & `waalid`)
Classes-ka ku jira Tusmo waxay dhaxli karaan fasallo kale adigoo isticmaalaya ereyga **`dhaxlaya`**. Si aad u wacdo dhisaha ama methods-ka fasalka sare (base class), waxaad adeegsaneysaa ereyga **`waalid`**.

```tusmo
koox Shaqaale dhaxlaya Qof {
    keyd:jajab Mushaar;

    dhis(m: eray, d: tiro, mush: jajab) : waxbo {
        // Wac dhisaha class-ka sare (base constructor)
        waalid.dhis(m, d);
        kan.Mushaar = mush;
    }

    shaqo faahfaahin() : waxbo {
        qor("Shaqaale: ", kan.Magac, ", Mushaar: $", kan.Mushaar);
    }
}
```

---

## Functional Concepts: Lambdas (Shaqooyinka Anonymous)

Tusmo waxay taageertaa dynamic arrow lambdas iyo shaqooyinka anonymous-ka ah si fudud:

### 1. Arrow Lambdas (`=>`)
Waa shaqooyin kooban oo hal sadar ah oo si toos ah loo qeexi karo:

```tusmo
// Qeexidda lambda labanlaabaysa tirada
keyd:hawl(tiro):tiro labanlaab = (x: tiro) => x * 2;
qor("Labanlaabka 5 waa: ", labanlaab(5));
```

### 2. Block Lambdas
Waa shaqooyin anonymous ah oo leh koodh ka kooban dhowr sadar oo ku dhex jira billaha `{}`:

```tusmo
keyd:hawl(tiro, tiro):tiro xisaabi = (a: tiro, b: tiro) => {
    keyd:tiro natiijo = a * b + 10;
    soo_celi natiijo;
};
```

---

## Memory Safety & Move Semantics (Maamulka Xusuusta)

Tusmo waxay leedahay mid ka mid ah nidaamyada ugu casrisan ee maamulka xusuusta (Memory Management) ee luuqadaha compiler-ka ah:

### 1. Ma jiro Garbage Collector (GC-Free)
Luuqadaha leh GC (sida Java, Python) waxay leeyihiin barnaamij gadaal ka orda oo mar walba iska baara memory-ga si uu u nadiifiyo, taas oo gaabinaysa xawaaraha barnaamijka. Tusmo ma laha wax GC ah, sidaas darteed xawaaraheedu waa kan ugu sarreeya ee suurtogalka ah.

### 2. Ownership & Automatic Scope Cleanup
Sidee Tusmo u xallisaa memory leaks-ka haddii uusan jirin GC? 
Compiler-ka Tusmo wuxuu si toos ah ula socdaa keydiyaasha leh noocyada u baahan dynamic memory allocation (sida `eray`, `tix` (arrays), `qaamuus`, iyo walxaha `koox` (classes) ee loo dhisay `cusub`). 

Marka uu barnaamijku ka baxo scope-ka uu ku jiro keydiyaha (sida dhamaadka shaqada ama loop-ka dhexdiisa), compiler-ka Tusmo wuxuu si toos ah u dhalinayaa (injects) koodh C ah oo lagu xoreynayo xusuusta (`free` functions).

```tusmo
hawl tijaabo() : waxbo {
    // Memory allocation wuxuu ka dhacaa C heap-ka
    keyd:eray qoraal_dheer = "Tani waa xog dynamic ah...";
    qor(qoraal_dheer);
    
    // scope cleanup: Marka barnaamijku halkan soo gaaro,
    // compiler-ku wuxuu si toos ah u dhalinayaa: tusmo_free_eray(qoraal_dheer);
}
```

### 3. Move Semantics (Wareejinta Lahaanshaha)
Markaad keydiyaha dynamic-ga ah u wareejiso keydiyaha kale, lahaanshaha (ownership-ka) xogtaas wuxuu u guurayaa keydiyaha cusub, kii horena wuxuu noqonayaa `NULL` si looga fogaado **double-free errors**:

```tusmo
keyd:eray a = "Xog muhiim ah";
keyd:eray b = a; // Lahaanshuhu wuxuu u guuray b, a hadda waa NULL!

qor(b); // Waa sax
// qor(a); // Qalad! Compiler-ka Tusmo wuxuu soo saarayaa cilad sababtoo ah 'a' hadda lahaansho ma laha.
```

---

## Maareynta Khaladaadka (Error Handling)

Tusmo waxay leedahay badbaado adag oo la xiriirta khaladaadka socodka barnaamijka (Runtime Errors):

1. **Semantic Safety**: Compiler-ka Tusmo wuxuu ka hortagaa khaladaadka ka hor inta aan barnaamijka la isku-dubin (compilation time). Tusaale ahaan, haddii aad isku daydo inaad isticmaasho keyd aan la qeexin ama aad qiimo khaldan siiso keyd gaar ah, compiler-ku wuxuu ku siinayaa fariin Af-Soomaali ah oo aad u cad.
2. **Bounds Checking (Badbaadada Tixaha)**: Haddii aad isku daydo inaad wax ka akhriso boos (index) aan ku jirin tixda (array out of bounds), Tusmo ma dhiseyso wax dhalinaya crash qarsoon (buffer overflow). Waxay si toos ah u daabacaysaa fariin runtime error oo Af-Soomaali ah oo muujinaysa line-ka iyo faylka saxda ah ee dhibtaadu ka dhacday.
3. **Null Pointer Protection**: Dhammaan wicitaannada dynamic-ga ah waxaa lagu ilaaliyaa macros caalami ah (`TUSMO_SAFE_ACCESS`) si haddii shay uu yahay `NULL` uu barnaamijku si nabad ah ugu istaago halkii uu ka dhici lahaa segmentation fault.

Hadda waxaad taqaanaa dhammaan siraha heerka sare ah ee Tusmo! U gudub bogga **Maktabadda Caadiga ah** si aad u aragto dhammaan maktabadaha diyaarka ah ee kuu qoran ee aad isla gujinta kowaadba isticmaali karto.
