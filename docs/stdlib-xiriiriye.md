# Xiriiriye Module

The Xiriiriye module provides low-level socket programming for TCP connections.

## Import

```tus
keen "xiriiriye";
```

## Create Socket

```tus
keyd:Xiriiriye socket = Xiriiriye() cusub;
```

## Methods

### samee_server(port)

Create a server socket listening on a port.

```tus
keyd:eray handle = socket.samee_server("8080");
haddii (handle == "") {
    qor("Failed to create server!");
} haddii_kale {
    qor("Server created!");
}
```

**Parameters:**
- `port` (eray) - Port number as string (e.g., "8080")

**Returns:** `eray` - Socket handle (empty string on failure)

---

### dhageyso(max_clients)

Start listening for connections.

```tus
keyd:tiro result = socket.dhageyso(5);
haddii (result == 0) {
    qor("Listening...");
}
```

**Parameters:**
- `saf_sugid_ugu_badan` (tiro) - Maximum queue length (typically 5-10)

**Returns:** `tiro` - 0 on success, -1 on failure

---

### aqbal()

Accept incoming client connection.

```tus
keyd:eray client_handle = socket.aqbal();
haddii (client_handle == "") {
    qor("No client connected");
} haddii_kale {
    qor("Client connected!");
}
```

**Returns:** `eray` - Client handle (empty string if no connection)

---

### kuxirmo(host, port)

Connect to a remote server as client.

```tus
keyd:eray handle = socket.kuxirmo("example.com", "80");
haddii (handle == "") {
    qor("Connection failed!");
}
```

**Parameters:**
- `host` (eray) - Hostname or IP (e.g., "example.com", "127.0.0.1")
- `port` (eray) - Port as string (e.g., "80")

**Returns:** `eray` - Socket handle (empty string on failure)

---

### dir(data)

Send data over socket.

```tus
keyd:tiro bytes_sent = socket.dir("Hello Server!");
qor("Sent bytes: ");
qor(bytes_sent);
```

**Parameters:**
- `xogta` (eray) - Data to send

**Returns:** `tiro` - Bytes sent, or -1 on error

---

### soo_hel(size)

Receive data from socket.

```tus
keyd:eray data = socket.soo_hel(1024);
qor("Received: ");
qor(data);
```

**Parameters:**
- `size` (tiro) - Maximum bytes to receive

**Returns:** `eray` - Received data

---

### xir()

Close the socket.

```tus
socket.xir();
```

---

### waa_ansax()

Check if socket is valid.

```tus
haddii (socket.waa_ansax()) {
    qor("Socket is open");
}
```

**Returns:** `miyaa` - haa if valid, maya otherwise

## Server Example

```tus
keen "xiriiriye";

keyd:Xiriiriye server = Xiriiriye() cusub;
keyd:eray handle = server.samee_server("9999");

haddii (handle == "") {
    qor("Server creation failed!");
    socket.xir();
}

server.dhageyso(5);
qor("Waiting for client...");

keyd:eray client = server.aqbal();
haddii (client == "") {
    qor("No client connected");
} haddii_kale {
    qor("Client connected!");
    server.dir("Welcome to server!");
}

server.xir();
```

## Client Example

```tus
keen "xiriiriye";

keyd:Xiriiriye client = Xiriiriye() cusub;
keyd:eray handle = client.kuxirmo("example.com", "80");

haddii (handle == "") {
    qor("Connection failed!");
    client.xir();
}

// Send HTTP request
client.dir("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n");

// Receive response
keyd:eray response = client.soo_hel(4096);
qor(response);

client.xir();
```
