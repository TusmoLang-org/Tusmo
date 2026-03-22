# Module-ka HTTP

Module-ka HTTP wuxuu bixiyaa shaqada server-ka HTTP.

## Keenista (Import)

```tus
keen "http";
```

## Kooxda Http (Http Class)

Samee server HTTP ah.

```tus
keyd:Http server = Http() cusub;
```

### dhegeyso(port, handler)

Ku billow server-ka HTTP port cayiman.

```tus
hawl maamule(codsi: Codsi) : waxbo {
    qor("Codsiga: " + codsi.waddo());
    codsi.jawaab_caadi("<h1>Hello!</h1>");
}

server.dhegeyso("8080", maamule);
```

**Halbeegyada (Parameters):**
- `port` (eray) - Lambarka port-ka (tusaale, "8080")
- `maamule` (hawl) - Hawsha maareynaysa oo qaadanaysa shayga Codsi

---

### jooji()

Jooji server-ka.

```tus
server.jooji();
```

---

## Kooxda Codsi (Codsi Class)

Kooxda Codsi waxay ka dhigan tahay codsi HTTP ah. Waxaa loo gudbiyaa hawshaada maamulaha (handler function).

### hab()

Hel habka (method) HTTP.

```tus
keyd:eray habka = codsi.hab();
// Waxay soo celisaa: "HELID" (GET), "DHIGID" (POST), iwm.
```

**Soo-celinta:** `eray` - Habka HTTP

---

### waddo()

Hel wadada/URL-ka codsiga.

```tus
keyd:eray wadada = codsi.waddo();
// tusaale, "/api/users"
```

**Soo-celinta:** `eray` - Wadada codsiga

---

### xambaare()

Hel nuxurka (body) codsiga.

```tus
keyd:eray xambaare = codsi.xambaare();
```

**Soo-celinta:** `eray` - Nuxurka codsiga

---

### macmiil()

Hel cinwaanka IP-ga ee macmiilka (client).

```tus
keyd:eray macmiil = codsi.macmiil();
// tusaale, "192.168.1.100:12345"
```

**Soo-celinta:** `eray` - Cinwaanka macmiilka

---

### hel_madax(magac)

Hel qiimaha header-ka HTTP.

```tus
keyd:eray content_type = codsi.hel_madax("Content-Type");
keyd:eray user_agent = codsi.hel_madax("User-Agent");
```

**Halbeegyada:**
- `magac` (eray) - Magaca header-ka

**Soo-celinta:** `eray` - Qiimaha header-ka

---

### jawaab_eray(nuxur, xaalad, nooca_nuxurka)

Dir jawaab qoraal ah.

```tus
codsi.jawaab_eray("<h1>Hello</h1>", 200, "text/html; charset=utf-8");
```

**Halbeegyada:**
- `nuxur` (eray) - Nuxurka jawaabta
- `xaalad` (tiro) - Code-ka xaaladda HTTP (tusaale, 200, 404)
- `nooca` (eray) - Nooca MIME (tusaale, "text/html")

---

### jawaab(data, xaalad, nooca_nuxurka)

Dir jawaab JSON ah.

```tus
keyd:qaamuus json_data = {"magac": "Tusmo", "version": "1.0"};
codsi.jawaab(json_data, 200, "application/json");
```

**Halbeegyada:**
- `nuxur` (qaamuus) - Xogta loo beddelayo JSON
- `xaalad` (tiro) - Code-ka xaaladda HTTP
- `nooca` (eray) - Nooca MIME

---

### jawaab_caadi(nuxur)

Dir jawaab HTML ah.

```tus
codsi.jawaab_caadi("<h1>Hello!</h1>");
```

**Halbeegyada:**
- `nuxur` (eray) - Nuxurka HTML-ka

---

### hel_socket_handle()

Hel socket-ka hoose si loogu dallacsiiyo (upgrade) WebSocket.

```tus
keyd:eray socket_handle = codsi.hel_socket_handle();
```

**Soo-celinta:** `eray` - Socket handle-ka WebSocket

---

### foom()

Baadh (parse) xogta foomka (application/x-www-form-urlencoded).

```tus
keyd:Form foomka = codsi.foom();
keyd:eray magac = foomka.hel("name");
keyd:eray email = foomka.hel("email");
```

**Soo-celinta:** `Form` - Shayga foomka oo leh habka `hel(field)`

## Tusaale: Server HTTP Fudud

```tus
keen "http";

hawl maaree_codsiga(codsi: Codsi) : waxbo {
    keyd:eray wadada = codsi.waddo();
    
    haddii (wadada == "/") {
        codsi.jawaab_caadi("<h1>Ku soo dhowow Tusmo!</h1>");
    } ama_haddii (wadada == "/api/hello") {
        keyd:qaamuus data = {"fariin": "Hello API"};
        codsi.jawaab(data, 200, "application/json");
    } haddii_kale {
        codsi.jawaab_eray("Lama Helin", 404, "text/plain");
    }
}

keyd:Http server = Http() cusub;
qor("Server-ku wuxuu ka billowday port 8080");
server.dhegeyso("8080", maaree_codsiga);
```

## Tusaale: WebSocket iyada oo loo marayo HTTP

```tus
keen "http";
keen "webxiriiriye";

hawl maaree_codsiga(codsi: Codsi) : waxbo {
    keyd:eray dallacsiin = codsi.hel_madax("Upgrade");
    
    haddii (dallacsiin == "websocket") {
        keyd:eray socket_handle = codsi.hel_socket_handle();
        keyd:eray ws_key = codsi.hel_madax("Sec-WebSocket-Key");
        
        keyd:WebXiriiriye ws = WebXiriiriye() cusub;
        ws.kor_u_qaad(socket_handle, ws_key);
        
        qor("WebSocket-ku waa xiriiray!");
        ws.xir(1000, "Waa dhammaaday");
    } haddii_kale {
        codsi.jawaab_caadi("<h1>WebSocket Server</h1>");
    }
}

keyd:Http server = Http() cusub;
server.dhegeyso("8080", maaree_codsiga);
```
