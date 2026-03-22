# Module-ka WebXiriiriye

Module-ka WebXiriiriye wuxuu bixiyaa taageerada WebSocket ee xiriirka labada dhinac ee wakhtiga dhabta ah.

## Keenista (Import)

```tus
keen "webxiriiriye";
```

## Samee WebSocket

```tus
keyd:WebXiriiriye ws = WebXiriiriye() cusub;
```

## Hababka (Methods)

### kor_u_qaad(socket_handle, ws_key)

U dallacsii xiriirka HTTP una beddel WebSocket.

```tus
keyd:eray ws_key = "dGhlIHNhbXBsZSBncmF2aXR5";  // Ka yimid HTTP request header
ws.kor_u_qaad(client_socket_handle, ws_key);
```

**Halbeegyada:**
- `client_socket_handle` (eray) - Macmiilka socket handle-kiisa oo ka yimid server-ka HTTP
- `ws_key` (eray) - Sec-WebSocket-Key oo ka yimid HTTP request header

---

### dir_qoraal(fariin)

Dir fariin qoraal ah.

```tus
keyd:tiro sent = ws.dir_qoraal("Hello!");
qor("Bytes la diray: ");
qor(sent);
```

**Halbeegyada:**
- `fariin` (eray) - Qoraalka fariinta

**Soo-celinta:** `tiro` - Bytes-ka la diray, ama -1 haddii uu qalad dhaco

---

### dir_binary(xog)

Dir xog binary ah.

```tus
keyd:tiro sent = ws.dir_binary("\x00\x01\x02");
```

**Halbeegyada:**
- `xog` (eray) - Xogta binary-ga ah

**Soo-celinta:** `tiro` - Bytes-ka la diray, ama -1 haddii uu qalad dhaco

---

### soo_hel_fariin()

Hel fariinta WebSocket.

```tus
keyd:qaamuus msg = ws.soo_hel_fariin();
haddii (msg["xaalad"] == "guul") {
    haddii (msg["nooc"] == "qoraal") {
        qor("Qoraal: ");
        qor(msg["xog"]);
    } ama_haddii (msg["nooc"] == "binary") {
        qor("Binary la helay");
    } ama_haddii (msg["nooc"] == "xir") {
        qor("Xiriirka waa la xiray");
    }
}
```

**Soo-celinta:** `qaamuus` - Shayga fariinta oo leh:
- `xaalad`: "guul" ama "qalad"
- `nooc`: "qoraal", "binary", "ping", "pong", ama "xir"
- `xog`: Nuxurka fariinta

---

### dir_ping()

Dir frame-ka ping.

```tus
keyd:tiro natiijo = ws.dir_ping();
```

**Soo-celinta:** `tiro` - 0 haddii lagu guuleysto, -1 haddii kale

---

### dir_pong()

Dir frame-ka pong.

```tus
keyd:tiro natiijo = ws.dir_pong();
```

**Soo-celinta:** `tiro` - 0 haddii lagu guuleysto, -1 haddii kale

---

### xir(cod, sabab)

Xir xiriirka WebSocket.

```tus
ws.xir(1000, "Xiritaan caadi ah");
```

**Halbeegyada:**
- `cod` (tiro) - Code-ka xiritaanka (1000 = xiritaan caadi ah)
- `sabab` (eray) - Sababta xiritaanka

---

### ma_xiran()

Hubi haddii WebSocket uu xiriirsan yahay.

```tus
haddii (ws.ma_xiran()) {
    qor("Waa xiriirsan yahay!");
}
```

**Soo-celinta:** `miyaa` - haa haddii uu xiriirsan yahay, maya haddii kale

## Tusaale: Server WebSocket

```tus
keen "xiriiriye";
keen "webxiriiriye";
keen "http";

keyd:Xiriiriye server = Xiriiriye() cusub;
keyd:eray handle = server.samee_server("8080");

haddii (handle == "") {
    qor("Server-ku waa fashilmay!");
    server.xir();
}

server.dhageyso(5);
qor("WebSocket server-ku wuxuu ku jiraa port 8080");

keyd:eray client = server.aqbal();
haddii (client == "") {
    qor("Macmiil ma jiro");
} haddii_kale {
    // Hel WebSocket key ka yimid codsiga HTTP
    keyd:eray ws_key = http.fariin_weyn(client, "Sec-WebSocket-Key");
    
    keyd:WebXiriiriye ws = WebXiriiriye() cusub;
    ws.kor_u_qaad(client, ws_key);
    
    qor("WebSocket waa xiriiray!");
    
    // Echo fariimaha
    keyd:qaamuus msg = ws.soo_hel_fariin();
    haddii (msg["xaalad"] == "guul" iyo msg["nooc"] == "qoraal") {
        ws.dir_qoraal(msg["xog"]);  // Dib u soo celi
    }
    
    ws.xir(1000, "Waa dhammaaday");
}

server.xir();
```
