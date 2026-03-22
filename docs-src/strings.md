# Erayada (Strings)

Erayada (Strings) gudaha Tusmo waxay isticmaalaan nooca `eray`.

## Sheegista

```tus
keyd:eray str1 = "Hello";
keyd:eray str2;
keyd:eray str3 = "";
```

## Isku-dhafka (Concatenation)

```tus
keyd:eray str = "Hello" + " " + "World";
```

## Hawlaha Erayada (String Functions)

### Dhererka (Length)

```tus
qor(dherer(str1));  // Hel dhererka erayga
```

### Tilmaamidda (Indexing)

```tus
qor(str1[0]);  // Xarafka koowaad
qor(str1[1]);  // Xarafka labaad
```

## F-Strings

U isticmaal `$"{}"` isku-dhafka:

```tus
keyd:eray midho = "Tufaax";
qor($"Waan jeclahay {midho}");
qor($"Xisaab: 5 * 3 = {5 * 3}");
```

Erayada safafka badan:

```tus
keyd:eray safar = $"Kani waa 
safar
badan";
```

## Isbarbardhigga (Comparison)

```tus
keyd:eray a = "abc";
keyd:eray b = "abc";
keyd:eray c = "def";

qor(a == b);  // haa
qor(a == c);  // maya
```
