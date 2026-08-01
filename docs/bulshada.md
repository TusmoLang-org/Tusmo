# Ka Qaybqaadashada (Community & Contributing)

Tusmo waa luuqad furan (**Open Source**) oo loo dhisay in bulshada Soomaaliyeed ee tiknoolajiyadda ay si wada jir ah u horumariyaan. Waxaan aaminsanahay in wada-shaqayntu ay tahay wadada kaliya ee lagu gaari karo luuqad horumarsan, qani ah, oo waarta.

---

## Xeerarka Horumarinta (Contributing Guidelines)

Haddii aad rabto inaad wax ku biiriso luuqadda Tusmo, waxaad gacan ka geysan kartaa qaybo badan:

1. **Maktabadda Caadiga ah (`stdlib/`)**: Waxaad qori kartaa maktabado cusub oo wax ku ool ah (tusaale: maareynta faylasha gaarka ah, algorithms-ka xogta, iwm).
2. **Cilad-bixin (Bug Fixing)**: Haddii aad aragto semantic checks oo aan sax ahayn ama runtime errors dhici kara, waxaad furi kartaa *Pull Request* si aad u saxdo.
3. **Dukumiintiyada (Documentation)**: Caawi turjumaadda ama ku darista tusaalooyin cusub oo koodh ah oo loogu talagalay boggaga rasmiga ah ee dukumiintiyada.
4. **Agabka (Tooling)**: Horumari LSP server-ka ama VS Code extension-ka si ay u taageeraan astaamo cusub oo editor-ka dhexdiisa ah.

### Habka loo soo diro isbeddelka:
- Fork gareey repo-ga rasmiga ah: `https://github.com/TusmoLang-org/Tusmo`.
- Abuur branch cusub oo sharraxaya waxaad qabanayso: `git checkout -b ku-dar-maktabad-cusub`.
- Qor koodhkaaga, hubina in dhammaan tests-ka ay si guul ah u gudbayaan.
- Fur *Pull Request (PR)* adigoo si faahfaahsan u sharraxaya waxa uu isbeddelkaagu qabanayo.

---

## Sida loo maamulo Dukumiintiyada (MkDocs & GitHub Hosting)

Dukumiintiyadan aad hadda akhrinayso waxaa loo habeeyay qaabka casriga ah ee **MkDocs (Material Theme)**. Waxaad si aad u fudud ugu tijaabin kartaa kombuyuutarkaaga ama ugu martigelin kartaa shabakadda:

### 1. Socodsiinta kombuyuutarkaaga (Local Preview)
Waxaad u baahantahay in `mkdocs` iyo `mkdocs-material` ay kuu rakiban yihiin:
```bash
# Ku rakib MkDocs iyo Material Theme adoo adeegsanaya pip
pip install mkdocs mkdocs-material

# Ka bilow server-ka preview-ga maxalliga ah (local server)
mkdocs serve
```
Fur cinwaanka `http://127.0.0.1:8000` si aad u aragto dukumiintiyada oo si qurux badan u naqshadaysan oo leh dark mode, dynamic tabs, iyo syntax midab leh!

### 2. Martigelinta GitHub Pages (GitHub Hosting)
Haddii aad leedahay xuquuqda maamulka (repository admin), waxaad si toos ah dukumiintiyadan ugu daabici kartaa GitHub Pages adigoo orodaya hal amar oo kaliya:
```bash
mkdocs gh-deploy
```
MkDocs wuxuu si toos ah u dhisayaa faylalka HTML wuxuuna u push-garaynayaa branch-ka `gh-pages` ee repo-gaaga si website-ku u noqdo mid toos ah!

---

## FAQ (Su'aalaha Badanaa la is-weydiiyo)

### S. Luuqaddu ma tahay mid *general-purpose* ah?
**J.** Haa, Tusmo waa luuqad *general-purpose* ah. Ma ahan mid loogu talagalay barashada aasaaska softiweerka oo kaliya. Waxaad u adeegsan kartaa inaad ku dhisto adeegyo shabakadeed oo casri ah (HTTP Web Servers), ciyaaro (games), CLI tools, iyo xitaa algorithms-ka xisaabinta ee aadka u adag.

### S. Sidee u shaqeeyaa maamulka xusuusta (GC-free) maadaama uusan jirin Garbage Collector?
**J.** Tusmo waxay adeegsataa hannaanka **Deterministic Ownership** oo aad ugu dhow kan luuqadda Rust. Marka aad qeexdo keydiyaha dynamic-ga ah (sida array ama string), compiler-ka Tusmo wuxuu ogyahay scope-ka uu ku nool yahay. Marka scope-kaas uu dhammaado, compiler-ka ayaa si automatic ah u gelnaya free methods si looga fogaado memory leaks. Tani waxay meesha ka saartay gaabiska uu keeno garbage collector-ku.

### S. Ma ku ordi kartaa embedded devices ama aaladaha yaryar (IoT)?
**J.** Haa. Maadaama koodhka Tusmo loo beddelo C caadi ah oo la isku-dubi karo (fully standalone C), wuxuu ordi karaa meel kasta oo uu ka shaqayn karo GCC compiler. Tan waxaa ku jira aaladaha yaryar sida Raspberry Pi ama aaladaha kale ee loogu talagalay embedded systems.

### S. Sidee u shaqeeyaa badbaadada koodhka (Memory Safety) ee ku jira runtime-ka?
**J.** runtime-ka Tusmo wuxuu leeyahay dhowr nidaam badbaado:
- **Bounds Checking**: Haddii aad isku daydo inaad wax ka akhriso tix (array) meel ka baxsan cabbirkeeda, runtime-ku wuxuu barnaamijka u istaajinayaa si nabad ah isagoo daabacaya runtime error Af-Soomaali ah oo aad u cad.
- **Null Safety**: Dhammaan dynamic pointers-ka waxaa lagu wacaa macros badbaado leh si looga fogaado Segmentation Faults.

Aad iyo aad ayaad ugu mahadsantahay isticmaalkaaga iyo horumarintaada Tusmo! Aynu wada dhisno luuqad casri ah oo waarta oo ku hadasha Afkeenna Hooyo.
