# HTTP Module

The HTTP module provides HTTP server functionality.

## Import

```tus
keen "http";
```

## Http Class

Create an HTTP server.

```tus
keyd:Http server = Http() cusub;
```

### dhegeyso(port, handler)

Start HTTP server on a port.

```tus
hawl maamule(codsi: Codsi) : waxbo {
    qor("Request: " + codsi.waddo());
    codsi.jawaab_caadi("<h1>Hello!</h1>");
}

server.dhegeyso("8080", maamule);
```

**Parameters:**
- `port` (eray) - Port number (e.g., "8080")
- `maamule` (hawl) - Handler function that takes a Codsi object

---

### jooji()

Stop the server.

```tus
server.jooji();
```

---

## Codsi Class

The Codsi class represents an HTTP request. It's passed to your handler function.

### hab()

Get HTTP method.

```tus
keyd:eray method = codsi.hab();
// Returns: "HELID" (GET), "DHIGID" (POST), etc.
```

**Returns:** `eray` - HTTP method

---

### waddo()

Get request path/URL.

```tus
keyd:eray path = codsi.waddo();
// e.g., "/api/users"
```

**Returns:** `eray` - Request path

---

### xambaare()

Get request body.

```tus
keyd:eray body = codsi.xambaare();
```

**Returns:** `eray` - Request body content

---

### macmiil()

Get client IP address.

```tus
keyd:eray client = codsi.macmiil();
// e.g., "192.168.1.100:12345"
```

**Returns:** `eray` - Client address

---

### hel_madax(name)

Get HTTP header value.

```tus
keyd:eray content_type = codsi.hel_madax("Content-Type");
keyd:eray user_agent = codsi.hel_madax("User-Agent");
```

**Parameters:**
- `magac` (eray) - Header name

**Returns:** `eray` - Header value

---

### jawaab_eray(content, status, content_type)

Send text response.

```tus
codsi.jawaab_eray("<h1>Hello</h1>", 200, "text/html; charset=utf-8");
```

**Parameters:**
- `nuxur` (eray) - Response content
- `xaalad` (tiro) - HTTP status code (e.g., 200, 404)
- `nooca` (eray) - MIME type (e.g., "text/html")

---

### jawaab(data, status, content_type)

Send JSON response.

```tus
keyd:qaamuus json_data = {"name": "Tusmo", "version": "1.0"};
codsi.jawaab(json_data, 200, "application/json");
```

**Parameters:**
- `nuxur` (qaamuus) - Data to convert to JSON
- `xaalad` (tiro) - HTTP status code
- `nooca` (eray) - MIME type

---

### jawaab_caadi(content)

Send HTML response (shortcut).

```tus
codsi.jawaab_caadi("<h1>Hello!</h1>");
```

**Parameters:**
- `nuxur` (eray) - HTML content

---

### hel_socket_handle()

Get underlying socket for WebSocket upgrade.

```tus
keyd:eray socket_handle = codsi.hel_socket_handle();
```

**Returns:** `eray` - Socket handle for WebSocket

---

### foom()

Parse form data (application/x-www-form-urlencoded).

```tus
keyd:Form form = codsi.foom();
keyd:eray name = form.hel("name");
keyd:eray email = form.hel("email");
```

**Returns:** `Form` - Form object with `hel(field)` method

## Example: Simple HTTP Server

```tus
keen "http";

hawl handle_request(codsi: Codsi) : waxbo {
    keyd:eray path = codsi.waddo();
    
    haddii (path == "/") {
        codsi.jawaab_caadi("<h1>Welcome to Tusmo!</h1>");
    } ama_haddii (path == "/api/hello") {
        keyd:qaamuus data = {"message": "Hello API"};
        codsi.jawaab(data, 200, "application/json");
    } haddii_kale {
        codsi.jawaab_eray("Not Found", 404, "text/plain");
    }
}

keyd:Http server = Http() cusub;
qor("Server started on port 8080");
server.dhegeyso("8080", handle_request);
```

## Example: WebSocket via HTTP

```tus
keen "http";
keen "webxiriiriye";

hawl handle_request(codsi: Codsi) : waxbo {
    keyd:eray upgrade = codsi.hel_madax("Upgrade");
    
    haddii (upgrade == "websocket") {
        keyd:eray socket_handle = codsi.hel_socket_handle();
        keyd:eray ws_key = codsi.hel_madax("Sec-WebSocket-Key");
        
        keyd:WebXiriiriye ws = WebXiriiriye() cusub;
        ws.kor_u_qaad(socket_handle, ws_key);
        
        qor("WebSocket connected!");
        ws.xir(1000, "Done");
    } haddii_kale {
        codsi.jawaab_caadi("<h1>WebSocket Server</h1>");
    }
}

keyd:Http server = Http() cusub;
server.dhegeyso("8080", handle_request);
```
