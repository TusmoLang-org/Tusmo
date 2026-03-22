# Module-ka Wakhti

Module-ka Wakhti wuxuu bixiyaa hawlaha wakhtiga iyo taariikhda.

## keenista (Import)

```tus
keen "wakhti";
```

## Hababka (Methods)

### hadda()

Hel timestamp-ka hadda jooga.

```tus
keyd:jajab hadda = wakhti.hadda();
qor("Timestamp: ");
qor(hadda);
```

**Soo-celinta:** `jajab` - Unix timestamp (ilbiriqsiyo tan iyo epoch)

---

### qaab(format)

Qaabee wakhtiga hadda jooga.

```tus
keyd:eray qaabaysan = wakhti.qaab("%Y-%m-%d %H:%M:%S");
qor(qaabaysan);  // tusaale, "2024-01-15 10:30:45"
```

**Halbeegyada:**
- `format` (eray) - Erayga qaabaynta

**Xarfaha qaabaynta (Format specifiers):**
| Code | Sharaxaad |
|------|-------------|
| `%Y` | Sanadka (4 god) |
| `%m` | Bisha (01-12) |
| `%d` | Maalinta (01-31) |
| `%H` | Saacadda (00-23) |
| `%M` | Daqiiqadda (00-59) |
| `%S` | Ilbiriqsiga (00-59) |

**Soo-celinta:** `eray` - Erayga wakhtiga oo qaabaysan

---

### sekeno()

Hel ilbiriqsiyada hadda (0-59).

```tus
keyd:tiro sec = wakhti.sekeno();
qor("Ilbiriqsiyo: ");
qor(sec);
```

**Soo-celinta:** `tiro` - Ilbiriqsiyo (0-59)

---

### daqiiqado()

Hel daqiiqadaha hadda (0-59).

```tus
keyd:tiro min = wakhti.daqiiqado();
qor("Daqiiqado: ");
qor(min);
```

**Soo-celinta:** `tiro` - Daqiiqado (0-59)

---

### saacado()

Hel saacadaha hadda (0-23).

```tus
keyd:tiro hr = wakhti.saacado();
qor("Saacad: ");
qor(hr);
```

**Soo-celinta:** `tiro` - Saacadood (0-23)

---

### maalin()

Hel maalinta bisha ee hadda (1-31).

```tus
keyd:tiro day = wakhti.maalin();
qor("Maalin: ");
qor(day);
```

**Soo-celinta:** `tiro` - Maalin (1-31)

---

### bil()

Hel bisha hadda (1-12).

```tus
keyd:tiro month = wakhti.bil();
qor("Bil: ");
qor(month);
```

**Soo-celinta:** `tiro` - Bil (1-12)

---

### sanad()

Hel sanadka hadda.

```tus
keyd:tiro year = wakhti.sanad();
qor("Sanad: ");
qor(year);
```

**Soo-celinta:** `tiro` - Sanadka oo buuxa

## Tusaale

```tus
keen "wakhti";

qor("Wakhtiga hadda:");
qor("Saacad: " + nooc(wakhti.saacado()));
qor("Daqiiqad: " + nooc(wakhti.daqiiqado()));
qor("Ilbiriqsi: " + nooc(wakhti.sekeno()));

qor("Taariikhda:");
qor("Maalin: " + nooc(wakhti.maalin()));
qor("Bil: " + nooc(wakhti.bil()));
qor("Sanad: " + nooc(wakhti.sanad()));
```
