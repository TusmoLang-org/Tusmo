---
title: Tusmo Documentation
description: Tusmo is a Somali static programming language that compiles to C for fast native binaries.
---

# Tusmo Language Documentation

Tusmo waa **Somali programming language** oo loo dhisay in ay noqoto mid sahlan in la barto, balse awood leh marka la gaadho production.

Tusmo language waxay isku darsatay:

- Syntax Soomaali ah (`keyd`, `haddii`, `soco`, `koox`)
- Static typing (type safety)
- Compilation to C -> native binary (performance fiican)
- Standard library ku habboon apps dhab ah (OS, HTTP, sockets, time, random)

## Why Tusmo (Developer + Leadership View)

Tusmo waxay ku habboon tahay kooxo raba:

- In ay barnaamijyada ku qoraan Af-Soomaali si onboarding-ku u fududaado
- In ay dhisaan software leh predictable performance
- In ay helaan luqad waxbarasho + luqad shaqo oo isku mar ah
- In ay yeeshaan ecosystem maxalli ah oo Somali developers ah

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash

```

`hello.tus`:

```tus
qor("Hello, Somali Developers!");
```

```bash
# Run
tusmo hello.tus
```


## Documentation Roadmap

- [Getting Started](getting-started.md)
- [How Tusmo Works](how-it-works.md)
- [Variables](variables.md)
- [Strings](strings.md)
- [Arrays](arrays.md)
- [Dictionaries](dictionaries.md)
- [Conditions](conditions.md)
- [Loops](loops.md)
- [Functions](functions.md)
- [Classes](classes.md)
- [Operators](operators.md)
- [Standard Library](stdlib.md)

## Standard Library Modules

- [OS](stdlib-os.md)
- [Wakhti (Time)](stdlib-wakhti.md)
- [Nasiib (Random)](stdlib-nasiib.md)
- [Xiriiriye (Sockets)](stdlib-xiriiriye.md)
- [WebXiriiriye (WebSocket)](stdlib-webxiriiriye.md)
- [HTTP](stdlib-http.md)


