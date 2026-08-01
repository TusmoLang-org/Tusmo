# Maktabadda Caadiga ah (Standard Library & API Reference)

Tusmo waxay la timaadaa maktabad aad u qani ah oo laguu diyaariyay si aad u dhisid barnaamijyadaada adigoon dibadda uga baahnayn maktabado kale. Dhammaan maktabadaha waxaa lagu soo dhex gashan karaa erey-furaha **`keen`** (sida: `keen "os";`).

---

## 1. Hawlaha Dhex-dhisan ee Laf-dhabarta ah (`core.tus`)

Kuwani waa shaqooyin caalami ah (global functions) oo si toos ah loo waci karo iyada oo aan loo baahnayn in la `keen`-gareeyo wax module ah:

### `nooc(x: walbo) : eray`
Waxay soo celisaa nooca xogta ee keydiyaha ama qiimaha loo soo diro.
```tusmo
qor(nooc(15));       // "tiro"
qor(nooc("haye"));   // "eray"
qor(nooc(run));      // "miyaa"
```

### `dherer(x: walbo) : tiro`
Waxay soo celisaa tirada xarfaha ku jira `eray` ama tirada walxaha ku jira `tix` (array).
```tusmo
keyd:eray s = "soomaali";
qor(dherer(s)); // 8
```

### Noocyada Beddelaada (Type Casting)
Tusmo waxay kuu sahlaysaa inaad xogta u beddesho noocyo kale:
* `eray(x: walbo) : eray` — U beddel xog kasta dhanka qoraalka.
* `tiro(x: walbo) : tiro` — U beddel xog kasta dhanka tirada (integer).
* `jajab(x: walbo) : jajab` — U beddel xog kasta dhanka jajabka (double).
* `miyaa(x: walbo) : miyaa` — U beddel xog kasta dhanka boolean (`run`/`been`).

```tusmo
keyd:eray s = "123";
keyd:tiro t = tiro(s); // Hadda waa nambarka 123
```

### ASCII Conversion
* `qor_tiro(x: xaraf) : tiro` — Waxay soo celisaa lambarka ASCII ee xarafka la siiyo.
* `qor_xaraf(x: tiro) : xaraf` — Waxay lambarka ASCII u beddeshaa xaraf.

```tusmo
keyd:tiro ascii_val = qor_tiro('A'); // 65
keyd:xaraf char_val = qor_xaraf(65); // 'A'
```

### `jooji(code: tiro) : waxbo`
Waxay si toos ah u joojisaa socodsiinta barnaamijka iyadoo la adeegsanayo exit code-ka la siiyo.
```tusmo
jooji(0); // Barnaamijku wuxuu u istaagayaa si guul ah
```

---

## 2. Hawlaha Erayga, Tixaha iyo Qaamuusyada

### A. Erayga (`eray.tus`)
Shaqooyinkan waxaa loo isticmaalaa in lagu maareeyo qoraalka (strings):
* `XarafWeyn(s: eray) : eray` — U beddel dhammaan qoraalka xarfo waaweyn.
* `XarafYar(s: eray) : eray` — U beddel dhammaan qoraalka xarfo yaryar.
* `kaReeb(s: eray) : eray` — Ka saar meelaha bannaanka ah (spaces) ee bilowga iyo dhammaadka.
* `Bkareeb(s: eray) : eray` — Trim bilowga qoraalka kaliya.
* `Mkareeb(s: eray) : eray` — Trim dhammaadka qoraalka kaliya.
* `kuBadal(s: eray, doq: eray, cusub: eray) : eray` — Ku beddel erey kasta oo `doq` ah ereyga `cusub`.
* `sooRaadi(s: eray, target: eray) : tiro` — Wuxuu soo celinayaa index-ka ugu horreeya ama `-1`.
* `lagaHelay(s: eray, target: eray) : miyaa` — Hubi in qoraalka uu ku dhex jiro.
* `qaybi(s: eray, delimiter: eray) : tix:eray` — Qaybi qoraalka adoo adeegsanaya xaraf delimiter ah.

```tusmo
keyd:eray heesta = "Tusmo waa luuqad cajiib ah";
keyd:tix:eray ereyada = qaybi(heesta, " ");
// ereyada[0] hadda waa "Tusmo"
```

### B. Tixaha (Arrays - methods)
Tixaha ama arrays-ka waxay leeyihiin methods dhex-dhisan oo lagu maareeyo walxaha ku jira:
* `.gali(value)` — Ku dar walax cusub dhammaadka tixda.
* `.gali(boos, value)` — Geli walax cusub index gaar ah (insert).
* `.kasaar(boos=index)` — Ka saar walaxda ku jirta index-ka (pop).
* `.kasaar(value)` — Ka saar walaxda leh qiimahaas (remove).

```tusmo
keyd:tiro[] tixda = [10, 20, 30];
tixda.gali(40); // Hadda waa [10, 20, 30, 40]
tixda.gali(boos=1, 15); // Hadda waa [10, 15, 20, 30, 40]
tixda.kasaar(boos=0); // Hadda waa [15, 20, 30, 40]
tixda.kasaar(30); // Hadda waa [15, 20, 40]
```

### C. Qaamuusyada (`qaamuus.tus`)
Markaad isticmaalayso qaamuuska (`qaamuus` type), waxaad adeegsan kartaa:
* `majiraa(q: qaamuus, fure: eray) : miyaa` — Hubi in furahaas uu ku jiro qaamuuska.
* `tir(q: qaamuus, fure: eray) : waxbo` — Ka tirtir furahaas iyo qiimihiisa qaamuuska dhexdiisa.

```tusmo
keyd:qaamuus q = {"magac": "Maxamed", "da'": "22"};
haddii (majiraa(q, "magac")) {
    qor("Magacu waa: ", q["magac"]);
}
tir(q, "da'"); // Ka saar da'da
```

---

## 3. Maktabadaha Casriga ah (`stdlib/`)

### A. Wakhti (Time operations)
Ku soo dhex gasho: `keen "wakhti";`
Fasalka: **`Wakhti`**

#### Sifooyinka & Methods:
* `hadda() : eray` — Waqtiga hadda ee qaab akhris fudud (`YYYY-MM-DD HH:MM:SS`).
* `wakhti() : jajab` — Soo celi unix timestamp ee hadda (ilbiriqsiyo jajab ah).
* `qaabee(format: eray) : eray` — Qaabee waqtiga adigoo adeegsanaya standard strftime strings.
* `sekeno() : tiro` — Sekenada hadda (0-59).
* `daqiiqado() : tiro` — Daqiiqadaha hadda (0-59).
* `saacado() : tiro` — Saacadaha hadda (0-23).
* `maalin() : tiro` — Maalinta bisha (1-31).
* `bil() : tiro` — Bisha (1-12).
* `sanad() : tiro` — Sanadka buuxa (e.g., 2026).
* `seexo(sekeno: tiro) : waxbo` — Jooji orodka barnaamijka tirada ilbiriqsiyada ee la tilmaamay.

```tusmo
keen "wakhti";

hawl main() : waxbo {
    keyd:Wakhti w = Wakhti() cusub;
    qor("Waqtiga hadda: ", w.hadda());
    qor("Sanadka: ", w.sanad());
    
    qor("Waxaan seexanayaa 2 ilbiriqsiyo...");
    w.seexo(2);
    qor("Waan soo toosay!");
}
```

### B. Xisaab (Math Library)
Ku soo dhex gasho: `keen "xisaab";`
Fasalka: **`Xisaab`**

#### Methods:
* `la_sin(x: jajab) : jajab` — Sin-ta xisaabta.
* `la_cos(x: jajab) : jajab` — Cos-ka xisaabta.
* `la_sqrt(x: jajab) : jajab` — Square root-ka (xidid labajibbaaran).
* `la_abs(x: jajab) : jajab` — Absolute value.
* `la_pow(base: jajab, exp: jajab) : jajab` — Awoodda tiro kale ku saaran tahay.
* `la_floor(x: jajab) : jajab` — Hoos u dhig jajabka tirada ugu dhow.
* `la_ceil(x: jajab) : jajab` — Sare u qaad jajabka tirada ugu dhow.
* `la_round(x: jajab) : jajab` — Wareeji jajabka tirada ugu dhow.

```tusmo
keen "xisaab";

hawl main() : waxbo {
    keyd:Xisaab math = Xisaab() cusub;
    qor("Xididka 16 waa: ", math.la_sqrt(16.0));
    qor("Floor 4.7 waa: ", math.la_floor(4.7));
}
```

### C. Nasiib (Random Library)
Ku soo dhex gasho: `keen "nasiib";`

#### Shaqooyinka:
* `bilaab_nasiib() : waxbo` — Diyaari nasiibka (initializes random seed using time).
* `nasiib_tiro(ugu_yaraan: tiro, ugu_badnaan: tiro) : tiro` — Soo saar tiro random ah oo u dhaxaysa tiradaas.
* `nasiib_jajab(ugu_yaraan: jajab, ugu_badnaan: jajab) : jajab` — Soo saar jajab random ah oo u dhexeeya.

```tusmo
keen "nasiib";

hawl main() : waxbo {
    bilaab_nasiib(); // Waa in la waco mar kaliya marka la bilaabayo
    keyd:tiro lambar = nasiib_tiro(1, 100);
    qor("Tirada nasiibka ee 1 ilaa 100 waa: ", lambar);
}
```

### D. Nidaamka Os (System and File I/O)
Ku soo dhex gasho: `keen "os";`
Fasalka: **`Os`**

Maktabaddani waxay leedahay **19 shaqo** oo awood badan oo lagu xakameeyo faylalka iyo nidaamka kumbuyuutarka:

* `halkee() : eray` — Soo celi folder-ka aad hadda ku sugantahay (Current Working Directory).
* `u_guur(folder_path: eray) : waxbo` — Ka bax folderka aad joogto, aad folder kale (CD).
* `itus(folder_path: eray) : tix:eray` — Soo celi liiska faylasha iyo folder-da ku jira.
* `abuur_folder(path: eray) : waxbo` — Abuur gal cusub.
* `tirtir_folder(path: eray) : waxbo` — Ka saar gal madhan oo jira.
* `tirtir_fayl(path: eray) : waxbo` — Tirtir fayl gaar ah.
* `majiraa(path: eray) : miyaa` — Hubi in fayl ama gal uu jiro.
* `fayl_miyaa(path: eray) : miyaa` — Hubi inuu yahay fayl caadi ah.
* `folder_miyaa(path: eray) : miyaa` — Hubi inuu yahay gal.
* `hel_deegaan(name: eray) : eray` — Akhriso qiimaha environment variable (ENV).
* `deji_deegaan(name: eray, value: eray) : waxbo` — Deji qiime cusub oo ENV ah.
* `fuli(command: eray) : tiro` — Orod amar shell ah (terminal command) oo soo celi exit code-ka.
* `koobi(source: eray, destination: eray) : waxbo` — Nuqul faylka kuna kaydi meel kale.
* `u_dhaqaaji(old_path: eray, new_path: eray) : waxbo` — Dhaqaaji ama magac-beddel fayl/gal.
* `aqri_fayl(path: eray) : eray` — Soo celi dhammaan qoraalka ku jira faylka.
* `qor_fayl(path: eray, content: eray, append: miyaa) : waxbo` — Qor xog ku dhex jirta faylka; ku dar haddii append==run.
* `isku_dar_waddo(part1: eray, part2: eray) : eray` — Ku dar laba qaybood si aad u hesho waddo buuxda (path join).
* `cabbir_fayl(path: eray) : tiro` — Soo celi cabbirka faylka (bytes).
* `nidaamkee() : eray` — Soo celi magaca OS-ka (`linux`, `windows`, `macos`).

```tusmo
keen "os";

hawl main() : waxbo {
    keyd:Os system = Os() cusub;
    
    // Qorista fayl
    system.qor_fayl("tusmo.txt", "Tusmo waa luuqad cajiib ah!", been);
    
    // Akhrinta fayl
    haddii (system.majiraa("tusmo.txt")) {
        keyd:eray xog = system.aqri_fayl("tusmo.txt");
        qor("Waxaa faylka ku qoran: ", xog);
    }
}
```

### E. Xiriiriye (TCP Sockets Network Library)
Ku soo dhex gasho: `keen "xiriiriye";`
Fasalka: **`Xiriiriye`**

Muuqaal ahaan wuxuu kuu sahlayaa dhisidda low-level TCP client/server applications:
* `samee_server(port: eray) : eray` — Samee server socket dhagaysanaya port gaar ah.
* `dhageyso(saf_sugid: tiro) : tiro` — Dhegeyso dadka kugu soo xirmaya.
* `aqbal() : Xiriiriye` — Aqbal oo abuur socket cusub ee ku soo xirme client ah.
* `kuxirmo(host: eray, port: eray) : eray` — Ku xirmo server meel kale ka ordaya.
* `dir(xog: eray) : tiro` — Ku dir xog socket-ka dhexdiisa.
* `soo_hel(size: tiro) : eray` — Ka soo hel (akhri) xog ka socota socket-ka.
* `xir() : waxbo` — Xir socket-ka.
* `waa_ansax() : miyaa` — Hubi haddii xiriiriye uu furan yahay.

---

### F. WebXiriiriye (WebSocket Protocol)
Ku soo dhex gasho: `keen "webxiriiriye";`
Fasalka: **`WebXiriiriye`**

Ku dhis real-time chat iyo adeegyo laba-dhinac leh (bi-directional sockets):
* `kor_u_qaad(client_socket_handle: eray, ws_key: eray) : waxbo` — Kor u qaad HTTP request una beddel WebSocket.
* `dir_qoraal(fariin: eray) : tiro` — Dir fariin qoraal ah.
* `dir_binary(xog: eray) : tiro` — Dir xog binary ah.
* `soo_hel_fariin() : qaamuus` — Soo hel fariin dhan, waxay soo celisaa qaamuus leh nooca iyo xogta.
* `xir(cod: tiro, sabab: eray) : waxbo` — Xir WebSocket-ka.
* `lagu_xirmay() : miyaa` — Hubi haddii loo xiran yahay.

---

### G. HTTP Protocol & Awr Framework (Web Framework)
Ku soo dhex gasho: `keen "awr";`
Fasalka: **`Awr`** (Sida Express.js ama FastAPI ee Soomaaliga ah)

Muuqaalkani wuxuu kuu sahlayaa inaad daqiiqad gudaheed ku abuurto server internet ah oo aad u dhakhso badan:

#### Methods:
* `doon(jidka: eray, maareeye: hawl(CodsiHttp):waxbo) : waxbo` — U deji GET route jid gaar ah.
* `dir(jidka: eray, maareeye: hawl(CodsiHttp):waxbo) : waxbo` — U deji POST route jid gaar ah.
* `jawaab(status: eray, content_type: eray, body: eray) : waxbo` — Dir jawaab HTTP ah.
* `kici(port: eray) : waxbo` — Kici oo bilow server-ka inuu dhagaysto port-gaas.

#### HTTP Request Object (`CodsiHttp`):
* `Method` — Nooca codsiga (`GET`, `POST`).
* `Jidka` — Jidka loo soo dhacay (e.g. `/`).
* `Jidhka` — Body-ga codsiga.
* `Madax` — Headers-ka (Dictionary).

```tusmo
keen "awr";

// Maareeyaha bogga hore
hawl bogga_hore(req: CodsiHttp) : waxbo {
    keyd:Awr server = Awr() cusub;
    server.jawaab("200 OK", "text/html; charset=utf-8", "<h1>Ku soo dhawaow Awr Framework!</h1>");
}

hawl main() : waxbo {
    keyd:Awr app = Awr() cusub;
    
    // Deji jidadka (routes)
    app.doon("/", bogga_hore);
    
    // Kici server-ka port-ka 8080
    app.kici("8080");
}
```

Halkan waxaad ku haysataa dukumiintiga rasmiga ah ee maktabadda qani-ga ah ee Tusmo! U guur bogga **Agabka & Deegaanka** si aad u aragto sida VS Code loogu rakibo dynamic extension-ka Tusmo.
