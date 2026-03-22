# Xaaladaha (Conditions)

Tusmo waxay u isticmaashaa keyword-yo Soomaali ah weedhaha shuruudda leh.

## Weedha Haddii (If Statement)

```tus
haddii (x > 5) {
    qor("x wuxuu ka weyn yahay 5");
}
```

## Haddii-Haddii_kale (If-Else)

```tus
haddii (x < 5) {
    qor("x wuxuu ka yar yahay 5");
} haddii_kale {
    qor("x kama yara 5");
}
```

## Haddii - Ama_haddii - Haddii_kale (If-Elif-Else)

```tus
haddii (x == 5) {
    qor("x wuxuu la mid yahay 5");
} ama_haddii (x == 10) {
    qor("x wuxuu la mid yahay 10");
} ama_haddii (x == 15) {
    qor("x wuxuu la mid yahay 15");
} haddii_kale {
    qor("x waa wax kale");
}
```

## Xaaladaha Isku-dhex-jirta

```tus
haddii (x > 5) {
    qor("x > 5");
    haddii (y > 15) {
        qor("y isna wuxuu ka weyn yahay 15");
    }
}
```

## Hawl-wadeennada Isbarbardhigga (Comparison Operators)

| Hawl-wadeen | Sharaxaad |
|----------|-------------|
| `==` | La mid ah |
| `!=` | Aan la mid ahayn |
| `<` | Ka yar |
| `>` | Ka weyn |
| `<=` | Ka yar ama la mid ah |
| `>=` | Ka weyn ama la mid ah |

## Hawl-wadeennada Boolean (Boolean Operators)

| Hawl-wadeen | Keyword | Sharaxaad |
|----------|---------|-------------|
| `&&` | `iyo` | And |
| `||` | `ama` | Or |

```tus
keyd:miyaa boolA = haa;
keyd:miyaa boolB = maya;

qor(boolA iyo boolB);  // Iyo (And)
qor(boolA ama boolB);    // Ama (Or)
```

## Ternary Operator

```tus
keyd:miyaa weyn = x > y ? haa : maya;
```
