# Variables

Tusmo is a statically-typed language with explicit type declarations.

## Declaration Syntax

```tus
keyd:<type> <name>;
keyd:<type> <name> = <value>;
```

## Data Types

| Type | Description | Example |
|------|-------------|---------|
| `tiro` | Integer | `10`, `-5`, `42` |
| `jajab` | Float | `3.14`, `-2.5` |
| `eray` | String | `"Hello"` |
| `xaraf` | Character | `'A'`, `'B'` |
| `miyaa` | Boolean | `haa` (yes), `maya` (no) |
| `tix:<type>` | Array | `[1, 2, 3]` |
| `qaamuus` | Dictionary | `{"key": "value"}` |
| `waxbo` | Void/null | No value |

## Examples

### Integer (tiro)

```tus
keyd:tiro a = 10;
keyd:tiro b;
keyd:tiro c = 5 + 3;
```

### Float (jajab)

```tus
keyd:jajab pi = 3.14;
keyd:jajab x = 2.5 * 4.2;
```

### String (eray)

```tus
keyd:eray name = "Hello";
keyd:eray greeting = name + " World";
```

### Character (xaraf)

```tus
keyd:xaraf ch = 'A';
keyd:xaraf ch2 = 'B';
```

### Boolean (miyaa)

```tus
keyd:miyaa flag1 = haa;
keyd:miyaa flag2 = maya;
keyd:miyaa flag3 = a > 5;
```

### Array (tix)

```tus
keyd:tix:tiro nums = [1, 2, 3, 4, 5];
keyd:tix:eray words = ["aa", "bb", "cc"];
keyd:tix:tiro empty = [];
```

### Dictionary (qaamuus)

```tus
keyd:qaamuus person = {"magac": "Ali", "da": 25};
keyd:qaamuus emptyDict;
```

### Void (waxbo)

```tus
keyd:waxbo nothing;
```

## F-Strings

Use `$"{}"` for string interpolation:

```tus
keyd:eray name = "Tusmo";
keyd:tiro age = 5;
qor($"Name is {name}, Age is {age}");
```

## Ternary Operator

```tus
keyd:miyaa cond = a > 5;
keyd:eray result = cond ? "big" : "small";
```
