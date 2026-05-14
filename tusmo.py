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
from tusmo_cli import (
    handle_download_command,
    handle_list_catalog_command,
    handle_remove_command,
    handle_update_lib_command,
    handle_baahiyaha_command,
)

sys.path.append(os.path.dirname(__file__))
from pathlib import Path

from compiler.frontend.lexer.lexer import lexer
from compiler.frontend.parser.parser import parser
from compiler.backend.transpiler import Transpiler
from compiler.midend.symbol_table import SymbolTable
from compiler.midend.semanticanalyzer import SemanticChecker, SemanticError
from compiler.frontend.parser.ast_nodes import Xidid
from compiler.processer import process_imports
from compiler.midend.fstring_resolver import resolve_fstrings
from compiler.midend.docstring_utils import (
    preprocess_docstrings,
    attach_docstrings,
)


LOCAL_VERSION = "0.0.6"
REPO_URL = "https://api.github.com/repos/TusmoLang-org/Tusmo/releases/latest"



def _platform_key(os_type: str) -> str:
    if os_type == "Windows":
        return "windows"
    if os_type == "Darwin":
        return "macos"
    return "linux"



def help(command=None):
    if command in ["-h", "--help", "-c", "--caawimaad"]:
        msg = r"""
  _______ _    _  _____ __  __  ____  
 |__   __| |  | |/ ____|  \/  |/ __ \ 
    | |  | |  | | (___ | \  / | |  | |
    | |  | |  | |\___ \| |\/| | |  | |
    | |  | |__| |____) | |  | | |__| |
    |_|   \____/|_____/|_|  |_|\____/ 

tusmo <fayl.tus> [doorashooyin] | tusmo <fayl.tus> | tusmo [doorashooyin]

Doorashooyinka (Options):
-c, --caawimaad / -h, --help:         waxay soo bandhigtaa macluumaadka doorashooyin-ka(options) (tusaale: tusmo -h ama tusmo -c).

-n, --nooc / -v, --version:           waxay soo bandhigtaa macluumaadka nooca/version aad heysato (tusaale: tusmo -v ama tusmo -n).

-m, --maktabadaha / -l, --libraries:  waxay tirinaysaa dhamaan maktabadaha (libararies) la heli karo (tusaale: tusmo -l ama tusmo -m).

--c:                                  Waxay keydinaysaa fayl-ka `C` ee la sameeyay, halkii laga tiri lahaa (tusaale: tusmo <*.tus> --c).

download / dagso / soo_degso / soo_dajiso:   waxay soo dejinaysaa maktabadda(libararies) aad rabto (tusaale: tusmo download <libarary_name> ama tusmo dagso <magaca_maktabada>)
tir-maktabad / uninstall / remove / tir:     waxay tirtiraysaa maktabad la rakibay (tusaale: tusmo tir-maktabad <magaca_maktabada>)
cusbooneysii-maktabad / cusboonaysii-lib / update-lib:  waxay cusboonaysiisaa maktabad la rakibay (tusaale: tusmo cusbooneysii-maktabad <magaca_maktabada>)
maktabado:                                    waxay ku tusaysaa dhammaan maktabadaha index-ka adigoo isticmaalaya arrow selection.
baahiyaha:                                    waxay akhrinaysaa baahiyaha.json kadibna si toos ah ayey u rakibaysaa dhammaan maktabadaha ku qoran.
--no-color:                                   waxay damisaa midabada output-ka.
--non-interactive / -y:                       waxay ka dhigaysaa hab aan su'aalo lahayn (CI-friendly).
update / cusboonaysii / casriye:    waxay isku dayaysaa inay is casriyeyso iyadoo soo dejinaysa nooca ugu dambeeya ee Tusmo (tusaale: tusmo update ama tusmo cusboonaysii).
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
        print("- opengl: Waxay la xiriirtaa sawirid (graphics), daaqad, iyo game-loop.")
        sys.exit(0)
   

def get_static_lib():
    flags = []
    for lib in Xidid.dhamaan_xogta:
        file_name = lib
        os_type = platform.system()
        os_name = _platform_key(os_type)

        # Waa inaad variable-ka dib u qeexdaa (re-assign)
        if os_name == "windows":
            if file_name.endswith(".maya"):
                file_name = file_name.removesuffix(".maya")
            elif not file_name.endswith(".lib"):
                file_name += ".lib"

        else:  # linux or macos
            if file_name.endswith(".maya"):
                file_name = file_name.removesuffix(".maya")
            elif not file_name.endswith(".a"):
                file_name += ".a"
            

        
        # Hubi in faylku dhab ahaan u jiro ka hor intaanan ku darin flags
        if os.path.exists(file_name):
            flags.append(f'"{file_name}"')
        else:
            # Haddii uusan jirin waddada tooska ah, isku day inaad ka raadiso .lib/
            alt_path = os.path.join(".lib", file_name)
            if os.path.exists(alt_path):
                flags.append(f'"{alt_path}"')
            else:
                # Haddii wali la waayo, iska daa saas (GCC ayaa error soo saari doona)
                flags.append(f'"{file_name}"')
                
    return " ".join(flags)

def main():
    remove_c_code = True

    if len(sys.argv) < 2:
        print("Isticmaalka: tusmo <magaca_faylka.tus> ")
        sys.exit(1)
 
    help(sys.argv[1])
    version(sys.argv[1])
    list_libraries(sys.argv[1])
    if handle_list_catalog_command(sys.argv):
        sys.exit(0)
    if handle_download_command(sys.argv):
        sys.exit(0)
    if handle_baahiyaha_command(sys.argv):
        sys.exit(0)
    if handle_remove_command(sys.argv):
        sys.exit(0)
    if handle_update_lib_command(sys.argv):
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
        "math": os.path.join(runtime_dir, "math.c"),
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
        all_imported_files = {os.path.abspath(filename)}
        final_ast = process_imports(initial_ast, base_directory=main_file_directory, stdlib_path=stdlib_dir, processed_files=all_imported_files)

        if not final_ast:
            sys.exit(0)
            
        used_features = set()
        resolve_fstrings(final_ast)
        attach_docstrings(final_ast)
        checker = SemanticChecker(shared_symbol_table)
        checker.check(final_ast)
        # Pass the 'checker' instance and detected features to the Transpiler
        transpiler = Transpiler(shared_symbol_table, checker)
        # Merge detected features with transpiler features
        transpiler.used_features.update(used_features)

        c_code, final_used_features = transpiler.transpile(final_ast)
        used_features.update(final_used_features)
                
        out_file = filename.replace(".tus", ".c")
        with open(out_file, "w") as f:
            f.write(c_code)

        binary = out_file.replace(".c", "")

        # Dynamically build the list of source files to compile
        source_files_to_compile = [out_file]

        for feature in used_features:
            if feature in feature_to_source_map:
                source_path = feature_to_source_map[feature]
                if isinstance(source_path, list):
                    for path in source_path:
                        if os.path.exists(path):
                            source_files_to_compile.append(path)
                else:
                    if os.path.exists(source_path):
                        source_files_to_compile.append(source_path)

        all_sources_str = " ".join([f'"{path}"' for path in source_files_to_compile])

        # Compiler and Flags
        cc = os.environ.get("TUSMO_CC", "gcc")
        lib_dir_override = os.environ.get("TUSMO_LIB_DIR")
        include_override = os.environ.get("TUSMO_INCLUDE_DIR")

        include_flag = f'-I"{include_override}"' if include_override else f'-I"{runtime_dir}"'
        lib_flag = f' -L"{lib_dir_override}"' if lib_dir_override else ""
        math_flag = " -lm" if "math" in used_features else ""

        

        compile_command = (
            f'"{cc}" -O3 -march=native -flto -o "{binary}" '
            f'{all_sources_str} '
            f'{include_flag} '
            # Halkan hoose ayaa isbeddelka lagu sameeyay:
            f'{get_static_lib()} ' 
            f'{lib_flag}  {math_flag}'
        )
        print(f"This is compiler command {compile_command}")
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
