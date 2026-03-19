# Classes

Tusmo supports object-oriented programming with classes using the `koox` keyword.

## Class Definition

```tus
koox Qof {
    keyd:eray name;
    keyd:tiro age;
    
    dhis(n: eray) : waxbo {
        kan.name = n;
        kan.age = 0;
    }
    
    hawl soo_dhah() : waxbo {
        qor("Name: " + kan.name);
    }
    
    hawl setAge(a: tiro) : waxbo {
        kan.age = a;
    }
    
    hawl getAge() : tiro {
        soo_celi kan.age;
    }
}
```

## Create Instance

Use `cusub` keyword to create a new instance:

```tus
keyd:Qof p1 = Qof("Ali") cusub;
p1.setAge(25);
p1.soo_dhah();
qor(p1.getAge());
```

## Constructor

The `dhis` method acts as the constructor:

```tus
dhis(n: eray) : waxbo {
    kan.name = n;
    kan.age = 0;
}
```

## Self Reference

Use `kan` to refer to the current instance:

```tus
kan.name = n;
kan.age = a;
soo_celi kan.age;
```

## Inheritance

Use `dhaxlaya` keyword for inheritance:

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

Use `waalid` to reference the parent class:

```tus
waalid.socoshada();  // Call parent method
```

## Complete Example

```tus
koox Player {
    keyd:eray name;
    keyd:miyaa alive;
    keyd:tiro score;
    
    dhis(n: eray) : waxbo {
        kan.name = n;
        kan.alive = haa;
        kan.score = 0;
    }
    
    hawl hit() : waxbo {
        kan.alive = maya;
    }
    
    hawl addScore(points: tiro) : waxbo {
        kan.score = kan.score + points;
    }
    
    hawl isAlive() : miyaa {
        soo_celi kan.alive;
    }
    
    hawl getScore() : tiro {
        soo_celi kan.score;
    }
}

keyd:Player player = Player("Hero") cusub;
qor(player.name);
qor(" is alive: ");
qor(player.isAlive());
player.hit();
player.addScore(100);
qor("Score: ");
qor(player.getScore());
```

## Class Keywords

| Keyword | Description |
|---------|-------------|
| `koox` | Class declaration |
| `dhaxlaya` | Inheritance keyword |
| `waalid` | Parent class reference |
| `cusub` | Create new instance |
| `kan` | Self reference |
| `dhis` | Constructor |
| `hawl` | Method declaration |
