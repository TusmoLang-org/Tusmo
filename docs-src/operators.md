# Operators

Tusmo supports various operators for arithmetic, comparison, and boolean operations.

## Arithmetic Operators

```tus
keyd:tiro a = 10;
keyd:tiro b = 3;

qor(a + b);   // Addition: 13
qor(a - b);   // Subtraction: 7
qor(a * b);   // Multiplication: 30
qor(a / b);   // Division: 3
qor(a % b);   // Modulus: 1
```

## Increment/Decrement

```tus
keyd:tiro x = 0;
x = x + 1;    // Increment
x = x - 1;    // Decrement
```

## Assignment Operators

```tus
keyd:tiro y = 0;
y = y + 3;
y = y - 2;
y = y * 2;
```

## Comparison Operators

```tus
keyd:tiro p = 5;
keyd:tiro q = 10;

qor(p == q);  // Equal: maya
qor(p != q);  // Not equal: haa
qor(p < q);   // Less than: haa
qor(p > q);   // Greater than: maya
qor(p <= q);  // Less or equal: haa
qor(p >= q);  // Greater or equal: maya
```

Float comparison:

```tus
keyd:jajab f1 = 3.14;
keyd:jajab f2 = 2.5;
qor(f1 > f2);  // haa
```

## Boolean Operators

| Operator | Keyword | Description |
|----------|---------|-------------|
| `&&` | `iyo` | And |
| `||` | `ama` | Or |

```tus
keyd:miyaa ha = haa;
keyd:miyaa maya = maya;

qor(ha iyo maya);  // And: maya
qor(ha ama maya);   // Or: haa
```

## Ternary Operator

```tus
keyd:tiro num = 5;
keyd:miyaa isBig = num > 10;
keyd:eray result = isBig ? "big" : "small";
```

## Operator Precedence

```tus
keyd:tiro prec = 2 + 3 * 4;    // 14 (multiplication first)
prec = (2 + 3) * 4;            // 20 (parentheses first)
```
