# Nasiib Module

The Nasiib module provides random number generation.

## Import

```tus
keen "nasiib";
```

Initialize before use (optional - automatic):

```tus
nasiib.bilaab_nasiib();
```

## Functions

### bilaab_nasiib()

Initialize the random number generator. Call once before using other functions.

```tus
nasiib.bilaab_nasiib();
```

**Returns:** `waxbo`

---

### nasiib_tiro(min, max)

Generate random integer between min and max (inclusive).

```tus
keyd:tiro num = nasiib.tiro(1, 100);
qor("Random: ");
qor(num);  // 1-100
```

**Parameters:**
- `ugu_yaraan` (tiro) - Minimum value
- `ugu_badnaan` (tiro) - Maximum value

**Returns:** `tiro` - Random integer

---

### nasiib_jajab(min, max)

Generate random float between min and max.

```tus
keyd:jajab num = nasiib.jajab(0.0, 1.0);
qor("Random float: ");
qor(num);  // e.g., 0.456789
```

**Parameters:**
- `ugu_yaraan` (jajab) - Minimum value
- `ugu_badnaan` (jajab) - Maximum value

**Returns:** `jajab` - Random float

## Example

```tus
keen "nasiib";

nasiib.bilaab_nasiib();

// Random integer 1-10
keyd:tiro num1 = nasiib.tiro(1, 10);
qor("Dice roll: ");
qor(num1);

// Random float 0-1
keyd:jajab num2 = nasiib.jajab(0.0, 1.0);
qor("Random float: ");
qor(num2);
```
