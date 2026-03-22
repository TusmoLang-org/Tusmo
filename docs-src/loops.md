# Wareegyada (Loops)

Tusmo waxay taageertaa dhowr nooc oo loop (wareegyo) ah.

## Wareegga Inta ay (While Loop)

```tus
keyd:tiro i = 0;
inta ay (i < 5) {
    qor("While: " + i);
    i = i + 1;
}
```

## Wareegga Samee-Inta ay (Do-While Loop)

```tus
keyd:tiro j = 0;
samay {
    qor("Do-While: " + j);
    j = j + 1;
} inta ay (j < 5);
```

## Wareegga Soco ee Range-ka (For Range Loop)

```tus
soco k laga bilaabo 0 .. 5 {
    qor("For Range: " + k);
}
```

## Wareegga Soco Mid kasta (For-Each Loop)

```tus
keyd:tix:eray arr = ["aa", "bb", "cc"];
soco xubin kasta laga helo arr {
    qor("For Each: " + xubin);
}
```

## Jooji (Break)

```tus
keyd:tiro n = 0;
inta ay (n < 10) {
    n = n + 1;
    haddii (n == 5) {
        joog;
    }
    qor("Tijaabada Break: " + n);
}
```

## Kasoco (Continue)

```tus
soco m laga bilaabo 0 .. 5 {
    haddii (m == 2) {
        kasoco;
    }
    qor("Tijaabada Continue: " + m);
}
```

## Wareegyada Is-dhex-jira

```tus
keyd:tiro outer = 0;
inta ay (outer < 3) {
    keyd:tiro inner = 0;
    soco inner_loop laga bilaabo 0 .. 3 {
        haddii (outer == 1 iyo inner == 1) {
            joog;
        }
        qor($"Bannaanka: {outer}, Gudaha: {inner}");
        inner = inner + 1;
    }
    outer = outer + 1;
}
```

## Soo-koobidda Keyword-yada Wareegga

| Keyword | Sharaxaad |
|---------|-------------|
| `inta ay ...` | Shuruudda While |
| `samay ...` | Do-while |
| `soco ...` | For/foreach |
| `joog` | Break |
| `kasoco` | Continue |
| `laga bilaabo` | Bilowga range-ka |
| `..` | Range-ka |
| `kasta laga helo` | Wareeg kasta (iteration) |
