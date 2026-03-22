# Hawl-wadeennada (Operators)

Tusmo waxay taageertaa hawl-wadeenno kala duwan oo loogu talagalay xisaabta, isbarbardhigga, iyo hawlgallada boolean-ka.

## Hawl-wadeennada Xisaabta (Arithmetic Operators)

```tus
keyd:tiro a = 10;
keyd:tiro b = 3;

qor(a + b);   // Isku-dar: 13
qor(a - b);   // Kala-goyn: 7
qor(a * b);   // Isku-dhufasho: 30
qor(a / b);   // Qaybin: 3
qor(a % b);   // Saami (Modulus): 1
```

## Kordhinta/Yareynta (Increment/Decrement)

```tus
keyd:tiro x = 0;
x = x + 1;    // Kordhin
x = x - 1;    // Yareyn
```

## Hawl-wadeennada Meel-dhigga (Assignment Operators)

```tus
keyd:tiro y = 0;
y = y + 3;
y = y - 2;
y = y * 2;
```

## Hawl-wadeennada Isbarbardhigga (Comparison Operators)

```tus
keyd:tiro p = 5;
keyd:tiro q = 10;

qor(p == q);  // La mid ah: maya
qor(p != q);  // Aan la mid ahayn: haa
qor(p < q);   // Ka yar: haa
qor(p > q);   // Ka weyn: maya
qor(p <= q);  // Ka yar ama la mid ah: haa
qor(p >= q);  // Ka weyn ama la mid ah: maya
```

Isbarbardhigga Float:

```tus
keyd:jajab f1 = 3.14;
keyd:jajab f2 = 2.5;
qor(f1 > f2);  // haa
```

## Hawl-wadeennada Boolean (Boolean Operators)

| Hawl-wadeen | Keyword | Sharaxaad |
|----------|---------|-------------|
| `&&` | `iyo` | And |
| `||` | `ama` | Or |

```tus
keyd:miyaa ha = haa;
keyd:miyaa maya = maya;

qor(ha iyo maya);  // Iyo (And): maya
qor(ha ama maya);   // Ama (Or): haa
```

## Ternary Operator

```tus
keyd:tiro num = 5;
keyd:miyaa isBig = num > 10;
keyd:eray result = isBig ? "weyn" : "yar";
```

## Kala-horreynta Hawl-wadeennada (Operator Precedence)

```tus
keyd:tiro prec = 2 + 3 * 4;    // 14 (isku-dhufashada ayaa horreysa)
prec = (2 + 3) * 4;            // 20 (parentheses ayaa horreeya)
```
