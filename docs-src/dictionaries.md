# Dictionaries

Dictionaries in Tusmo use `qaamuus` type for key-value pairs.

## Declaration

```tus
keyd:qaamuus emptyDict;
keyd:qaamuus person = {"magac": "Ali", "da": 25};
```

## Access Values

```tus
qor(person["magac"]);  // "Ali"
qor(person["da"]);     // 25
```

## Modify Values

```tus
person["da"] = 26;
```

## Add New Keys

```tus
person["phone"] = "612345678";
```

## Nested Dictionaries

```tus
keyd:qaamuus nested = {
    "user": {
        "username": "admin",
        "email": "admin@test.com"
    }
};

qor(nested["user"]["username"]);
```

## Different Value Types

```tus
keyd:qaamuus mixed = {
    "name": "Test",
    "age": 20,
    "score": 95.5,
    "active": haa
};
```

## Arrays in Dictionaries

```tus
keyd:qaamuus scores = {
    "math": [90, 85, 88],
    "science": [95, 92]
};

qor(scores["math"]);
```

## Dictionary of Dictionaries

```tus
keyd:qaamuus students = {
    "ali": {"grade": "A", "score": 95},
    "sara": {"grade": "B", "score": 88}
};
```
