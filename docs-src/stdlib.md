# Standard Library

Tusmo comes with built-in modules in the `stdlib/` folder. These are imported using the `keen` keyword.

## Built-in Functions

These functions are available without importing:

### Output

```tus
qor("Hello!");      // Print to console
```

### String Functions

| Function | Description | Example |
|----------|-------------|---------|
| `dherer(str)` | Get string length | `dherer("hello")` → 5 |
| `nooc(value)` | Convert to string | `nooc(123)` → "123" |
| `eray(value)` | Convert to string | `eray(3.14)` → "3.14" |
| `tiro(value)` | Convert to integer | `tiro("42")` → 42 |
| `jajab(value)` | Convert to float | `jajab("3.14")` → 3.14 |
| `miyaa(value)` | Convert to boolean | `miyaa("haa")` → haa |

### Array Functions

| Function | Description | Example |
|----------|-------------|---------|
| `tix_cayiman(arr)` | Get array type | Returns element type |

## Importing Modules

```tus
keen "os";
keen "wakhti";
keen "nasiib";
keen "xiriiriye";
keen "http";
```

## Library Sections

- [OS Module](stdlib-os) - File system and system operations
- [Wakhti Module](stdlib-wakhti) - Time and date functions
- [Nasiib Module](stdlib-nasiib) - Random number generation
- [Xiriiriye Module](stdlib-xiriiriye) - TCP socket programming
- [WebXiriiriye Module](stdlib-webxiriiriye) - WebSocket support
- [HTTP Module](stdlib-http) - HTTP server and request handling
