# Strings

Strings in Tusmo use the `eray` type.

## Declaration

```tus
keyd:eray str1 = "Hello";
keyd:eray str2;
keyd:eray str3 = "";
```

## Concatenation

```tus
keyd:eray str = "Hello" + " " + "World";
```

## String Functions

### Length

```tus
qor(dherer(str1));  // Get string length
```

### Indexing

```tus
qor(str1[0]);  // First character
qor(str1[1]);  // Second character
```

## F-Strings

Use `$"{}"` for interpolation:

```tus
keyd:eray fruit = "Apple";
qor($"I like {fruit}");
qor($"Math: 5 * 3 = {5 * 3}");
```

Multi-line strings:

```tus
keyd:eray multiline = $"This is a
multi-line
string";
```

## Comparison

```tus
keyd:eray a = "abc";
keyd:eray b = "abc";
keyd:eray c = "def";

qor(a == b);  // haa (yes)
qor(a == c);  // maya (no)
```
