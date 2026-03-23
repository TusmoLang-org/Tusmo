# Varaibles

Tusmo waa luqad statically-typed ah taasi oo macnaheedu yahay in si cad loo muujiyo nooc-yada data-da.

## Syntax-ka Sheegista

```tus
keyd:<nooca> <magaca>;
 ama
keyd:<nooca> <magaca> = <qiimaha>;
```

## Noocyada Xogta

| Nooca | Sharaxaad | Tusaale |
|-------|-----------|---------|
| `tiro` | Integer | `10`, `-5`, `42` |
| `jajab` | Float | `3.14`, `-2.5` |
| `eray` | String | `"Hello"` |
| `xaraf` | Character | `'A'`, `'B'` |
| `miyaa` | Boolean | `haa` (haa), `maya` (maya) |
| `tix:<nooca>` | Array | `[1, 2, 3]` |
| `qaamuus` | Dictionary | `{"fure": "qiimo"}` |
| `waxbo` | Void | Qiimo ma leh |

## Tusaalooyin

### Integer (tiro)

```tus
keyd:tiro a = 10;
keyd:tiro b;
keyd:tiro c = 5 + 3;
b = 10;
b = b + a;
```

### Float (jajab)

```tus
keyd:jajab pi = 3.14;
keyd:jajab x = 2.5 * 4.2;
```

### String (eray)

```tus
keyd:eray magac = "Somali";
keyd:eray salaan = "Hellow "+magac+" developers";
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
Keyword-ka `miyaa` wuxuu ka turjumaa badanaa in response-ka ay noqoto **haa** ama **maya** taasi waa sababta aan u dooranay.

### Array (tix)

```tus
keyd:tix:tiro tirooyin = [1, 2, 3, 4, 5];
keyd:tix:eray erayo = ["aa", "ee", "ii", "oo", "uu"];
keyd:tix:xaraf xarfo = ['a', 'e', 'i', 'o', 'u'];
keyd:tix:tiro eber = [];

//eber[0] = 1;
```

### Dictionary (qaamuus)

```tus
keyd:qaamuus qof = {"magac": "Ali", "da": 25};
keyd:qaamuus qaamuusEber;
```

### Void (waxbo)

```tus
keyd:waxbo waxba;
```

## F-Strings

U isticmaal `$"{}"` isku-dhafka erayada:

```tus
keyd:eray magac = "Tusmo";
keyd:tiro da'da = 5;
qor($"Magacu waa {magac}, Da'du waa {da'da}");
```

## Ternary Operator

```tus
keyd:miyaa cond = a > 5;
keyd:eray natiijo = cond ? "weyn" : "yar";
```
