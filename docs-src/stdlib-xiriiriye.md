# Module-ka Xiriiriye

Module-ka Xiriiriye wuxuu bixiyaa barnaamijka socket-ka ee heerka hoose ee xiriirka TCP.

## Soo-dejinta (Import)

```tus
keen "xiriiriye";
```

## Samee Socket

```tus
keyd:Xiriiriye socket = Xiriiriye() cusub;
```

## Hababka (Methods)

### samee_server(port)

Abuur socket server oo ka dhageysanaya port cayiman.

```tus
keyd:eray handle = socket.samee_server("8080");
haddii (handle == "") {
    qor("Fashil ku yimid abuurista server-ka!");
} haddii_kale {
    qor("Server-ka waa la abuuray!");
}
```

**Halbeegyada:**
- `port` (eray) - Lambarka port-ka oo eray ah (tusaale, "8080")

**Soo-celinta:** `eray` - Socket handle (eray madhan haddii uu fashilmo)

---

### dhageyso(ugu_badan_macmiil)

Billow dhageysiga xiriirada.

```tus
keyd:tiro natiijo = socket.dhageyso(5);
haddii (natiijo == 0) {
    qor("Dhageysanaya...");
}
```

**Halbeegyada:**
- `ugu_badan_macmiil` (tiro) - Dhererka ugu badan ee safka sugitaanka (badanaa 5-10)

**Soo-celinta:** `tiro` - 0 haddii lagu guuleysto, -1 haddii kale

---

### aqbal()

Aqbal xiriirka macmiilka ee soo socda.

```tus
keyd:eray client_handle = socket.aqbal();
haddii (client_handle == "") {
    qor("Macmiil ma xiriirsana");
} haddii_kale {
    qor("Macmiil waa soo xiriiray!");
}
```

**Soo-celinta:** `eray` - Macmiilka handle-kiisa (eray madhan haddii uusan jirin xiriir)

---

### kuxirmo(host, port)

Ku xirmo server fog sidii macmiil (client).

```tus
keyd:eray handle = socket.kuxirmo("example.com", "80");
haddii (handle == "") {
    qor("Xiriirku waa fashilmay!");
}
```

**Halbeegyada:**
- `host` (eray) - Magaca host-ka ama IP (tusaale, "example.com", "127.0.0.1")
- `port` (eray) - Port-ka oo eray ah (tusaale, "80")

**Soo-celinta:** `eray` - Socket handle (eray madhan haddii uu fashilmo)

---

### dir(xogta)

Xog ku dir socket-ka.

```tus
keyd:tiro bytes_sent = socket.dir("Hello Server!");
qor("Bytes la diray: ");
qor(bytes_sent);
```

**Halbeegyada:**
- `xogta` (eray) - Xogta la dirayo

**Soo-celinta:** `tiro` - Bytes-ka la diray, ama -1 haddii uu qalad dhaco

---

### soo_hel(size)

Ka hel xog socket-ka.

```tus
keyd:eray data = socket.soo_hel(1024);
qor("La helay: ");
qor(data);
```

**Halbeegyada:**
- `size` (tiro) - Bytes-ka ugu badan ee la helayo

**Soo-celinta:** `eray` - Xogta la helay

---

### xir()

Xir socket-ka.

```tus
socket.xir();
```

---

### waa_ansax()

Hubi haddii socket-ku yahay mid ansax ah.

```tus
haddii (socket.waa_ansax()) {
    qor("Socket-ku waa furan yahay");
}
```

**Soo-celinta:** `miyaa` - haa haddii uu ansax yahay, maya haddii kale

## Tusaale Server

```tus
keen "xiriiriye";

keyd:Xiriiriye server = Xiriiriye() cusub;
keyd:eray handle = server.samee_server("9999");

haddii (handle == "") {
    qor("Abuurista server-ka waa fashilantay!");
    server.xir();
}

server.dhageyso(5);
qor("Sugaya macmiil...");

keyd:eray client = server.aqbal();
haddii (client == "") {
    qor("Macmiil ma xiriirsana");
} haddii_kale {
    qor("Macmiil waa soo xiriiray!");
    server.dir("Ku soo dhowow server-ka!");
}

server.xir();
```

## Tusaale Macmiil (Client)

```tus
keen "xiriiriye";

keyd:Xiriiriye client = Xiriiriye() cusub;
keyd:eray handle = client.kuxirmo("example.com", "80");

haddii (handle == "") {
    qor("Xiriirku waa fashilmay!");
    client.xir();
}

// Dir codsi HTTP ah
client.dir("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n");

// Hel jawaabta
keyd:eray response = client.soo_hel(4096);
qor(response);

client.xir();
```
