# tusmo.py (Correctly Updated)

import sys
import os
import traceback
import subprocess
import json
import platform
import urllib.request
import urllib.error
import requests

sys.path.append(os.path.dirname(__file__))
from pathlib import Path

from compiler.frontend.lexer.lexer import lexer
from compiler.frontend.parser.parser import parser
from compiler.backend.transpiler import Transpiler
from compiler.midend.symbol_table import SymbolTable
from compiler.midend.semanticanalyzer import SemanticChecker, SemanticError
from compiler.processer import process_imports
from compiler.midend.fstring_resolver import resolve_fstrings
from compiler.midend.docstring_utils import (
    preprocess_docstrings,
    attach_docstrings,
)


LOCAL_VERSION = "0.0.52"
REPO_URL = "https://api.github.com/repos/TusmoLang-org/Tusmo/releases/latest"

def help(command=None):
    if command in ["-h", "--help", "-c", "--caawimaad"]:
        msg = r"""
  _______ _    _  _____ __  __  ____  
 |__   __| |  | |/ ____|  \/  |/ __ \ 
    | |  | |  | | (___ | \  / | |  | |
    | |  | |  | |\___ \| |\/| | |  | |
    | |  | |__| |____) | |  | | |__| |
    |_|   \____/|_____/|_|  |_|\____/ 

-c --caawimaad / -h, --help         Tusmo waxay bixisaa caawimaad iyo macluumaad ku saabsan isticmaalka iyo astaamaha Tusmo.

-n --nooc / -v, --version           Tusmo waxay soo bandhigtaa macluumaadka nooca hadda jira ee Tusmo.

-m --maktabadaha / -l, --libraries  Tusmo waxay liis garaynaysaa maktabadaha la taageerayo iyo astaamahooda.

--c                                 Tusmo waxay ilaalisaa faylka C ee la soo saaray kadib marka la isku daro, halkii laga tirt

download / dagso / soo_degso / soo_dajiso <magaca_maktabadda>  Tusmo waxay soo dejinaysaa maktabadda la cayimay iyadoo la adeegsanayo magaca maktabadda.
update / cusboonaysiin / casriye    Tusmo waxay isku dayaysaa inay is casriyeyso iyadoo soo dejinaysa nooca ugu dambeeya ee Tusmo.

"""
        print(msg)
        sys.exit(0)

def check_for_updates():
    try:
        # Si loo yareeyo in la xannibo
        headers = {'User-Agent': 'Tusmo-Update-Checker'}
        response = requests.get(REPO_URL, headers=headers, timeout=5)
        
        if response.status_code == 200:
            latest_release = response.json()
            remote_version = latest_release["tag_name"]

            if remote_version.lstrip('v') != LOCAL_VERSION.lstrip('v'):
                print("\n")
                print("-" * 15, "Casriyeen Cusub Ayaa Lahelay", "-" * 15)
                print(f"Nooc cusub ayaa la helay: {remote_version}")
                print(f"Nooca aad haysato: {LOCAL_VERSION}")
                print("run-dheh 'tusmo cusboonaysii' si aad u cusbooneysiiso.")
         
    except Exception:
        # si aamusan ha u fail-garoowdo in case hadii user-ka uu san internet haysan si uu ogaan karo version-kiisa bilaa erro bilaa internet
        pass

def version(command=None):
    if command in ["-v", "--version", "-n", "--nooca"]:
        print(f"Tusmo Version: {LOCAL_VERSION}-beta")
        
        check_for_updates()
        sys.exit(0)


def update_tusmo(command=None):
    import platform
    if command in ["update", "cusboonaysii", "casriyee"]:
        os_type = platform.system() # Linux, Windows, or Darwin
        print(f"Nidaamkaaga waa: {os_type}")
        
        try:
            # Linux and MacOS share very similar command structures
            if os_type == "Linux" or os_type == "Darwin":
                print("Tusmo waxay isku dayaysaa inay is casriyeyso (Unix)...")
                cmd = "curl -fsSL https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.sh | bash"
                subprocess.run(cmd, shell=True, check=True)
            
            elif os_type == "Windows":
                print("Tusmo waxay isku dayaysaa inay is casriyeyso (Windows)...")
                cmd = "irm https://raw.githubusercontent.com/TusmoLang-org/Tusmo/main/install.ps1 | iex"
                subprocess.run(["powershell", "-Command", cmd], check=True)
            
            print("\nTusmo waa la cusboonaysiiyay!")
            
        except subprocess.CalledProcessError as e:
            print(f"\nKhalad ayaa dhacay: {e}")
        
        sys.exit(0)

def download_libraries(all_args):
    import shutil
    import zipfile
    import tempfile
    import urllib.request
    import urllib.error
    import json

    if len(all_args) != 3:
        return False

    command = all_args[1].lower()
    if command not in ["install", "-i", "-d", "dagso", "soo_degso", "soo_dajiso", "soo_daji"]:
        return False

    raw_name = all_args[2]
    if "=" in raw_name:
        library_name, version = raw_name.split("=", 1)
        version = version.strip()
    else:
        library_name, version = raw_name, None

    # --- Akhri kataloogga rasmiga ah: TusmoLang-org/index ---
    def fetch_catalog(url):
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                status = getattr(resp, "status", None)
                if status not in (None, 200):
                    return None
                data = resp.read().decode("utf-8")
                return json.loads(data).get("packages", [])
        except Exception:
            return None

    catalog_candidates = [
        os.environ.get("TUSMO_CATALOG_URL"),
        "https://raw.githubusercontent.com/TusmoLang-org/index/main/TusmoLang-org/catalog.json",
        "https://raw.githubusercontent.com/TusmoLang-org/index/main/catalog.json",
    ]

    catalog = []
    for catalog_url in [c for c in catalog_candidates if c]:
        catalog = fetch_catalog(catalog_url)
        if catalog:
            break

    if not catalog:
        print(
            f"Ma awoodi in aan akhriyo kataloogga rasmiga ah (TusmoLang-org/index). Fadlan hubi internet-kaaga, ama dejiso TUSMO_CATALOG_URL oo tilmaamaysa catalog.json."
        )
        return True

    pkg = next((p for p in catalog if p.get("name") == library_name), None)
    if not pkg:
        print(f"Maktabadda '{library_name}' lagama helin central-ka. Fadlan hubi magaca maktabadda ama eeg katalogga TusmoLang-org/index.")
        return True

    repo_url = pkg.get("repo")
    available_versions = pkg.get("versions", [])
    if version:
        if version not in available_versions:
            print(f"Nooca '{version}' lagama helin '{library_name}'. Noocyada jira: {', '.join(available_versions)}")
            return True
        chosen_version = version
    else:
        chosen_version = pkg.get("latest") or (available_versions[0] if available_versions else None)
        if not chosen_version:
            print(f"'{library_name}' lagama helin version-kan.")
            return True

    repo = repo_url.rstrip("/").split("/")[-1]
    target_dir = os.path.abspath(os.path.join(os.getcwd(), ".lib", repo))
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    print(f"\n[Tusmo] Waxaa la soo dejinayaa '{repo}' ... "
          f"nooca {chosen_version} ka socda {repo_url}")

    # Download ZIP (tag if specified, else main) — avoids any auth prompts
    if chosen_version:
        zip_url = f"{repo_url}/archive/refs/tags/{chosen_version}.zip"
    else:
        zip_url = f"{repo_url}/archive/refs/heads/main.zip"

    try:
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
                # GitHub zips root as repo-<branch/tag>
                extracted_root = next(Path(tmpdir).glob(f"{repo}-*"))
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                shutil.move(str(extracted_root), target_dir)
            print("Waxaa laguu soo dajiyaya ZIP gudaha .lib/")
    except Exception as e:
        print(f"Waa lagu guuldareystay soo dejinta '{library_name}': {e}")
        print(f"   URL la isku dayay: {zip_url}")
        return True

    return True

def update_libraries(command=None):
    pass

def remove_libraries(command=None):
    pass

def list_libraries(command=None):
    if command in ["-l", "--libraries", "-m","--maktabadaha"]:
        print("Tusmo waxay taageertaa maktabadahan soo socda:")
        print("- nasiib: Maktabadan waa mid lagu talagalay in .")
        print("- wakhti: Waxay la xiriirtaa waqtiga iyo taariikhda.")
        print("- os: Waxay la xiriirtaa nidaamka computer-ka.")
        print("- http: Waxay la xiriira codsiyada HTTP iyo server-yada webka.")
        print("- Xiriiriye: Waxay la xiriirtaa isgaarsiinta shabakadda ee heerka socket-ka.")
        print("- webxiriiriye: Waxay la xiriirtaa isgaarsiinta web-ka ee heerka websocket-ka.")
        sys.exit(0)
   


def main():
    remove_c_code = True

    if len(sys.argv) < 2:
        print("Isticmaalka: tusmo <magaca_faylka.tus> ")
        sys.exit(1)
 
    help(sys.argv[1])
    version(sys.argv[1])
    list_libraries(sys.argv[1])
    if download_libraries(sys.argv[0:3]):
        sys.exit(0)
    update_tusmo(sys.argv[1])
    
    if len(sys.argv) == 3 and sys.argv[2] == "--c":
        remove_c_code = False

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"Cilad: Faylka '{filename}' ma jiro.")
        sys.exit(1)

    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = script_directory
    runtime_dir = os.path.join(project_root, "runtime")
    stdlib_dir = os.path.join(project_root, "stdlib")


# --- QAYBTA CUSUB: C-INTERFACE (STATIC LIBS & HEADERS) ---
    os_type = platform.system()
    
    # Extension-ka saxda ah ee library-ga C
    static_ext = ".a" if os_type != "Windows" else ".lib"
    
    # Folder-ka kaliya ee aan u aqoonsanray dunida C
    c_bridge_folder = os.path.join(os.getcwd(), ".include")
    
    c_static_libs = []
    c_include_flag = ""

    if os.path.exists(c_bridge_folder):
        # 1. Ku dar folder-ka liiska "Include Path" ee GCC
        c_include_flag = f' -I"{c_bridge_folder}"'
        
        # 2. Si recursive ah u raadi dhammaan .a ama .lib files
        for root, dirs, files in os.walk(c_bridge_folder):
            for file in files:
                if file.endswith(static_ext):
                    full_path = os.path.join(root, file)
                    c_static_libs.append(f'"{full_path}"')
    
    c_libs_str = " ".join(c_static_libs)


    # Map features to their source files
    feature_to_source_map = {
        "string": os.path.join(runtime_dir, "string.c"),
        "nasiib": os.path.join(runtime_dir, "random.c"),
        "io": os.path.join(runtime_dir, "io.c"),
        "wakhti": os.path.join(runtime_dir, "time.c"),
        "os": os.path.join(runtime_dir, "os.c"),
        "dictionary": os.path.join(runtime_dir, "dictionary.c"),
        "conversion": os.path.join(runtime_dir, "type_conversion.c"),
        "http": os.path.join(runtime_dir, "http.c"),
        "socket": os.path.join(runtime_dir, "socket.c"),
        "websocket": os.path.join(runtime_dir, "websocket.c"),
        "array": [
            os.path.join(runtime_dir, "array.c"),
            os.path.join(runtime_dir, "array_generic.c"),
        ],
    }

    with open(filename, "r") as f:
        main_code = f.read()

    shared_symbol_table = SymbolTable()

    try:
        initial_ast = parse_code_to_ast(main_code, filename)

        if not initial_ast:
            sys.exit(0)

        main_file_directory = os.path.dirname(os.path.abspath(filename))
        final_ast = process_imports(initial_ast, base_directory=main_file_directory, stdlib_path=stdlib_dir)

        if not final_ast:
            sys.exit(0)

        resolve_fstrings(final_ast)
        attach_docstrings(final_ast)

        checker = SemanticChecker(shared_symbol_table)
        checker.check(final_ast)

    
        # Pass the 'checker' instance to the Transpiler
        transpiler = Transpiler(shared_symbol_table, checker)
        c_code, used_features = transpiler.transpile(final_ast)                
        out_file = filename.replace(".tus", ".c")
        with open(out_file, "w") as f:
            f.write(c_code)

        binary = out_file.replace(".c", "")

        # Dynamically build the list of source files to compile
        source_files_to_compile = [out_file]
        
        


        for feature in used_features:
            if feature in feature_to_source_map:
                source_path = feature_to_source_map[feature]
                # Check if the path is a list (like for 'array') or a single string
                if isinstance(source_path, list):
                    for path in source_path:
                        if os.path.exists(path):
                            source_files_to_compile.append(path)
                else:  # It's a single string
                    if os.path.exists(source_path):
                        source_files_to_compile.append(source_path)

        # Implicit dependency: Array (mixed) might use Dictionary printing
        if "array" in used_features and "dictionary" not in used_features:
            dict_path = feature_to_source_map["dictionary"]
            if os.path.exists(dict_path):
                source_files_to_compile.append(dict_path)

        all_sources_str = " ".join([f'"{path}"' for path in source_files_to_compile])

        # Allow overriding compiler/lib/include via env vars (for bundled installs)
        cc = os.environ.get("TUSMO_CC", "gcc")
        lib_dir_override = os.environ.get("TUSMO_LIB_DIR")
        include_override = os.environ.get("TUSMO_INCLUDE_DIR")

        include_flag = f'-I"{include_override}"' if include_override else f'-I"{runtime_dir}"'
        lib_flag = f' -L"{lib_dir_override}"' if lib_dir_override else ""
        
        # The final, dynamic compile command
        # ---------------------------------------------------------

        # Amarka kama dambaysta ah ee Compiler-ka
        compile_command = (
            f'"{cc}" -O3 -march=native -flto -o "{binary}" '
            f'{all_sources_str} {c_libs_str} '      # .a files ka yimid .include
            f'{include_flag}{c_include_flag} '      # -I runtime iyo -I .include
            f'{lib_flag} -lgc'                      # Boehm GC
        )

        compile_result = os.system(compile_command)

        if compile_result == 1:
            print(
                f"\nCilad ayaa ka dhacday isku-darka C code-ka. Faylka C wuxuu ku yaal: {out_file}"
            )
           

        if remove_c_code:
            if os.path.exists(out_file):
                os.remove(out_file)
            

    except SemanticError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception:
        print("\nCilad Lama Filaan Ah Ayaa Dhacday:")
        traceback.print_exc()
        sys.exit(1)


def parse_code_to_ast(code, filename):
    code = preprocess_docstrings(code)
    lexer.filename = filename
    lexer.lineno = 1
    ast = parser.parse(code, lexer=lexer)
    return ast if ast is not None else []


if __name__ == "__main__":
    main()
