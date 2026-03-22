# Module-ka OS

Module-ka OS wuxuu bixiyaa nidaamka faylka iyo hawlgallada nidaamka.

## Keenista (Import)

```tus
keen "os";
```

## Hababka (Methods)

### halkee()

Hel directory-ga shaqada ee hadda (current working directory).

```tus
keyd:eray cwd = os.halkee();
qor(cwd);
```

**Soo-celinta:** `eray` - Wadada directory-ga hadda

---

### u_guur(folder)

Beddel directory-ga.

```tus
os.u_guur("/path/to/folder");
```

**Halbeegyada:**
- `folder` (eray) - Wadada loo guurayo

---

### itus(wadada)

Liis gareey waxyaabaha ku jira directory-ga.

```tus
keyd:tix:eray files = os.itus("/path/to/folder");
soco item kasta laga helo files {
    qor(item);
}
```

**Halbeegyada:**
- `wadada` (eray) - Wadada directory-ga

**Soo-celinta:** `tix:eray` - Tix ka kooban magacyada faylka/folder-ka

---

### abuur_folder(wadada)

Abuur directory cusub.

```tus
os.abuur_folder("myfolder");
```

**Halbeegyada:**
- `wadada` (eray) - Wadada la abuurayo

---

### tirtir_folder(wadada)

Ka saar (tirtir) directory.

```tus
os.tirtir_folder("myfolder");
```

**Halbeegyada:**
- `wadada` (eray) - Wadada la tirtirayo

---

### tirtir_fayl(wadada)

Tirtir fayl.

```tus
os.tirtir_fayl("file.txt");
```

**Halbeegyada:**
- `wadada` (eray) - Wadada faylka la tirtirayo

---

### majiraa(wadada)

Hubi haddii wadadu jirto.

```tus
keyd:miyaa exists = os.majiraa("file.txt");
haddii (exists) {
    qor("Faylku waa jiraa!");
}
```

**Halbeegyada:**
- `wadada` (eray) - Wadada la hubinayo

**Soo-celinta:** `miyaa` - haa haddii uu jiro, maya haddii kale

---

### fayl_miyaa(wadada)

Hubi haddii uu yahay fayl jira.

```tus
keyd:miyaa isFile = os.fayl_miyaa("file.txt");
```

**Halbeegyada:**
- `wadada` (eray) - Wadada la hubinayo

**Soo-celinta:** `miyaa` - haa haddii uu yahay fayl, maya haddii kale

---

### folder_miyaa(wadada)

Hubi haddii uu yahay directory (folder) jira.

```tus
keyd:miyaa isDir = os.folder_miyaa("folder");
```

**Halbeegyada:**
- `wadada` (eray) - Wadada la hubinayo

**Soo-celinta:** `miyaa` - haa haddii uu yahay folder, maya haddii kale

---

### hel_deegaan(magac)

Hel doorsoomaha deegaanka (environment variable).

```tus
keyd:eray path = os.hel_deegaan("PATH");
qor(path);
```

**Halbeegyada:**
- `magac` (eray) - Magaca doorsoomaha

**Soo-celinta:** `eray` - Qiimaha doorsoomaha

---

### deji_deegaan(magac, qiimo)

Deji doorsoomaha deegaanka.

```tus
os.deji_deegaan("MY_VAR", "hello");
```

**Halbeegyada:**
- `magac` (eray) - Magaca doorsoomaha
- `qiimo` (eray) - Qiimaha doorsoomaha

---

### fuli(amar)

Fuli amarka shell-ka.

```tus
keyd:tiro natiijo = os.fuli("ls -la");
```

**Halbeegyada:**
- `amar` (eray) - Amarka shell-ka

**Soo-celinta:** `tiro` - Exit code

---

### koobi(il, meel)

Koobiyeey fayl.

```tus
os.koobi("source.txt", "dest.txt");
```

**Halbeegyada:**
- `il` (eray) - Wadada faylka asalka ah
- `meel` (eray) - Wadada meesha loo koobiyeynayo

---

### nuqul(il, meel)

Waa la mid koobi - koobiyeey fayl.

```tus
os.nuqul("source.txt", "dest.txt");
```

---

### u_dhaqaaji(wadadii_hore, wadada_cusub)

Dhaqaaji ama dib u magacow faylka/folder-ka.

```tus
os.u_dhaqaaji("old.txt", "new.txt");
```

**Halbeegyada:**
- `wadadii_hore` (eray) - Wadada hadda
- `wadada_cusub` (eray) - Wadada cusub

---

### aqri_fayl(wadada)

Akhri nuxurka faylka.

```tus
keyd:eray content = os.aqri_fayl("file.txt");
qor(content);
```

**Halbeegyada:**
- `wadada` (eray) - Wadada faylka

**Soo-celinta:** `eray` - Nuxurka faylka

---

### qor_fayl(wadada, nuxur, ku_dar)

Wax ku qor faylka.

```tus
// Qor (dib u qor)
os.qor_fayl("file.txt", "Hello", maya);

// Ku dar (append)
os.qor_fayl("file.txt", " World", haa);
```

**Halbeegyada:**
- `wadada` (eray) - Wadada faylka
- `nuxur` (eray) - Waxa la qorayo
- `ku_dar` (miyaa) - haa haddii aad ku darayso, maya haddii aad dib u qorayso

---

### isku_dar_waddo(qayb1, qayb2)

Isku dar qaybaha wadada.

```tus
keyd:eray full = os.isku_dar_waddo("folder", "file.txt");
qor(full);  // "folder/file.txt"
```

**Halbeegyada:**
- `qayb1` (eray) - Qaybta koowaad ee wadada
- `qayb2` (eray) - Qaybta labaad ee wadada

**Soo-celinta:** `eray` - Wadada isku dhafan

---

### cabbir_fayl(wadada)

Hel baaxadda faylka oo byte ah.

```tus
keyd:tiro size = os.cabbir_fayl("file.txt");
qor("Baaxadda faylka: " + nooc(size));
```

**Halbeegyada:**
- `wadada` (eray) - Wadada faylka

**Soo-celinta:** `tiro` - Baaxadda faylka oo byte ah
