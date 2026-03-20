# Tusmo

Luuqad barnaamij Soomaaliyeed oo u turjunta C.

## Waa maxay Tusmo?

Tusmo waa luuqad barnaamij oo statically-typed ah taas oo isticmaasha keywords Soomaali ah. Waxaa Tusmo loo badalaa C code ka dib binary fayl, kaas oo la excute-kareen karo.

## Bilaabid Degdeg ah
### Talo 
Kahor inta aadan la soo dagin tusmo fadlan soo dagso VScode si aad u hesho **syntax highlighter** iyo **DocHover**

### Linux/macOS

```bash
# ku soo dagso Tusmo linux-kaada ama macos-kaada
curl -fsSL https://raw.githubusercontent.com/Tusmolang/Tusmo/main/install.sh | bash
```

### Windows

```powershell
# Soo dagso Tusmo windwon adigoo u maraayo powershel-ka qab administration-ka
irm https://raw.githubusercontent.com/Tusmolang/Tusmo/main/install.ps1 | iex
```

```tus
// hello.tus
qor("Hello, Somaali developers!");
```

## Run-karee Tusmo file
```tus
# kani wuxuu soo saari donaa binary fayl
tusmo hello.tus

#kadib run-garee binary fayl-ka
./hello
```


## Astaamaha

* **Naxwaha Soomaaliga** - Ereyo Soomaali ah oo dhalad ah (`keyd`, `haddii`, `soco`, `koox`)
* **Noocyo Sugan (Static Typing)** - Is-beddeleyaasha (Variables) waxay leeyihiin noocyo cad
* **Ku-salaysnaan Walxeed (Object-Oriented)** - Kooxo (Classes) leh dhaxal
* **Qashin-gur (Garbage Collection)** - Maareyn xusuuseed oo iskeed u shaqeysa
* **Maktabadda Caadiga ah (Standard Library)** - Akhrinta/qorista faylasha, HTTP, xiriiriyeyaal (sockets), waqti, iyo nasiib (random)

## Tusaalaha Luuqadda

```tus
// variables
keyd:eray magac = "Tusmo";
keyd:tiro da = 5;

// Shuruudo
haddii (da > 3) {
    qor("Waa weyn!");
}

// Wareegyo
soco i laga bilaabo 0 .. 5 {
    qor(i);
}

// Hawlo (Functions)
hawl greet(name: eray) : waxbo {
    qor("Soo dhawow " + name);
}

// Kooxo (Classes)
koox Qof {
    keyd:eray name;
    
    dhis(n: eray) : waxbo {
        kan.name = n;
    }
    hawl sooBandhig() : waxbo {
        qor("Magacaygu waa " + kan.name);
    }
}

keyd:Qof p1 = Qof("Ali") cusub;
p1.sooBandhig();
greet("Mubaarak");
```

## Dukumiintiyada

Aqriso Documentation-ka Tusmo oo booqo: **[Dukumiintiyada Tusmo](https://tusmolang.github.io/Tusmo/)**

### Bilaabidda
* [Rakibidda](https://tusmolang.github.io/Tusmo/getting-started)
* [Sida ay u shaqeyso](https://tusmolang.github.io/Tusmo/how-it-works)

### Tixraaca Luuqadda
* [Is-beddeleyaal (Variables)](https://tusmolang.github.io/Tusmo/variables)
* [Xargo (Strings)](https://tusmolang.github.io/Tusmo/strings)
* [Tixo (Arrays)](https://tusmolang.github.io/Tusmo/arrays)
* [Qaamuusyo (Dictionaries)](https://tusmolang.github.io/Tusmo/dictionaries)
* [Shuruudo (Conditions)](https://tusmolang.github.io/Tusmo/conditions)
* [Wareegyo (Loops)](https://tusmolang.github.io/Tusmo/loops)
* [Hawlo (Functions)](https://tusmolang.github.io/Tusmo/functions)
* [Kooxo (Classes)](https://tusmolang.github.io/Tusmo/classes)
* [Hawl-galayaal (Operators)](https://tusmolang.github.io/Tusmo/operators)

### Maktabadda Caadiga ah (Standard Library)
* [Dulmarka Maktabadda Caadiga ah](https://tusmolang.github.io/Tusmo/stdlib)
* [Qaybta OS (Nidaamka)](https://tusmolang.github.io/Tusmo/stdlib-os)
* [Wakhti (Time)](https://tusmolang.github.io/Tusmo/stdlib-wakhti)
* [Nasiib (Random)](https://tusmolang.github.io/Tusmo/stdlib-nasiib)
* [Xiriiriye (Sockets)](https://tusmolang.github.io/Tusmo/stdlib-xiriiriye)
* [WebXiriiriye (WebSocket)](https://tusmolang.github.io/Tusmo/stdlib-webxiriiriye)
* [HTTP](https://tusmolang.github.io/Tusmo/stdlib-http)



## Shatiga (License)

MIT

---

Ugu dambeyntii luuqadan Tusmo waxay wali ku jirtaa under development Fadlan wixii cilado ah nooc kastaba ay ahaadaan 
