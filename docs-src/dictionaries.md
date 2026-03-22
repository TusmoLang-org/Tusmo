# Qaamuusyada (Dictionaries)

Qaamuusyada Tusmo waxay u isticmaalaan nooca `qaamuus` lammaanaha fure-iyo-qiimo (key-value pairs).

## Sheegista

```tus
keyd:qaamuus qaamuusEber;
keyd:qaamuus qof = {"magac": "Ali", "da": 25};
```

## Helidda Qiimayaasha

```tus
qor(qof["magac"]);  // "Ali"
qor(qof["da"]);     // 25
```

## Beddelidda Qiimayaasha

```tus
qof["da"] = 26;
```

## Ku-daridda Furayaal Cusub

```tus
qof["telefoon"] = "612345678";
```

## Qaamuusyada Is-dhex-jira

```tus
keyd:qaamuus is_dhex_jira = {
    "isticmaale": {
        "magac": "admin",
        "email": "admin@test.com"
    }
};

qor(is_dhex_jira["isticmaale"]["magac"]);
```

## Noocyo Qiimo oo Kala Duwan

```tus
keyd:qaamuus isku_dhaf = {
    "magac": "Tijaabo",
    "da": 20,
    "dhibco": 95.5,
    "shaqaynaya": haa
};
```




