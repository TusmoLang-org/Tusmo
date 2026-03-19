# Arrays

Arrays in Tusmo use `tix:<type>` syntax.

## Declaration

```tus
keyd:tix:tiro nums = [1, 2, 3, 4, 5];
keyd:tix:eray words = ["foo", "bar", "baz"];
keyd:tix:jajab floats = [1.1, 2.2, 3.3];
keyd:tix:miyaa flags = [haa, maya, haa];
keyd:tix:tiro empty = [];
```

## Access Elements

```tus
qor(nums[0]);  // First element
qor(nums[2]);  // Third element
```

## Modify Elements

```tus
keyd:tix:tiro arr = [10, 20, 30];
arr[0] = 100;
```

## Array Length

```tus
qor(dherer(nums));
```

## Iterate with For-Each

```tus
soco item kasta laga helo nums {
    qor(item);
}
```

## 2D Arrays

```tus
keyd:tix:tix:tiro matrix = [[1, 2], [3, 4], [5, 6]];

qor(matrix[0][0]);  // 1
qor(matrix[1][1]);  // 4

keyd:tix:tix:eray stringMatrix = [["a", "b"], ["c", "d"]];
qor(stringMatrix[0][0]);  // "a"
```

## Arrays with Expressions

```tus
keyd:tiro val1 = 1;
keyd:tiro val2 = 2;
keyd:tix:tiro exprArr = [val1 + val2, val1 * val2, val2 - val1];
```
