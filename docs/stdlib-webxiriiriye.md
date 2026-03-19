# WebXiriiriye Module

The WebXiriiriye module provides WebSocket support for real-time bidirectional communication.

## Import

```tus
keen "webxiriiriye";
```

## Create WebSocket

```tus
keyd:WebXiriiriye ws = WebXiriiriye() cusub;
```

## Methods

### kor_u_qaad(socket_handle, ws_key)

Upgrade HTTP connection to WebSocket.

```tus
keyd:eray ws_key = "dGhlIHNhbXBsZSBncmF2aXR5";  // From HTTP request header
ws.kor_u_qaad(client_socket_handle, ws_key);
```

**Parameters:**
- `client_socket_handle` (eray) - Client socket handle from HTTP server
- `ws_key` (eray) - Sec-WebSocket-Key from HTTP request header

---

### dir_qoraal(message)

Send text message.

```tus
keyd:tiro sent = ws.dir_qoraal("Hello!");
qor("Sent bytes: ");
qor(sent);
```

**Parameters:**
- `fariin` (eray) - Message text

**Returns:** `tiro` - Bytes sent, or -1 on error

---

### dir_binary(data)

Send binary data.

```tus
keyd:tiro sent = ws.dir_binary("\x00\x01\x02");
```

**Parameters:**
- `xog` (eray) - Binary data

**Returns:** `tiro` - Bytes sent, or -1 on error

---

### soo_hel_fariin()

Receive WebSocket message.

```tus
keyd:qaamuus msg = ws.soo_hel_fariin();
haddii (msg["xaalad"] == "guul") {
    haddii (msg["nooc"] == "qoraal") {
        qor("Text: ");
        qor(msg["xog"]);
    } ama_haddii (msg["nooc"] == "binary") {
        qor("Binary received");
    } ama_haddii (msg["nooc"] == "xir") {
        qor("Connection closed");
    }
}
```

**Returns:** `qaamuus` - Message object with:
- `xaalad`: "guul" or "qalad"
- `nooc`: "qoraal", "binary", "ping", "pong", or "xir"
- `xog`: Message content

---

### dir_ping()

Send ping frame.

```tus
keyd:tiro result = ws.dir_ping();
```

**Returns:** `tiro` - 0 on success, -1 on error

---

### dir_pong()

Send pong frame.

```tus
keyd:tiro result = ws.dir_pong();
```

**Returns:** `tiro` - 0 on success, -1 on error

---

### xir(code, reason)

Close WebSocket connection.

```tus
ws.xir(1000, "Normal shutdown");
```

**Parameters:**
- `cod` (tiro) - Close code (1000 = normal close)
- `sabab` (eray) - Close reason

---

### ma_xiran()

Check if WebSocket is connected.

```tus
haddii (ws.ma_xiran()) {
    qor("Connected!");
}
```

**Returns:** `miyaa` - haa if connected, maya otherwise

## Example: WebSocket Server

```tus
keen "xiriiriye";
keen "webxiriiriye";
keen "http";

keyd:Xiriiriye server = Xiriiriye() cusub;
keyd:eray handle = server.samee_server("8080");

haddii (handle == "") {
    qor("Server failed!");
    server.xir();
}

server.dhageyso(5);
qor("WebSocket server on port 8080");

keyd:eray client = server.aqbal();
haddii (client == "") {
    qor("No client");
} haddii_kale {
    // Get WebSocket key from HTTP request
    keyd:eray ws_key = http.fariin_weyn(client, "Sec-WebSocket-Key");
    
    keyd:WebXiriiriye ws = WebXiriiriye() cusub;
    ws.kor_u_qaad(client, ws_key);
    
    qor("WebSocket connected!");
    
    // Echo messages
    keyd:qaamuus msg = ws.soo_hel_fariin();
    haddii (msg["xaalad"] == "guul" iyo msg["nooc"] == "qoraal") {
        ws.dir_qoraal(msg["xog"]);  // Echo back
    }
    
    ws.xir(1000, "Done");
}

server.xir();
```
