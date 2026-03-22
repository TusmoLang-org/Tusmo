# Maktabadda Caadiga ah (Standard Library)

Tusmo waxay la timaadaa modules ku dhex dhisan oo ku jira folder-ka `stdlib/`. Kuwan waxaa lagu soo dejiyaa iyadoo la isticmaalayo keyword-ka `keen`.

## Hawlaha ku dhex dhisan (Built-in Functions)

Hawlahani waxay diyaar yihiin iyadoon waxba la soo dejin:

### Soo-saarka (Output)

```tus
qor("Hello!");      // Ku daabac console-ka
```

### Hawlaha Erayada (String Functions)

| Hawsha | Sharaxaad | Tusaale |
|----------|-------------|---------|
| `dherer(str)` | Hel dhererka erayga | `dherer("hello")` → 5 |
| `nooc(value)` | Hel nooca xogta | `nooc(123)` → "tiro" |
| `eray(value)` | U beddel eray | `eray(3.14)` → "3.14" |
| `tiro(value)` | U beddel integer | `tiro("42")` → 42 |
| `jajab(value)` | U beddel float | `jajab("3.14")` → 3.14 |
| `miyaa(value)` | U beddel boolean | `miyaa("haa")` → haa |

### Hawlaha Tixda (Array Functions)

| Hawsha | Sharaxaad | Tusaale |
|----------|-------------|---------|
| `tix_cayiman(arr)` | Hel nooca tixda | Waxay soo celisaa nooca xubinta |

## Soo-dejinta Modules-ka (Importing Modules)

```tus
keen "os";
keen "wakhti";
keen "nasiib";
keen "xiriiriye";
keen "http";
```

## Qaybaha Maktabadda

- [Module-ka OS](stdlib-os.md) - Nidaamka faylka iyo hawlgallada nidaamka
- [Module-ka Wakhti](stdlib-wakhti.md) - Hawlaha wakhtiga iyo taariikhda
- [Module-ka Nasiib](stdlib-nasiib.md) - Soo saarista lambarrada nasiibka ah (random)
- [Module-ka Xiriiriye](stdlib-xiriiriye.md) - Barnaamijka TCP socket
- [Module-ka WebXiriiriye](stdlib-webxiriiriye.md) - Taageerada WebSocket
- [Module-ka HTTP](stdlib-http.md) - HTTP server iyo maareynta codsiyada
