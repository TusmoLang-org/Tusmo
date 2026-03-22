# Kooxaha (Classes)

Tusmo waxay taageertaa barnaamijka ku salaysan waxa af-ka qalaad lagu yiraahdo oop (object-oriented programming) iyadoo la isticmaalayo keyword-ka `koox`.

## Qeexidda Kooxda (Class Definition)

```tus
koox Qof {
    keyd:eray magac;
    keyd:tiro da'da;
    
    dhis(n: eray) : waxbo {
        kan.magac = n;
        kan.da'da = 0;
    }
    
    hawl soo_dhah() : waxbo {
        qor("Magaca: " + kan.magac);
    }
    
    hawl setAge(a: tiro) : waxbo {
        kan.da'da = a;
    }
    
    hawl getAge() : tiro {
        soo_celi kan.da'da;
    }
}
```

## Sameynta Instance

U isticmaal keyword-ka `cusub` si aad u sameyso instance cusub:

```tus
keyd:Qof p1 = Qof("Ali") cusub;
p1.setAge(25);
p1.soo_dhah();
qor(p1.getAge());
```

## Constructor

Habka `dhis` wuxuu u shaqeeyaa sidii constructor:

```tus
dhis(n: eray) : waxbo {
    kan.magac = n;
    kan.da'da = 0;
}
```

## Tixraaca Nafsiyi (Self Reference)

U isticmaal `kan` si aad u tixraacdo instance-ka hadda jooga:

```tus
kan.magac = n;
kan.da'da = a;
soo_celi kan.da'da;
```

## Dhaxalka (Inheritance)

U isticmaal keyword-ka `dhaxlaya` si aad u dhaxasho koox kale:

```tus
koox Baabuur {
    keyd:tiro taayiro;
    keyd:eray nooca;

    dhis(t: tiro) : waxbo {
        kan.taayiro = t;
        kan.nooca = "Baabuur";
    }

    hawl socoshada() : waxbo {
        qor("Baabuur wuu socdaa");
    }
}

koox Toyota dhaxlaya Baabuur {
    keyd:eray model;

    dhis(m: eray) : waxbo {
        waalid.dhis(4);
        kan.model = m;
    }
    
    hawl socoshada() : waxbo {
        waalid.socoshada();
        qor("Toyota " + kan.model);
    }
}
```

U isticmaal `waalid` si aad u tixraacdo kooxda waalidka ah (parent class):

```tus
waalid.socoshada();  // Wac habka waalidka
```

## Tusaale Dhammaystiran

```tus
koox Ciyaaryahan {
    keyd:eray magac;
    keyd:miyaa nolol;
    keyd:tiro dhibco;
    
    dhis(n: eray) : waxbo {
        kan.magac = n;
        kan.nolol = haa;
        kan.dhibco = 0;
    }
    
    hawl ku_dhac() : waxbo {
        kan.nolol = maya;
    }
    
    hawl ku_dar_dhibco(dhibco: tiro) : waxbo {
        kan.dhibco = kan.dhibco + dhibco;
    }
    
    hawl ma_nool_yahay() : miyaa {
        soo_celi kan.nolol;
    }
    
    hawl hel_dhibco() : tiro {
        soo_celi kan.dhibco;
    }
}

keyd:Ciyaaryahan ciyaaryahan = Ciyaaryahan("Halyeey") cusub;
qor(ciyaaryahan.magac);
qor(" ma nool yahay: ");
qor(ciyaaryahan.ma_nool_yahay());
ciyaaryahan.ku_dhac();
ciyaaryahan.ku_dar_dhibco(100);
qor("Dhibcaha: ");
qor(ciyaaryahan.hel_dhibco());
```

## Keyword-yada Kooxda

| Keyword | Sharaxaad |
|---------|-------------|
| `koox` | Sheegista kooxda |
| `dhaxlaya` | Keyword-ka dhaxalka |
| `waalid` | Tixraaca kooxda waalidka |
| `cusub` | Sameynta instance cusub |
| `kan` | Tixraaca naftiisa |
| `dhis` | Constructor ama dhise |
| `hawl / shaqo` | Sheegista habka (method) |
