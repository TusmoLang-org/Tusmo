import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from pathlib import Path

CLR_RESET = "\033[0m"
CLR_TITLE = "\033[1;36m"
CLR_INFO = "\033[0;37m"
CLR_OK = "\033[1;32m"
CLR_WARN = "\033[1;33m"
CLR_ERR = "\033[1;31m"
REGISTRY_PATH = os.path.join(".lib", "installed.json")
BAAHIYAHA_PATH = "baahiyaha.json"


DEFAULT_CATALOG_URLS = [
    "https://raw.githubusercontent.com/TusmoLang-org/index/main/catalog.json",
    "https://raw.githubusercontent.com/TusmoLang-org/index/main/TusmoLang-org/catalog.json",
]


@dataclass
class LibraryEntry:
    name: str
    owner: str
    repo_url: str
    description: str
    latest: str
    versions: list[str]
    version_urls: dict[str, str]


def _flags_from_argv(argv):
    no_color = ("--no-color" in argv) or (os.environ.get("NO_COLOR") == "1")
    non_interactive = ("--non-interactive" in argv) or ("-y" in argv) or (not sys.stdin.isatty())
    return no_color, non_interactive


def _strip_cli_flags(argv):
    skip = {"--no-color", "--non-interactive", "-y"}
    return [a for a in argv if a not in skip]


def _set_colors_enabled(enabled: bool):
    global CLR_RESET, CLR_TITLE, CLR_INFO, CLR_OK, CLR_WARN, CLR_ERR
    if enabled:
        CLR_RESET = "\033[0m"
        CLR_TITLE = "\033[1;36m"
        CLR_INFO = "\033[0;37m"
        CLR_OK = "\033[1;32m"
        CLR_WARN = "\033[1;33m"
        CLR_ERR = "\033[1;31m"
    else:
        CLR_RESET = ""
        CLR_TITLE = ""
        CLR_INFO = ""
        CLR_OK = ""
        CLR_WARN = ""
        CLR_ERR = ""


def _read_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {"installed": []}
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("installed"), list):
            return data
    except Exception:
        pass
    return {"installed": []}


def _write_registry(data):
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _upsert_registry_entry(name, owner, version, repo_url, description, install_dir):
    db = _read_registry()
    installed = db["installed"]
    new_item = {
        "name": name,
        "owner": owner,
        "version": version,
        "repo_url": repo_url,
        "description": description,
        "install_dir": os.path.abspath(install_dir),
    }
    replaced = False
    for i, item in enumerate(installed):
        if item.get("name", "").lower() == name.lower():
            installed[i] = new_item
            replaced = True
            break
    if not replaced:
        installed.append(new_item)
    _write_registry(db)


def _remove_registry_entry(name):
    db = _read_registry()
    before = len(db["installed"])
    db["installed"] = [x for x in db["installed"] if x.get("name", "").lower() != name.lower()]
    _write_registry(db)
    return len(db["installed"]) != before


def _read_catalog():
    env_url = os.environ.get("TUSMO_CATALOG_URL")
    candidates = [env_url] + DEFAULT_CATALOG_URLS if env_url else DEFAULT_CATALOG_URLS
    for url in candidates:
        try:
            with urllib.request.urlopen(url, timeout=12) as resp:
                status = getattr(resp, "status", 200)
                if status not in (200, None):
                    continue
                data = json.loads(resp.read().decode("utf-8"))
                return data
        except Exception:
            continue
    return None


def _normalize_catalog(catalog_obj):
    if isinstance(catalog_obj, list):
        raw_packages = catalog_obj
    elif isinstance(catalog_obj, dict):
        raw_packages = catalog_obj.get("packages", [])
    else:
        raw_packages = []
    out = []
    for pkg in raw_packages:
        if not isinstance(pkg, dict):
            continue

        # New schema support:
        # { "<lib-name>": { "mulkiilaha": "...", "faahfaahinta": "...", "versions": {"1.0.1": {"url":"..."}} } }
        if len(pkg) == 1 and isinstance(next(iter(pkg.values())), dict):
            lib_name = next(iter(pkg.keys()))
            meta = next(iter(pkg.values()))
            owner = str(meta.get("mulkiilaha", "")).strip()
            description = str(meta.get("faahfaahinta", "")).strip()
            versions_obj = meta.get("versions", {}) or {}
            version_urls = {}
            for ver, ver_meta in versions_obj.items():
                if isinstance(ver_meta, dict):
                    u = str(ver_meta.get("url", "")).strip()
                    if u:
                        version_urls[str(ver).strip()] = u
            versions = list(version_urls.keys())
            latest = _pick_latest_version(versions)
            repo_url = version_urls.get(latest, "") if latest else ""
            if lib_name:
                out.append(
                    LibraryEntry(
                        name=str(lib_name).strip(),
                        owner=owner,
                        repo_url=repo_url,
                        description=description,
                        latest=latest or "",
                        versions=versions,
                        version_urls=version_urls,
                    )
                )
            continue

        name = (
            pkg.get("name")
            or pkg.get("library_name")
            or pkg.get("MagacaMaktabadaWaa")
            or ""
        ).strip()
        owner = (
            pkg.get("owner")
            or pkg.get("author")
            or pkg.get("MagacaQoraagaMaktabadaWaa")
            or ""
        ).strip()
        repo_url = (
            pkg.get("repo")
            or pkg.get("url")
            or pkg.get("repository")
            or pkg.get("UrlkaMaktabadaWaa")
            or ""
        ).strip()
        description = (
            pkg.get("description")
            or pkg.get("FaahfaahintaMaktabadaWaa")
            or ""
        ).strip()
        versions = pkg.get("versions") or []
        if isinstance(versions, str):
            versions = [versions]
        if not versions and pkg.get("version"):
            versions = [str(pkg.get("version"))]
        if not versions and pkg.get("NoociiUdameeyayWaa"):
            versions = [str(pkg.get("NoociiUdameeyayWaa"))]
        latest = (pkg.get("latest") or (versions[0] if versions else "")).strip()
        if not latest and pkg.get("NoociiUdameeyayWaa"):
            latest = str(pkg.get("NoociiUdameeyayWaa")).strip()
        if not latest and versions:
            latest = versions[0]
        if name:
            version_urls = {}
            versions_obj = pkg.get("versions", {})
            if isinstance(versions_obj, dict):
                for ver, ver_meta in versions_obj.items():
                    if isinstance(ver_meta, dict):
                        u = str(ver_meta.get("url", "")).strip()
                        if u:
                            version_urls[str(ver).strip()] = u
            out.append(LibraryEntry(name, owner, repo_url, description, latest, versions, version_urls))
    return out


def _version_key(v: str):
    parts = [p for p in v.replace("-", ".").split(".") if p != ""]
    key = []
    for p in parts:
        if p.isdigit():
            key.append((0, int(p)))
        else:
            key.append((1, p))
    return key


def _pick_latest_version(versions: list[str]):
    if not versions:
        return ""
    return sorted(versions, key=_version_key, reverse=True)[0]


def _score(query, entry: LibraryEntry):
    q = query.lower().strip()
    name = entry.name.lower()
    owner_name = f"{entry.owner}/{entry.name}".lower() if entry.owner else name
    desc = entry.description.lower()
    base = max(
        SequenceMatcher(None, q, name).ratio(),
        SequenceMatcher(None, q, owner_name).ratio(),
        SequenceMatcher(None, q, desc).ratio() if desc else 0.0,
    )
    if q == name or q == owner_name:
        return 1.0
    if q in name:
        base = max(base, 0.85)
    return base


def _pick_with_arrows(options: list[str], title: str, non_interactive: bool = False):
    if not options:
        return None
    if non_interactive or not sys.stdin.isatty():
        return 0
    try:
        import curses
    except ImportError:
        return 0

    def _fit_line(text: str, max_w: int):
        clean = text.replace("\n", " ").replace("\r", " ")
        if max_w < 4:
            return clean[:max_w]
        if len(clean) <= max_w:
            return clean
        return clean[: max_w - 3] + "..."

    def _run(stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        idx = 0
        while True:
            stdscr.erase()
            h, w = stdscr.getmaxyx()
            content_w = max(10, w - 1)

            stdscr.addstr(0, 0, _fit_line(title, content_w))
            stdscr.addstr(1, 0, _fit_line("Isticmaal ↑/↓ Kadib Enter", content_w))

            start_row = 3
            max_rows = max(1, h - start_row - 1)
            start = 0
            if idx >= max_rows:
                start = idx - max_rows + 1
            visible = options[start : start + max_rows]

            for i, opt in enumerate(visible):
                real_i = start + i
                prefix = "> " if real_i == idx else "  "
                line = _fit_line(prefix + opt, content_w)
                if real_i == idx:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(start_row + i, 0, line)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(start_row + i, 0, line)

            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (curses.KEY_UP, ord("k")):
                idx = (idx - 1) % len(options)
            elif ch in (curses.KEY_DOWN, ord("j")):
                idx = (idx + 1) % len(options)
            elif ch in (10, 13, curses.KEY_ENTER):
                return idx
            elif ch in (ord("q"), 27):
                return None

    return curses.wrapper(_run)


def _confirm_yes_no(prompt: str, default_yes: bool = True, non_interactive: bool = False):
    if non_interactive:
        return default_yes
    suffix = "[Y/n]" if default_yes else "[y/N]"
    ans = input(f"{prompt} {suffix} ").strip().lower()
    if not ans:
        return default_yes
    return ans in ("y", "yes", "h", "haa")


def _download_repo_tag(repo_url: str, version: str, target_dir: str):
    repo_name = repo_url.rstrip("/").split("/")[-1]
    zip_url = f"{repo_url}/archive/refs/tags/{version}.zip"
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "lib.zip")
        with urllib.request.urlopen(zip_url, timeout=30) as resp:
            status = getattr(resp, "status", 200)
            if status not in (200, None):
                raise RuntimeError(f"HTTP {status}")
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(resp, f)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmpdir)
            extracted_root = next(Path(tmpdir).glob(f"{repo_name}-*"))
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            shutil.move(str(extracted_root), target_dir)


def _download_zip_url(zip_url: str, target_dir: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "lib.zip")
        with urllib.request.urlopen(zip_url, timeout=30) as resp:
            status = getattr(resp, "status", 200)
            if status not in (200, None):
                raise RuntimeError(f"HTTP {status}")
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(resp, f)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmpdir)
            roots = [p for p in Path(tmpdir).iterdir() if p.is_dir()]
            extracted_root = roots[0] if roots else Path(tmpdir)
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            shutil.move(str(extracted_root), target_dir)


def _read_baahiyaha():
    if not os.path.exists(BAAHIYAHA_PATH):
        return {"maktabado": []}
    try:
        with open(BAAHIYAHA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("maktabado"), list):
            return data
    except Exception:
        pass
    return {"maktabado": []}


def _write_baahiyaha(data):
    with open(BAAHIYAHA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _upsert_baahiye(name, owner, version, source_url):
    data = _read_baahiyaha()
    libs = data["maktabado"]
    new_item = {
        "magaca_maktabada": name,
        "mulkiilaha": owner,
        "nooca": version,
        "url": source_url,
    }
    replaced = False
    for i, item in enumerate(libs):
        if str(item.get("magaca_maktabada", "")).lower() == name.lower():
            libs[i] = new_item
            replaced = True
            break
    if not replaced:
        libs.append(new_item)
    _write_baahiyaha(data)


def handle_list_catalog_command(argv):
    no_color, non_interactive = _flags_from_argv(argv)
    _set_colors_enabled(not no_color)
    argv = _strip_cli_flags(argv)
    if len(argv) < 2:
        return False
    cmd = argv[1].lower()
    if cmd not in ["maktabado", "libraries", "libs"]:
        return False

    print(f"{CLR_TITLE}[Tusmo]{CLR_RESET} Waxaan raadineynaa catalog-ga maktabadaha...")
    catalog = _read_catalog()
    if not catalog:
        print(f"{CLR_ERR}Ma helin catalog-ga TusmoLang-org/index.{CLR_RESET}")
        print(f"{CLR_INFO}    Hubi internet ama TUSMO_CATALOG_URL.{CLR_RESET}")
        return True

    entries = _normalize_catalog(catalog)
    if not entries:
        print(f"{CLR_WARN}Catalog-ga waa madhan ama lama fahmin qaabkiisa.{CLR_RESET}")
        return True

    entries.sort(key=lambda e: e.name.lower())
    labels = [
        f"{e.name} ({e.latest}) - {e.description[:100]}" if e.description else f"{e.name} ({e.latest})"
        for e in entries
    ]
    pick = _pick_with_arrows(labels, "Maktabadaha la heli karo:", non_interactive=non_interactive)
    if pick is None:
        print("Waa laga noqday doorashada.")
        return True

    chosen = entries[pick]
    owner = f" by {chosen.owner}" if chosen.owner else ""
    print(f"\n{CLR_TITLE}Magac:{CLR_RESET} {chosen.name}{owner}")
    print(f"    {CLR_INFO}Nooca ugu dambeeya:{CLR_RESET} {chosen.latest or 'lama cayimin'}")
    print(f"    {CLR_INFO}URL:{CLR_RESET} {chosen.repo_url or 'lama cayimin'}")
    print(f"    {CLR_INFO}Faahfaahin:{CLR_RESET} {chosen.description or 'ma jiro'}")
    print(f"\n{CLR_OK}Si aad u rakibto:{CLR_RESET}")
    print(f"    tusmo dagso {chosen.name}")
    return True


def handle_download_command(argv):
    no_color, non_interactive = _flags_from_argv(argv)
    _set_colors_enabled(not no_color)
    argv = _strip_cli_flags(argv)
    if len(argv) < 3:
        return False
    cmd = argv[1].lower()
    if cmd not in ["install", "-i", "-d", "dagso", "soo_degso", "soo_dajiso", "soo_daji", "download"]:
        return False

    query = argv[2].strip()
    version = None
    if "=" in query:
        query, version = [x.strip() for x in query.split("=", 1)]

    print(f"{CLR_TITLE}[Tusmo]{CLR_RESET} Waxaan raadineynaa catalog-ga maktabadaha...")
    catalog = _read_catalog()
    if not catalog:
        print(f"{CLR_ERR}Ma helin catalog-ga TusmoLang-org/index.{CLR_RESET}")
        print(f"{CLR_INFO}    Hubi internet ama TUSMO_CATALOG_URL.{CLR_RESET}")
        return True

    print(f"{CLR_TITLE}[Tusmo]{CLR_RESET} Catalog waa la helay. Waxaan falanqeynaynaa maktabadaha...")
    entries = _normalize_catalog(catalog)
    qlow = query.lower()
    exact = [
        e for e in entries
        if e.name.lower() == qlow or f"{e.owner}/{e.name}".lower() == qlow
    ]
    if exact:
        chosen = exact[0]
    else:
        ranked = [(e, _score(query, e)) for e in entries]
        ranked = [x for x in ranked if x[1] >= 0.45]
        ranked.sort(key=lambda x: x[1], reverse=True)
        if not ranked:
            print(f"{CLR_WARN}Maktabad u eg '{query}' lagama helin index-ka.{CLR_RESET}")
            return True
        if len(ranked) == 1 and ranked[0][1] >= 0.95:
            candidate = ranked[0][0]
            label = f"{candidate.name} ({candidate.latest})"
            if candidate.description:
                label += f" - {candidate.description[:100]}"
            if not _confirm_yes_no(f"Ma waxaad ula jeedday: {label}?", default_yes=True, non_interactive=non_interactive):
                print("Waa laga noqday doorashada.")
                return True
            chosen = candidate
        else:
            labels = [
                f"{e.name} ({e.latest}) - {e.description[:100]}" if e.description else f"{e.name} ({e.latest})"
                for e, _ in ranked[:10]
            ]
            pick = _pick_with_arrows(labels, "Waxaan soo helay Maktabadahan, fadlan dooro mida aad rabtay:", non_interactive=non_interactive)
            if pick is None:
                print("Waa laga noqday doorashada.")
                return True
            chosen = ranked[pick][0]

    if not chosen.repo_url:
        print(
            f"{CLR_ERR}URL-ka maktabaddan lama helin:{CLR_RESET} '{chosen.name}'.\n"
            f"{CLR_INFO}    Fadlan, haddii aad tahay developer-ka maktabaddan,\n"
            f"    ku dar URL-ka maktabadda gudaha catalog.json.{CLR_RESET}"
        )
        return True

    chosen_version = version or chosen.latest
    if not chosen_version:
        print(f"{CLR_ERR}Nooc lama helin:{CLR_RESET} {chosen.name}")
        return True
    if chosen.versions and chosen_version not in chosen.versions:
        print(f"{CLR_ERR}Noocan '{chosen_version}' lagama helin {chosen.name}.{CLR_RESET}")
        print(f"{CLR_INFO}    Jira: {', '.join(chosen.versions)}{CLR_RESET}")
        return True

    safe_owner = chosen.owner or "unknown"
    target_dir = os.path.abspath(os.path.join(".lib", f"{safe_owner}__{chosen.name}__{chosen_version}"))
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
    source_url = chosen.version_urls.get(chosen_version) if chosen.version_urls else ""
    if not source_url:
        source_url = chosen.repo_url
    try:
        print(f"{CLR_TITLE}[Tusmo]{CLR_RESET} Maktabad la doortay: {chosen.name}")
        print(f"    {CLR_INFO}Nooca la rakibayo:{CLR_RESET} {chosen_version}")
        print(f"    {CLR_INFO}Waxaan soo dejinaynaa: {source_url}{CLR_RESET}")
        if source_url.endswith(".zip"):
            _download_zip_url(source_url, target_dir)
        elif "/archive/refs/tags/" in source_url:
            _download_zip_url(source_url, target_dir)
        else:
            _download_repo_tag(chosen.repo_url, chosen_version, target_dir)
        print(f"{CLR_OK}[Tusmo] Soo dejin waa dhammaatay.{CLR_RESET}")
        print(f"{CLR_OK}[Tusmo] Rakibid waa dhammaatay:{CLR_RESET} {target_dir}")
        _upsert_registry_entry(
            chosen.name, chosen.owner, chosen_version, chosen.repo_url, chosen.description, target_dir
        )
        print(f"{CLR_OK}[Tusmo] Registry waa la cusbooneysiiyay:{CLR_RESET} {REGISTRY_PATH}")
        _upsert_baahiye(chosen.name, chosen.owner, chosen_version, source_url)
        print(f"{CLR_OK}[Tusmo] Baahiyaha waa la cusbooneysiiyay:{CLR_RESET} {BAAHIYAHA_PATH}")
    except urllib.error.HTTPError as e:
        print(f"{CLR_ERR}Soo dejin waa fashilantay (HTTP {e.code}).{CLR_RESET}")
        print(f"{CLR_INFO}    Hubi tag-ga '{chosen_version}'.{CLR_RESET}")
    except Exception as e:
        print(f"{CLR_ERR}Soo dejin waa fashilantay:{CLR_RESET} {e}")
    return True


def handle_remove_command(argv):
    no_color, _ = _flags_from_argv(argv)
    _set_colors_enabled(not no_color)
    argv = _strip_cli_flags(argv)
    if len(argv) < 3:
        return False
    cmd = argv[1].lower()
    if cmd not in ["tir-maktabad", "remove", "tir", "delete", "uninstall"]:
        return False
    name = argv[2].strip()

    db = _read_registry()
    item = next((x for x in db["installed"] if x.get("name", "").lower() == name.lower()), None)
    if not item:
        print(f"{CLR_WARN}Maktabadan lama helin registry:{CLR_RESET} {name}")
        return True

    install_dir = item.get("install_dir", "")
    if install_dir and os.path.exists(install_dir):
        shutil.rmtree(install_dir)
        print(f"{CLR_OK}[Tusmo] Waa la tiray:{CLR_RESET} {install_dir}")
    _remove_registry_entry(name)
    print(f"{CLR_OK}[Tusmo] Registry waa la cusbooneysiiyay.{CLR_RESET}")
    return True


def handle_update_lib_command(argv):
    no_color, non_interactive = _flags_from_argv(argv)
    _set_colors_enabled(not no_color)
    argv = _strip_cli_flags(argv)
    if len(argv) < 3:
        return False
    cmd = argv[1].lower()
    if cmd not in ["cusbooneysii-maktabad", "cusboonaysii-lib", "update-lib", "upgrade-lib"]:
        return False
    name = argv[2].strip()
    version_override = argv[3].strip() if len(argv) >= 4 else None

    db = _read_registry()
    item = next((x for x in db["installed"] if x.get("name", "").lower() == name.lower()), None)
    if not item:
        print(f"{CLR_WARN}Maktabadan lama helin registry:{CLR_RESET} {name}")
        print(f"{CLR_INFO}    Marka hore rakib: tusmo dagso {name}{CLR_RESET}")
        return True

    print(f"{CLR_TITLE}[Tusmo]{CLR_RESET} Waxaan ka hubineynaa nooc cusub: {name}")
    catalog = _read_catalog()
    if not catalog:
        print(f"{CLR_ERR}Ma helin catalog-ga TusmoLang-org/index.{CLR_RESET}")
        return True
    entries = _normalize_catalog(catalog)
    chosen = next((e for e in entries if e.name.lower() == name.lower()), None)
    if not chosen:
        print(f"{CLR_WARN}Maktabadda '{name}' lagama helin catalog-ka.{CLR_RESET}")
        return True

    target_version = version_override or chosen.latest
    if not target_version:
        print(f"{CLR_ERR}Nooc lama helin:{CLR_RESET} {chosen.name}")
        return True
    current_version = item.get("version", "")
    if not version_override and current_version == target_version:
        print(f"{CLR_INFO}Maktabadda '{name}' horey ayey ugu jirtaa nooca ugu dambeeya ({current_version}).{CLR_RESET}")
        return True
    if chosen.versions and target_version not in chosen.versions:
        print(f"{CLR_ERR}Noocan '{target_version}' lagama helin {chosen.name}.{CLR_RESET}")
        return True
    if not chosen.repo_url:
        print(f"{CLR_ERR}URL-ka maktabaddan lama helin:{CLR_RESET} {chosen.name}")
        return True

    safe_owner = chosen.owner or "unknown"
    target_dir = os.path.abspath(os.path.join(".lib", f"{safe_owner}__{chosen.name}__{target_version}"))
    source_url = chosen.version_urls.get(target_version) if chosen.version_urls else ""
    if not source_url:
        source_url = chosen.repo_url
    print(f"{CLR_TITLE}[Tusmo]{CLR_RESET} Cusboonaysiin: {chosen.name} {current_version} -> {target_version}")
    try:
        if source_url.endswith(".zip") or "/archive/refs/tags/" in source_url:
            _download_zip_url(source_url, target_dir)
        else:
            _download_repo_tag(chosen.repo_url, target_version, target_dir)
        old_dir = item.get("install_dir", "")
        if old_dir and old_dir != target_dir and os.path.exists(old_dir):
            shutil.rmtree(old_dir)
        _upsert_registry_entry(
            chosen.name, chosen.owner, target_version, chosen.repo_url, chosen.description, target_dir
        )
        _upsert_baahiye(chosen.name, chosen.owner, target_version, source_url)
        print(f"{CLR_OK}[Tusmo] Cusboonaysiin waa dhammaatay.{CLR_RESET}")
    except Exception as e:
        print(f"{CLR_ERR}[Tusmo] Cusboonaysiin waa fashilantay:{CLR_RESET} {e}")
    return True


def handle_baahiyaha_command(argv):
    no_color, non_interactive = _flags_from_argv(argv)
    _set_colors_enabled(not no_color)
    argv = _strip_cli_flags(argv)
    if len(argv) < 2:
        return False
    cmd = argv[1].lower()
    if cmd != "baahiyaha":
        return False

    data = _read_baahiyaha()
    libs = data.get("maktabado", [])
    if not libs:
        print(f"{CLR_WARN}baahiyaha.json waa madhan ama ma jiro.{CLR_RESET}")
        return True

    print(f"{CLR_TITLE}[Tusmo]{CLR_RESET} Waxaan rakibeynaa dhammaan baahiyaha...")
    total = len(libs)
    for i, lib in enumerate(libs, start=1):
        name = str(lib.get("magaca_maktabada", "")).strip()
        version = str(lib.get("nooca", "")).strip()
        if not name:
            continue
        print(f"{CLR_INFO}    [{i}/{total}] Rakibid: {name}={version or 'latest'}{CLR_RESET}")
        dl_argv = ["tusmo", "dagso", f"{name}={version}" if version else name]
        if no_color:
            dl_argv.append("--no-color")
        if non_interactive:
            dl_argv.append("--non-interactive")
        handle_download_command(dl_argv)
    print(f"{CLR_OK}[Tusmo] Dhammaan baahiyaha waa la dhammeeyay.{CLR_RESET}")
    return True
