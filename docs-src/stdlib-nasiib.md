# Module-ka Nasiib (Random)

Module-ka Nasiib wuxuu bixiyaa soo saarista lambarrada nasiibka ah (random).

## Soo-dejinta (Import)

```tus
keen "nasiib";
```

Bilaabi ka hor isticmaalka (ikhtiyaari - otomaatig ayay u dhacdaa):

```tus
bilaab_nasiib();
```

## Hawlaha (Functions)

### bilaab_nasiib()

Wac mar qura bilaab_nasiib() ka hor inta aanad isticmaalin hawlaha kale si loo bilaabo.

```tus
bilaab_nasiib();
```

**Soo-celinta:** `waxbo`

---

### nasiib_tiro(ugu_yaraan, ugu_badnaan)

Soo saar integer(tiro) nasiib ah oo u dhexeeya ugu yaraan iyo ugu badnaan (oo ay ku jiraan).

```tus
keyd:tiro num = nasiib_tiro(1, 100);
qor("Nasiib: ");
qor(num);  // 1-100
```

**Halbeegyada:**
- `ugu_yaraan` (tiro) - Qiimaha ugu yar
- `ugu_badnaan` (tiro) - Qiimaha ugu weyn

**Soo-celinta:** `tiro` - Integer nasiib ah

---

### nasiib_jajab(ugu_yaraan, ugu_badnaan)

Soo saar float nasiib ah oo u dhexeeya ugu yaraan iyo ugu badnaan.

```tus
keyd:jajab num = nasiib_jajab(0.0, 1.0);
qor("Jajab nasiib ah: ");
qor(num);  // tusaale, 0.456789
```

**Halbeegyada:**
- `ugu_yaraan` (jajab) - Qiimaha ugu yar
- `ugu_badnaan` (jajab) - Qiimaha ugu weyn

**Soo-celinta:** `jajab` - Float nasiib ah

## Tusaale

```tus
keen "nasiib";

bilaab_nasiib();

// Integer nasiib ah 1-10
keyd:tiro num1 = nasiib_tiro(1, 10);
qor("Lulidda laadhka: ");
qor(num1);

// Jajab nasiib ah 0-1
keyd:jajab num2 = nasiib_jajab(0.0, 1.0);
qor("Jajab nasiib ah: ");
qor(num2);
```
