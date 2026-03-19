# OS Module

The OS module provides file system and system operations.

## Import

```tus
keen "os";
```

## Methods

### halkee()

Get the current working directory.

```tus
keyd:eray cwd = os.halkee();
qor(cwd);
```

**Returns:** `eray` - Current directory path

---

### u_guur(folder)

Change directory.

```tus
os.u_guur("/path/to/folder");
```

**Parameters:**
- `folder_kee_aadaa` (eray) - Path to change to

---

### itus(path)

List directory contents.

```tus
keyd:tix:eray files = os.itus("/path/to/folder");
soco item kasta laga helo files {
    qor(item);
}
```

**Parameters:**
- `folder_kee_ku_tusiyaa_waxa_ku_jira` (eray) - Directory path

**Returns:** `tix:eray` - Array of file/folder names

---

### abuur_folder(path)

Create a directory.

```tus
os.abuur_folder("myfolder");
```

**Parameters:**
- `path` (eray) - Path to create

---

### tirtir_folder(path)

Remove a directory.

```tus
os.tirtir_folder("myfolder");
```

**Parameters:**
- `path` (eray) - Path to remove

---

### tirtir_fayl(path)

Delete a file.

```tus
os.tirtir_fayl("file.txt");
```

**Parameters:**
- `path` (eray) - File path to delete

---

### majiraa(path)

Check if path exists.

```tus
keyd:miyaa exists = os.majiraa("file.txt");
haddii (exists) {
    qor("File exists!");
}
```

**Parameters:**
- `path` (eray) - Path to check

**Returns:** `miyaa` - haa if exists, maya otherwise

---

### fayl_miyaa(path)

Check if path is a file.

```tus
keyd:miyaa isFile = os.fayl_miyaa("file.txt");
```

**Parameters:**
- `path` (eray) - Path to check

**Returns:** `miyaa` - haa if file, maya otherwise

---

### folder_miyaa(path)

Check if path is a directory.

```tus
keyd:miyaa isDir = os.folder_miyaa("folder");
```

**Parameters:**
- `path` (eray) - Path to check

**Returns:** `miyaa` - haa if directory, maya otherwise

---

### hel_deegaan(name)

Get environment variable.

```tus
keyd:eray path = os.hel_deegaan("PATH");
qor(path);
```

**Parameters:**
- `name` (eray) - Variable name

**Returns:** `eray` - Variable value

---

### deji_deegaan(name, value)

Set environment variable.

```tus
os.deji_deegaan("MY_VAR", "hello");
```

**Parameters:**
- `name` (eray) - Variable name
- `value` (eray) - Variable value

---

### fuli(command)

Execute shell command.

```tus
keyd:tiro result = os.fuli("ls -la");
```

**Parameters:**
- `command` (eray) - Shell command

**Returns:** `tiro` - Exit code

---

### koobi(source, destination)

Copy file.

```tus
os.koobi("source.txt", "dest.txt");
```

**Parameters:**
- `source` (eray) - Source file path
- `destination` (eray) - Destination file path

---

### nuqul(source, destination)

Alias for `koobi` - copy file.

```tus
os.nuqul("source.txt", "dest.txt");
```

---

### u_dhaqaaji(old_path, new_path)

Move or rename file/folder.

```tus
os.u_dhaqaaji("old.txt", "new.txt");
```

**Parameters:**
- `old_path` (eray) - Current path
- `new_path` (eray) - New path

---

### aqri_fayl(path)

Read file contents.

```tus
keyd:eray content = os.aqri_fayl("file.txt");
qor(content);
```

**Parameters:**
- `path` (eray) - File path

**Returns:** `eray` - File contents

---

### qor_fayl(path, content, append)

Write to file.

```tus
// Write (overwrite)
os.qor_fayl("file.txt", "Hello", maya);

// Append
os.qor_fayl("file.txt", " World", haa);
```

**Parameters:**
- `path` (eray) - File path
- `content` (eray) - Content to write
- `append` (miyaa) - haa to append, maya to overwrite

---

### isku_dar_waddo(part1, part2)

Join path parts.

```tus
keyd:eray full = os.isku_dar_waddo("folder", "file.txt");
qor(full);  // "folder/file.txt"
```

**Parameters:**
- `part1` (eray) - First path part
- `part2` (eray) - Second path part

**Returns:** `eray` - Joined path

---

### cabbir_fayl(path)

Get file size in bytes.

```tus
keyd:tiro size = os.cabbir_fayl("file.txt");
qor("File size: " + nooc(size));
```

**Parameters:**
- `path` (eray) - File path

**Returns:** `tiro` - File size in bytes
