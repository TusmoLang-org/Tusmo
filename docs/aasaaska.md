# Aasaaska Luuqada (Language Basics)

Boggan wuxuu si faahfaahsan u sharraxayaa naxwaha aasaasiga ah ee luuqadda **Tusmo**—sida loo qeexo keydiyayaasha, loo maareeyo noocyada xogta, loo hago socodka koodhka (Control Flow), iyo sidee loo dhiso hawlaha (functions).

---

## Variable & Constants (Keydiyaha iyo Qeexiyaha)

Si xog loo kaydiyo, luuqadda Tusmo waxay adeegsataa laba erey-fure oo muhiim ah:

1. **Keydiyaha (Variable)**: Waxaa lagu abuuraa ereyga `keyd`. Koodhka dhexdiisa, qiimaha ku jira keydiyaha waa la beddeli karaa hadhow.
2. **Qeexiyaha (Constant)**: Waxaa lagu abuuraa ereyga `qeex`. Qiimaha qeexiyaha waa mid go'an oo aan la beddeli karin barnaamijka oo dhan ka dib marka la qeexo.

### 1. Qeexidda Keydiyaha (`keyd`)
Hab-dhaqanka qeexidda keydiyaha waa: `keyd:nooca_xogta magaca_keydiyaha = qiimaha;`

Tusaale:
```tusmo
// Qeexidda keydiyaha magaciisu yahay "da'da" oo kaydinaya tiro
keyd:tiro da_da = 25;

// Beddelidda qiimaha keydiyaha
da_da = 26; // Waa la oggol yahay sababtoo ah waa keyd
```

### 2. Qeexidda Qeexiyaha (`qeex`)
Hab-dhaqanku waa: `qeex:nooca_xogta MAGAC_GOAN = qiimaha;`

Tusaale:
```tusmo
// Qeexidda qiimaha Pi oo go'an (constant)
qeex:jajab PI = 3.14159;

// PI = 3.14; // Qalad! Compiler-ku wuxuu keenayaa cilad sababtoo ah PI waa qeexiye
```

---

## Noocyada Xogta (Data Types)

Tusmo waa luuqad **statically typed** ah, taas oo macnaheedu yahay in keydiyaha kasta la ogyahay nooca xogta uu kaydinayo ka hor inta aan koodhka la socodsiin. Luuqaddu waxay leedahay 5 nooc oo aasaasi ah (Primitives):

| Nooca Xogta | Sharaxaad | Tusaale |
| :--- | :--- | :--- |
| `tiro` | Tirooyinka idil (integers) oo togan ama taban | `keyd:tiro x = -5;` |
| `jajab` | Tirooyinka leh dhibcaha jajabka ah (double precision float) | `keyd:jajab y = 19.99;` |
| `eray` | Qoraalka caadiga ah ee xigashada labanlaabka ah ku dhex jira (strings) | `keyd:eray magac = "Faadumo";` |
| `miyaa` | Qiimaha runta ah ama been abuurka ah (boolean: `run` ama `been`) | `keyd:miyaa waa_diyaar = run;` |
| `xaraf` | Hal xaraf oo kaliya oo ku dhex jira xigashada kelida ah (char) | `keyd:xaraf fasal = 'A';` |

---

## Socodka Koodhka (Control Flow)

Tusmo waxay leedahay nidaamyo awood badan oo lagu xakameeyo socodka koodhka iyadoo la adeegsanayo shuruudo iyo wareegyo (loops).

### 1. Shuruudaha (`haddii`, `ama_haddii`, `haddii_kale`)
Si aad go'aan u gaarto adigoo ku xiraya shuruudo gaar ah:

```tusmo
keyd:tiro dhibcaha = 85;

haddii (dhibcaha >= 90) {
    qor("Darajadaada waa A!");
} ama_haddii (dhibcaha >= 80) {
    qor("Darajadaada waa B!");
} haddii_kale {
    qor("Waxaad u baahantahay inaad dadaasho sxb.");
}
```

*Fiiro gaar ah: Ereyga `haddii_kale` waxaa kale oo loo qori karaa si kooban oo ah `kale`:*
```tusmo
haddii (darajo == 100) {
    qor("Ugu sarreeya!");
} kale {
    qor("Waa caadi.");
}
```

### 2. Wareegyada (Loops)
Wareegyada waxaa loo adeegsadaa in koodh la soo celceliyo dhowr jeer.

#### A. Loop-ka `inta ay` (While Loop)
Wuxuu shaqaynayaa inta ay shuruuddu run tahay:

```tusmo
keyd:tiro kow = 1;

inta ay (kow <= 5) {
    qor("Tirada hadda waa: ", kow);
    kow = kow + 1; // Kor u qaad
}
```

#### B. Loop-ka `soco...laga bilaabo` (For Loop)
Wuxuu ku habboon yahay marka aad garanayso inta jeer ee loop-ku ordi doono:

```tusmo
// For loop: Orod 1 ilaa 5
soco keyd:tiro i laga bilaabo 1 ilaa 5 {
    qor("Wareegga: ", i);
}
```

---

## Hawlaha (Functions)

Hawluhu waxay kuu sahlayaan inaad koodhkaaga u kala jebiso qaybo yaryar oo dib loo isticmaali karo. Waxaa lagu qeexaa ereyga `hawl`.

### Hab-dhaqanka:
```tusmo
hawl magaca_hawsha(param1: nooc, param2: nooc) : nooca_soo_celinta {
    // Koodhka shaqada
    soo_celi qiimaha;
}
```

### Tusaale 1: Hawl soo celinaysa qiime
```tusmo
// Hawl isku daraysa laba tiro
hawl isku_dar(a: tiro, b: tiro) : tiro {
    soo_celi a + b;
}

hawl main() : waxbo {
    keyd:tiro wadajir = isku_dar(10, 20);
    qor("Wadarta waa: ", wadajir);
}
```

### Tusaale 2: Hawl aan waxba soo celinayn (`waxbo` / void)
```tusmo
hawl salaam(magac: eray) : waxbo {
    qor("Haye, ", magac, "! Ku soo dhawaow luuqadda Tusmo.");
}
```

### Tusaale 3: Hawl leh Parameters leh Default Values
Tusmo waxay kuu sahlaysaa inaad siiso parameters-ka qiime diyaarsan haddii aan la soo dirin:

```tusmo
hawl xisaabi_qiime(qiime: tiro, canshuur: jajab = 0.05) : jajab {
    soo_celi qiime + (qiime * canshuur);
}
```

---

## Faallooyinka (Comments)

Faallooyinka waa qoraal sharraxaad ah oo la geliyo koodhka gudihiisa si qofka akhriyaya u fahmo, laakiin compiler-ku ma socodsiiyo.

```tusmo
// Kani waa faallo hal sadar ah (Single-line comment)

/* 
   Kani waa faallo dhowr sadar ah 
   oo lagu sharraxi karo algorithms 
   aad u adag (Multi-line comment).
*/
```

Hadda waxaad baratay aasaaska laf-dhabarta ah ee luuqadda! U gudub bogga xiga ee **Heerka Sare** si aad u barato nidaamka Classes-ka, Memory Safety-ga, iyo Lambdas.
