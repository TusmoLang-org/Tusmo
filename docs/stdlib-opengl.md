# Maktabadda OpenGL

Maktabadda **OpenGL** ee Tusmo waxay kuu oggolaanaysaa inaad dhisatid ciyaaro, animation-no, iyo muuqaallo 2D iyo 3D ah adigoo isticmaalaya luqadda Tusmo. Maktabaddani waxay si toos ah ula xiriirtaa nidaamka hoose ee OpenGL iyo GLFW.

## Sida loo soo daro (Importing)

Si aad u bilowdo isticmaalka OpenGL, ku dar koodkan bilowga faylkaaga:

```tusmo
keen "opengl/opengl";
```

---

## Kooxda Daaqad (Window Class)

Kooxdan waxay maamushaa daaqadda ciyaarta iyo socodka nidaamka.

### Hawlaha Daaqadda:

| Hawsha | Sharaxaadda |
| :--- | :--- |
| `fur(ballac, dheer, cinwaan)` | Bilaaba nidaamka oo fura daaqad cusub. |
| `ma_socotaa()` | Hubiya haddii daaqadu weli shaqaynayso (miyey_xirmaysaa). |
| `muuji()` | Soo muujiya wixii lagu sawiray shaashadda. |
| `hubi()` | Hubiya dhacdooyinka sida badhamada la riixayo. |
| `xir()` | Xira daaqadda oo nadiifiya nidaamka. |

---

## Kooxda Sawire (Renderer Class)

Kooxdan waxay xilsaaran tahay dhammaan hawlaha sawiridda iyo midabaynta.

### Hawlaha Sawiridda:

| Hawsha | Sharaxaadda |
| :--- | :--- |
| `midabka_masaxida(r, g, b, a)` | Dejiya midabka la isticmaalayo marka shaashadda la masaxayo. |
| `nadiifi(xusuusta)` | Masaxa shaashadda adigoo isticmaalaya xusuusta la siiyay. |
| `bilow(nooca)` | Bilaaba sawiridda shay cusub (sida `SADDEX_GEES`). |
| `dhameey()` | Dhamaystira sawiridda shayga hadda socday. |
| `bar_2d(x, y)` | Dejiya meesha (dhibicda) uu sawirku ka bilaabanayo. |
| `midab(r, g, b)` | Dejiya midabka shayga la sawirayo hadda. |
| `dib_u_deji()` | Dib u dejiya matrix-ka xisaabta ee sawiridda. |

---

## Halbeegyada (Constants)

Halbeegyadan waxaa loo isticmaalaa in OpenGL loo sheego nooca sawirka ama xusuusta la nadiifinayo.

*   **Noocyada Sawirka:** `SADDEX_GEES`, `AFAR_GEES`, `XARIIQYAAL`, `DHIBCO`.
*   **Xusuusta:** `XUSUUSTA_MIDABKA`, `XUSUUSTA_DHUMUCDA`.

---

## Tusaale: Sawiridda Saddex-gees

Kani waa tusaale fudud oo muujinaya sida loo furo daaqad iyo sida loo sawiro saddex-gees midabo leh:

```tusmo
keen "opengl/opengl";

// 1. Sameynta Daaqadda iyo Sawiraha
keyd:Daaqad daaqada = Daaqad() cusub;
keyd:Sawire sawire = Sawire() cusub;

// 2. Furitaanka Daaqadda
haddii (daaqada.fur(800, 600, "Ciyaartayda Koowaad")) {
    
    // Deji midabka masaxida (Madow khafiif ah)
    sawire.midabka_masaxida(0.05, 0.05, 0.05, 1.0);

    // 3. Loop-ka Ciyaarta
    inta ay (daaqada.ma_socotaa()) {
        
        // Nadiifi shaashadda
        sawire.nadiifi(XUSUUSTA_MIDABKA);
        
        // Dib u deji xisaabta Matrix-ka
        sawire.dib_u_deji();

        // 4. Sawiridda Saddex-gees midabo leh
        sawire.bilow(SADDEX_GEES);
            
            sawire.midab(1.0, 0.0, 0.0); // Cas
            sawire.bar_2d(0.0, 0.5);
            
            sawire.midab(0.0, 1.0, 0.0); // Cagaar
            sawire.bar_2d(-0.5, -0.5);
            
            sawire.midab(0.0, 0.0, 1.0); // Buluug
            sawire.bar_2d(0.5, -0.5);
            
        sawire.dhameey();

        // 5. Cusboonaysii shaashadda
        daaqada.muuji();
        daaqada.hubi();
    }
}

// 6. Xiritaanka
daaqada.xir();
```
