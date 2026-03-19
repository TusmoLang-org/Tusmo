# Loops

Tusmo supports multiple loop types.

## While Loop

```tus
keyd:tiro i = 0;
inta ay (i < 5) {
    qor("While: " + i);
    i = i + 1;
}
```

## Do-While Loop

```tus
keyd:tiro j = 0;
samay {
    qor("Do-While: " + j);
    j = j + 1;
} inta ay (j < 5);
```

## For Range Loop

```tus
soco k laga bilaabo 0 .. 5 {
    qor("For Range: " + k);
}
```

## For-Each Loop

```tus
keyd:tix:eray arr = ["aa", "bb", "cc"];
soco item kasta laga helo arr {
    qor("For Each: " + item);
}
```

## Break

```tus
keyd:tiro n = 0;
inta ay (n < 10) {
    n = n + 1;
    haddii (n == 5) {
        joog;
    }
    qor("Break test: " + n);
}
```

## Continue

```tus
soco m laga bilaabo 0 .. 5 {
    haddii (m == 2) {
        kasoco;
    }
    qor("Continue test: " + m);
}
```

## Nested Loops

```tus
keyd:tiro outer = 0;
inta ay (outer < 3) {
    keyd:tiro inner = 0;
    soco inner_loop laga bilaabo 0 .. 3 {
        haddii (outer == 1 iyo inner == 1) {
            joog;
        }
        qor($"Outer: {outer}, Inner: {inner}");
        inner = inner + 1;
    }
    outer = outer + 1;
}
```

## Loop Keywords Summary

| Keyword | Description |
|---------|-------------|
| `inta ay ...` | While condition |
| `samay ...` | Do-while |
| `soco ...` | For/foreach |
| `joog` | Break |
| `kasoco` | Continue |
| `laga bilaabo` | Range start |
| `..` | Range |
| `kasta laga helo` | For each iteration |
