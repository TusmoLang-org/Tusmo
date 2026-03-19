# tusmo.py (Correctly Updated)

import sys
import os
import traceback
import subprocess

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

LOCAL_VERSION = "1.0.26"
REPO_URL = "https://api.github.com/repos/tusmo-official/Tusmo/releases/latest"

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
    import requests
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
                cmd = "sudo rm -rf ~/.tusmo /usr/local/bin/tusmo 2>/dev/null && curl -fsSL https://raw.githubusercontent.com/tusmo-official/Tusmo/main/install.sh | bash"
                subprocess.run(cmd, shell=True, check=True)
            
            elif os_type == "Windows":
                print("Tusmo waxay isku dayaysaa inay is casriyeyso (Windows)...")
                cmd = "irm https://raw.githubusercontent.com/tusmo-official/Tusmo/main/install.ps1 | iex"
                subprocess.run(["powershell", "-Command", cmd], check=True)
            
            print("\nTusmo waa la cusboonaysiiyay!")
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Khalad ayaa dhacay: {e}")
        
        sys.exit(0)

def download_libraries(all_args):
    import shutil
    import requests
    import zipfile
    import io
    import time

    # Hubi in doodu tahay 3 (tusmo download library_name)
    if len(all_args) == 3:
        command = all_args[1].lower()
        if command in ["download", "dagso", "soo_degso", "soo_dajiso", "soo_daji"]:
            library_name = all_args[2]
            
            # 🔗 Link-ga rasmiga ah ee Tusmo Organization
            base_url = f"https://github.com{library_name}"
            target_path = f"./tusmo_modules/{library_name}"

            print(f"\n[Tusmo] Waxaa la bilaabay soo dajinta: {library_name}...")
            print(f"Source: {base_url}")
            time.sleep(0.5)

            # --- 1. ISKU DAY GIT CLONE ---
            if shutil.which("git"):
                print(f"[Git] Waxaa la helay git, waxaa la bilaabayaa 'cloning' repo-ka...")
                try:
                    # 'capture_output=True' waxay naga caawinaysaa inaan log-ga nadiifino
                    subprocess.run(["git", "clone", base_url, target_path], check=True, capture_output=True)
                    print(f"✅ Guul! {library_name} hadda waa diyaar (via Git).")
                    return
                except subprocess.CalledProcessError:
                    print(f"⚠️  [Git] Git wuu ku fashilmay (maga laga yaabaa in repo-gu jirin).")

            # --- 2. ISKU DAY MANUAL DOWNLOAD (HADDII GIT UU MAQAN YAHAY) ---
            print(f"📡 [System] Waxaa la isku dayayaa soo dejin toos ah (Manual Download)...")
            
            # GitHub ZIP link (inta badan waa 'main' ama 'master')
            zip_url = f"{base_url}/archive/refs/heads/main.zip"
            
            try:
                # Progress bar yar oo 'fake' ah si loo dareemo in wax dhacayaan
                for i in range(1, 6):
                    sys.stdout.write(f"\r🔥 [Cooking] Soo dejinta: [{'#' * i}{'.' * (5-i)}] {i*20}%")
                    sys.stdout.flush()
                    time.sleep(0.2)
                print("\n")

                r = requests.get(zip_url, stream=True)
                
                # Haddii 'main' la waayo, isku day 'master'
                if r.status_code != 200:
                    zip_url = f"{base_url}/archive/refs/heads/master.zip"
                    r = requests.get(zip_url, stream=True)

                r.raise_for_status()

                # Kala fur faylka
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    # GitHub ZIP wuxuu leeyahay folder dheeri ah (tusmo-lib-main)
                    # Waxaan u soo saaraynaa galka aan rabno
                    z.extractall(path="./tusmo_modules")
                
                print(f"✅ Guul! {library_name} hadda waa diyaar (Manual).")
            
            except Exception as e:
                print(f"❌ Cilad: Ma suurtagalin in la soo dejiyo '{library_name}'.")
                print(f"   Hubi in magaca maktabaddu sax yahay: {base_url}")

            sys.exit(0)

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
    download_libraries(sys.argv[1:])
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
        compile_command = (
            f'"{cc}" -O3 -march=native -flto -o "{binary}" '
            f'{all_sources_str} {include_flag}{lib_flag} -lgc'
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
