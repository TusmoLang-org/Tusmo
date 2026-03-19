# Functions

Tusmo supports functions with two syntax styles.

## Function Syntax

Tusmo supports two function syntax styles:

### Colon Style (void return)

```tus
hawl greet(name: eray) : waxbo {
    qor("Hello " + name);
}
```

### Arrow Style (with return)

```tus
shaqo add(a: tiro, b: tiro) => tiro {
    soo_celi a + b;
}
```

### Return Values

Use `soo_celi` to return:

```tus
hawl divide(a: jajab, b: jajab) => jajab {
    soo_celi a / b;
}

hawl getMessage() : eray {
    soo_celi "This is a message";
}
```

### Parameters with Default Values

```tus
hawl greetDefault(name: eray, prefix: eray = "Mr.") : waxbo {
    qor("Hello " + prefix + " " + name);
}
```

### No Parameters

```tus
hawl sayHello() : waxbo {
    qor("Just saying Hello!");
}
```

### Return Boolean

```tus
hawl isEven(n: tiro) : miyaa {
    keyd:miyaa res = (n % 2) == 0;
    soo_celi res;
}
```

### Array Parameters

```tus
hawl sumArray(arr: tix:tiro) : tiro {
    keyd:tiro total = 0;
    soco item kasta laga helo arr {
        total = total + item;
    }
    soo_celi total;
}
```

### Function Keywords

| Keyword | Description |
|---------|-------------|
| `hawl` | Function declaration (colon style) |
| `shaqo` | Function declaration (arrow style) |
| `soo_celi` | Return value |
| `: waxbo` | Void return type |
| `=> <type>` | Return type (arrow style) |

### Calling Functions

```tus
greet("Tusmo");
keyd:tiro result = add(5, 3);
qor(divide(10.0, 4.0));
```
