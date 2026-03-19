# Conditions

Tusmo uses Somali keywords for conditional statements.

## If Statement

```tus
haddii (x > 5) {
    qor("x is greater than 5");
}
```

## If-Else

```tus
haddii (x < 5) {
    qor("x is less than 5");
} haddii_kale {
    qor("x is NOT less than 5");
}
```

## If-Elif-Else

```tus
haddii (x == 5) {
    qor("x equals 5");
} ama_haddii (x == 10) {
    qor("x equals 10");
} ama_haddii (x == 15) {
    qor("x equals 15");
} haddii_kale {
    qor("x is something else");
}
```

## Nested Conditions

```tus
haddii (x > 5) {
    qor("x > 5");
    haddii (y > 15) {
        qor("y > 15 too");
    }
}
```

## Comparison Operators

| Operator | Description |
|----------|-------------|
| `==` | Equal |
| `!=` | Not equal |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal |
| `>=` | Greater than or equal |

## Boolean Operators

| Operator | Keyword | Description |
|----------|---------|-------------|
| `&&` | `iyo` | And |
| `||` | `ama` | Or |

```tus
keyd:miyaa boolA = haa;
keyd:miyaa boolB = maya;

qor(boolA iyo boolB);  // And
qor(boolA ama boolB);    // Or
```

## Ternary Operator

```tus
keyd:miyaa big = x > y ? haa : maya;
```
