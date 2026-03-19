# Wakhti Module

The Wakhti module provides time and date functions.

## Import

```tus
keen "wakhti";
```

## Methods

### hadda()

Get current Unix timestamp.

```tus
keyd:jajab now = wakhti.hadda();
qor("Timestamp: ");
qor(now);
```

**Returns:** `jajab` - Unix timestamp (seconds since epoch)

---

### qaab(format)

Format current time.

```tus
keyd:eray formatted = wakhti.qaab("%Y-%m-%d %H:%M:%S");
qor(formatted);  // e.g., "2024-01-15 10:30:45"
```

**Parameters:**
- `format` (eray) - Format string

**Format specifiers:**
| Code | Description |
|------|-------------|
| `%Y` | Year (4 digits) |
| `%m` | Month (01-12) |
| `%d` | Day (01-31) |
| `%H` | Hour (00-23) |
| `%M` | Minute (00-59) |
| `%S` | Second (00-59) |

**Returns:** `eray` - Formatted time string

---

### sekeno()

Get current seconds (0-59).

```tus
keyd:tiro sec = wakhti.sekeno();
qor("Seconds: ");
qor(sec);
```

**Returns:** `tiro` - Seconds (0-59)

---

### daqiiqado()

Get current minutes (0-59).

```tus
keyd:tiro min = wakhti.daqiiqado();
qor("Minutes: ");
qor(min);
```

**Returns:** `tiro` - Minutes (0-59)

---

### saacado()

Get current hours (0-23).

```tus
keyd:tiro hr = wakhti.saacado();
qor("Hour: ");
qor(hr);
```

**Returns:** `tiro` - Hours (0-23)

---

### maalin()

Get current day of month (1-31).

```tus
keyd:tiro day = wakhti.maalin();
qor("Day: ");
qor(day);
```

**Returns:** `tiro` - Day (1-31)

---

### bil()

Get current month (1-12).

```tus
keyd:tiro month = wakhti.bil();
qor("Month: ");
qor(month);
```

**Returns:** `tiro` - Month (1-12)

---

### sanad()

Get current year.

```tus
keyd:tiro year = wakhti.sanad();
qor("Year: ");
qor(year);
```

**Returns:** `tiro` - Full year

## Example

```tus
keen "wakhti";

qor("Current time:");
qor("Hour: " + nooc(wakhti.saacado()));
qor("Minute: " + nooc(wakhti.daqiiqado()));
qor("Second: " + nooc(wakhti.sekeno()));

qor("Date:");
qor("Day: " + nooc(wakhti.maalin()));
qor("Month: " + nooc(wakhti.bil()));
qor("Year: " + nooc(wakhti.sanad()));
```
