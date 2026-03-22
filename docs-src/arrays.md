# Tixyada

Tixyada Tusmo waxay isticmaalaan syntax-ka `tix:<nooca>`.

## Sheegista

```tus
keyd:tix:tiro tirooyin = [1, 2, 3, 4, 5];
keyd:tix:eray erayo = ["foo", "bar", "baz"];
keyd:tix:jajab jajabyo = [1.1, 2.2, 3.3];
keyd:tix:miyaa calamo = [haa, maya, haa];
keyd:tix:tiro eber = [];
```

## Helidda Xubnaha

```tus
qor(tirooyin[0]);  // Xubinta koowaad
qor(tirooyin[2]);  // Xubinta saddexaad
```

## Beddelidda Xubnaha

```tus
keyd:tix:tiro tix_ = [10, 20, 30];
tix_[0] = 100;
```

## Dhererka Tixda

```tus
qor(dherer(tirooyin));
```

## Ku Soco (For-Each)

```tus
soco xubin kasta laga helo tirooyin {
    qor(xubin);
}
```

## Tixyada 2D

```tus
keyd:tix:tix:tiro matrix = [[1, 2], [3, 4], [5, 6]];

qor(matrix[0][0]);  // 1
qor(matrix[1][1]);  // 4

keyd:tix:tix:eray stringMatrix = [["a", "b"], ["c", "d"]];
qor(stringMatrix[0][0]);  // "a"
```

## Tixyada leh Weedho (Expressions)

```tus
keyd:tiro qiimo1 = 1;
keyd:tiro qiimo2 = 2;
keyd:tix:tiro exprArr = [qiimo1 + qiimo2, qiimo1 * qiimo2, qiimo2 - qiimo1];
```
