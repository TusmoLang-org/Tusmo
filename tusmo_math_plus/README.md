# Tusmo Math Plus

Maktabad xisaabeed oo lagu daro Tusmo:
- `isku_dar`, `celcelis`, `ugu_yar`, `ugu_weyn`
- `gcd`, `lcm`, `factorial`
- `xadid` (clamp), `lerp`
- `darajo_ilaa_rad`, `rad_ilaa_darajo`

## Isticmaal
```
keen "math_plus.tus";

keyd:tix:tiro t = [1, 2, 3, 4];
qor(isku_dar(t));      // 10
qor(celcelis(t));      // 2.5
qor(gcd(18, 24));      // 6
qor(lcm(6, 8));        // 24
qor(factorial(5));     // 120
```

## Rakibid (ku-meel-gaar, ilaa kataloogga rasmiga ahi ka socdo)
1. Nuqul galka `tusmo_math_plus/` ee mashruucaaga.
2. Orod: `mkdir -p .lib && cp -r tusmo_math_plus .lib/`
3. Xagga code-ka: `keen "math_plus/math_plus.tus";`

Marka kataloogga TusmoLang-org/index lagu daro, waxaad isticmaali kartaa:
```
tusmo dagso tusmo_math_plus
```

## Shuruudaha
- Tusmo v0.0.36 ama ka sarre (si `dagso` u shaqeyso marka lagu daro kataloogga rasmiga ah).
