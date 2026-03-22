# Hawlaha (Functions)

Tusmo waxay taageertaa hawlaha leh laba qaab oo syntax ah.

## Syntax-ka Hawsha

Tusmo waxay taageertaa laba qaab oo syntax-ka hawsha ah:

### Qaabka semi colon-ka (:) (soo-celin waxbo ah)

```tus
hawl salaam(magac: eray) : waxbo {
    qor("Hello " + magac);
}
```

### Qaabka semi colon-ka (:) (leh soo-celin)

```tus
shaqo isku_dar(a: tiro, b: tiro) : tiro {
    soo_celi a + b;
}
```

### Qaabka Arrow-ga (=>) (soo-celin waxbo ah)

```tus
hawl salaam(magac: eray) => waxbo {
    qor("Hello " + magac);
}
```

### Qaabka Arrow-ga (=>) (leh soo-celin)

```tus
shaqo isku_dar(a: tiro, b: tiro) => tiro {
    soo_celi a + b;
}
```

#### FG: Tusmo waxay taggeertaa sidoo kale labo keyword ku waas oo lagu declare-gareeyo functions-ka kuwaa oo kala ah ```hawl``` ama ```shaqo```

### Qiimayaasha la soo celiyo

U isticmaal `soo_celi` si aad u soo celiso qiimo:

```tus
hawl qaybi(a: jajab, b: jajab) => jajab {
    soo_celi a / b;
}

hawl helFariin() : eray {
    soo_celi "Tani waa fariin";
}
```

### Halbeegyada leh Qiimaha caadiga ah (Default Values)

```tus
hawl salaamCaadi ah(magac: eray, horgale: eray = "Mr.") : waxbo {
    qor("Hello " + horgale + " " + magac);
}
```

### Aan lahayn Halbeegyo

```tus
hawl dhehHello() : waxbo {
    qor("Kaliya waxaan leeyahay Hello!");
}
```

### Soo-celinta Boolean

```tus
hawl waaDhowr(n: tiro) : miyaa {
    keyd:miyaa natiijo = (n % 2) == 0;
    soo_celi natiijo;
}
```

### Halbeegyada Tixda

```tus
hawl isku_darTix(arr: tix:tiro) : tiro {
    keyd:tiro wadarta = 0;
    soco xubin kasta laga helo arr {
        wadarta = wadarta + xubin;
    }
    soo_celi wadarta;
}
```

### Keyword-yada Hawsha

| Keyword | Sharaxaad |
|---------|-------------|
| `hawl` ama `shaqo` | Qeexista function |
| `soo_celi` | Soo-celinta qiimaha |
| `: waxbo` ama => `waxbo` | Nooca soo-celinta waxbo (void) |
| `=> <nooca>` ama `: <nooca>` | Nooca soo-celinta (qaabka falaarta) |

### Wacidda Hawlaha

```tus
salaam("Tusmo");
keyd:tiro natiijo = isku_dar(5, 3);
qor(qaybi(10.0, 4.0));
```
