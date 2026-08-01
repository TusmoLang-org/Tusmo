# Bogga Hordhaca (Introduction)

Ku soo dhawaada dukumiintiyada rasmiga ah ee **Tusmo**! 

**Tusmo** waa luuqad high-level, oo ah **general-purpose** (loo adeegsan karo hawl kasta oo dhanka softiweerka ah), loona qaabeeyay in koodhkeeda lagu qoro **Af-Soomaali**. Luuqadani ma ahan mid loo dhisay barasho ama tijaabo kaliya, balse waa luuqad casri ah oo compiles-gareysa (transpiled) C code aad u dheereeya, una diyaarsan dhisidda barnaamijyada waaweyn, sida backend, GUI iyo ciyaaraha (games).

---

## Maxay Tahay Luuqadani?

Tusmo waa luuqad isku daraysa quruxda iyo fududaanta luuqadaha casriga ah (sida Python iyo Go) iyo xawaaraha iyo awoodda luuqadaha heerka hoose (sida C iyo C++). Compiler-ka Tusmo wuxuu koodhkaaga u turjumaa C code aad u nadiif ah, kaas oo markaas lagu compile-gareeyo **GCC compiler** iyadoo la adeegsanayo algorithms-ka optimizes-ka ugu sarreeya (`-O3 -march=native -flto`).

Waxanyaabaha ay caanka ku tahay Tusmo waxaa ka mid ah:
1. **Turjumaad toos ah oo C ah**: Barnaamijyada ku qoran Tusmo waxay u ordaan si la mid ah ama ka dhakhsaha badan barnaamijyada C-ga ceeriin ah ee caadiga ah.
2. **Maamulka Xusuusta ee Awoodda Badan (Memory Management)**: Tusmo ma laha *Garbage Collector* oo barnaamijka gaabiya, laakiin waxay leedahay nidaam **Automatic Move Semantics & Ownership** kaas oo si toos ah u xoreeya xusuusta marka uu dhammaado scope-ka keydiyaha (variable scope cleanup).
3. **Af-Soomaali Naxwe ahaan sax ah**: Erayada muhiimka ah (keywords) waxaa si taxadar leh loogu turjumay Af-Soomaali si naxwe ahaan iyo qaab ahaanba ay ugu habboonaadaan qof kasta oo Soomaali ah oo baranaya ama ku shaqaysanaya horumarinta softiweerka.

---

## Xawaaraha iyo Isticmaalka Xusuusta (Performance Benchmarks)

Si aan u tijaabino awoodda dhabta ah ee Tusmo, waxaan ku sameynay tijaabooyin rasmi ah (benchmarks) oo toos loogu orodsiiyey nidaamkaaga (**Kali Linux**, CPU xawaare sare leh, GCC `-O3` optimize) anagoo barbardhigayna xawaaraha socodsiinta iyo isticmaalka xusuusta saxda ah (Peak RSS RAM) ee luuqadaha **Tusmo**, **Python 3**, iyo **Rust**.

---

### 📊 Tijaabada 1aad: Xisaabinta Fibonacci (Recursion Benchmark)
Tijaabadani waxay cabbiraysaa xawaaraha CPU-ga iyo xusuusta ee recursion-ka dhowr jeer lagu celceliyo (**Fibonacci 38**):

| Luuqadda | Xawaaraha Socodsiinta (Seconds) | Isticmaalka Peak RAM (Memory) | Habka Socodsiinta (Execution Model) |
| :--- | :--- | :--- | :--- |
| **Python 3** | `9.16s` | `9.01 MB` | Interpreted (VM / Dynamic Bytecode) |
| **Tusmo (Af-Soomaali)** | **`0.11s`** | **`1.47 MB`** | **Compiled (Ahead-of-Time via C)** |
| **Rust** | `0.15s` | `2.08 MB` | Compiled (Ahead-of-Time via LLVM) |

*(Fiiro gaar ah: Tijaabadan waxaa si cilmiyeysan loogu cabbiray isolated C process memory harness `getrusage` oo toos looga orodsiyeey nidaamkaaga Kali Linux si meesha looga saaro wax kasta oo ka baxsan orodka barnaamijka).*

#### 💻 Koodhka Tijaabada (Fibonacci 38 Source Codes):

**Tusmo**
```tusmo
    hawl fibonacci(n: tiro) : tiro {
        haddii (n <= 1) {soo_celi n;}
        soo_celi fibonacci(n - 1) + fibonacci(n - 2);
    }

    hawl main() : waxbo {
        keyd:tiro tiro_fib = fibonacci(38);
        qor("Tusmo: ", tiro_fib);
    }
```

**Rust**
```rust
    fn fibonacci(n: u32) -> u32 {
        if n <= 1 {
            return n;
        }
        fibonacci(n - 1) + fibonacci(n - 2)
    }

    fn main() {
        let tiro_fib = fibonacci(38);
        println!("Rust: {}", tiro_fib);
    }
```

**Python**
```python
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    tiro_fib = fibonacci(38)
    print(f"Python: {tiro_fib}")
```

---

### 📊 Tijaabada 2aad: Gelinta iyo Habaynta Array (Memory Allocation Benchmark)
Tijaabadani waxay cabbiraysaa dhisidda iyo gelinta **1,000,000 (Hal milyan) oo xogood** oo ku jira tix (array allocation & push):

| Luuqadda | Xawaaraha Socodsiinta (Seconds) | Isticmaalka Peak RAM (Memory) | Maamulka Xusuusta (Memory Management) |
| :--- | :--- | :--- | :--- |
| **Python 3** | `0.164s` | `47.23 MB` | Garbage Collection (GC) pauses |
| **Tusmo (Af-Soomaali)** | **`0.005s`** | **`5.67 MB`** | **Automatic Scope Ownership (No GC)** |
| **Rust** | `0.008s` | `4.10 MB` | Ownership & Borrow Checker (No GC) |

#### 💻 Koodhka Tijaabada (Array 1M Push Source Codes):

**Tusmo**
```tusmo
hawl main() : waxbo {
    keyd:tix:tiro tixda = [];
    soco i laga bilaabo 1..1000000 {
        tixda.gali(i);
    }
    qor("Tusmo Array: ", dherer(tixda));
}
```

Rust
```rust
fn main() {
    let mut tixda = Vec::new();
    for i in 1..=1000000 {
        tixda.push(i);
    }
    println!("Rust Array: {}", tixda.len());
}
```

**Python**
```python
tixda = []
for i in range(1, 1000001):
    tixda.append(i)
print(f"Python Array: {len(tixda)}")
```

---

### 🔍 Falanqaynta Natiijooyinka:
* **Tusmo vs Python (Fibonacci & Array)**: Tusmo waxay ka dhakhsaha badan tahay Python in ka baxsan **83 jeer** dhanka recursion-ka, halka dhanka Array Allocation ay ka dhakhsaha badan tahay **32 jeer**, iyadoo isticmaalaysa xusuus (RAM) aad u yar (ku dhowaad **8 jeer** ka yar Python).
* **Tusmo vs Rust (Fibonacci & Array)**: Tusmo waxay si buuxda ula tartantaa luuqadda **Rust** dhanka xawaaraha labada tijaaboba (xitaa waxay ka yara xusuus yar tahay recursive-ka sababtoo ah compiler-keeda GCC wuxuu sameeyaa fine-tuned call-stack optimization). Labaduba waxay isticmaalaan maamul xusuuseed Scope-based ah oo aan lahayn Garbage Collector oo barnaamijka gaabiya.

---

## Hadafka Luuqada

Tusmo waxaa loo dhisay si ay u xalliso dhowr dhibaatooyin oo waaweyn oo ka jira deegaanka tiknoolajiyadda Soomaalida iyo caalamkaba:

* **Burburinta Caqabadda Luuqada**: Barashada koodhka iyo fikirka kumbuyuutarka (computational thinking) waxaa badanaa caqabad ku noqda luuqadda Ingiriisiga. Tusmo waxay u sahlaysaa ardayda, macallimiinta, iyo horumariyeyaasha Soomaaliyeed inay si toos ah koodhka ugu bartaan luuqadooda hooyo.
* **Xawaare Sare iyo Fududaan**: Inta badan luuqadaha bilowga loo isticmaalo (sida Python) waa kuwo gaabis ah. Tusmo waxay bixisaa fududaantaas laakiin leh xawaaraha C code oo compiles-garaysan.
* **Qani ku ah Maktabado (Rich Standard Library)**: Tusmo waxay toos ula timaadaa maktabado diyaarsan oo laguu dhisay sida:
  - **Raylib**: Dhisidda ciyaaraha 2D/3D iyo interface-yada sawirka leh (GUI).
  - **Awr**: Express-style web framework oo loogu talagalay in lagu dhiso server-ka web-ka ee casriga ah (web APIs).
  - **Sockets & WebSockets**: Isgaarsiinta aasaasiga ah ee internetka iyo is-dhaafsiga xogta tooska ah (real-time chat messaging).

---

## Tusaale Kooban: Hello World

Aan aragno barnaamijka ugu caansan ee barashada luuqadaha, "Hello World" oo ku qoran Tusmo:

```tusmo
// Tusaalaha ugu horreeya ee Tusmo
hawl main() : waxbo {
    qor("Haye adduun! Tani waa luuqadda rasmiga ah ee Tusmo.");
}
```

Haddii aad rabto inaad si toos ah u qorto koodh adigoon abuurin shaqada `main()`, Tusmo waxay sidoo kale taageertaa **Global Scripting Mode** (koodhku wuxuu u socdaa si toos ah isagoo aan lagu dhex qorin shaqo):

```tusmo
qor("Ku soo dhawaada Tusmo! Halkan koodhku wuxuu ku soconayaa si toos ah.");
```

---

## Muuqaal Ka Weyn: Xisaabinta Tirada Fibonacci

Si loo arko sida ay u fududahay dhisidda algorithms-ka adag, ka eeg tusaalahan xisaabinta tirada Fibonacci:

```tusmo
hawl fibonacci(n: tiro) : tiro {
    haddii (n <= 1) {
        soo_celi n;
    }
    soo_celi fibonacci(n - 1) + fibonacci(n - 2);
}

hawl main() : waxbo {
    keyd:tiro tiro_fib = fibonacci(10);
    qor("Fibonacci tirada 10-aad waa: ", tiro_fib);
}
```

Hadafkayagu waa inaan kugu hoggaaminno barashada aasaaska ilaa heerka ugu sarreeya ee luuqadan aadka u awoodda badan! Mid-mid u akhri boggaga xiga si aad u bilowdo safarkaaga.
