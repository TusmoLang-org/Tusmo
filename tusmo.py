# Tusmo.py waa faylka main driver-ka ah ee luuqada Tusmo.

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
from compiler.processer import process_imports, validate_embedded_c_includes
from compiler.midend.fstring_resolver import resolve_fstrings
from compiler.midend.docstring_utils import (
    preprocess_docstrings,
    attach_docstrings,
)


LOCAL_VERSION = "2.0.1"
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
    seen = set()
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
            

        
        # De-duplicate clean/normalized flags
        if file_name in seen:
            continue
        seen.add(file_name)

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
    stdlib_dir = os.path.join(project_root, "stdlib")
    


    # Map features to their source files (deprecated: all C implementations are now inlined inside stdlib files)
    feature_to_source_map = {}


    with open(filename, "r") as f:
        main_code = f.read()

    shared_symbol_table = SymbolTable()

    try:
        from compiler.frontend.parser.ast_nodes import Xidid
        Xidid.dhamaan_xogta = []
        initial_ast = parse_code_to_ast(main_code, filename)

        if not initial_ast:
            sys.exit(0)

        # Injekti 'core' standard library si toos ah (Automatic Linking)
        from compiler.frontend.parser.ast_nodes import KeenNode
        initial_ast.insert(0, KeenNode(0, f'"{os.path.join(stdlib_dir, "core.tus")}"', filename))
        
        main_file_directory = os.path.dirname(os.path.abspath(filename))
        all_imported_files = {os.path.abspath(filename)}
        final_ast = process_imports(initial_ast, base_directory=main_file_directory, stdlib_path=stdlib_dir, processed_files=all_imported_files)
        validate_embedded_c_includes(final_ast, project_root, runtime_dir=None, stdlib_path=stdlib_dir)

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
                
        out_file = os.path.splitext(filename)[0] + ".c"
        with open(out_file, "w") as f:
            f.write(c_code)

        binary = os.path.splitext(out_file)[0]
        if os.name == "nt" and not binary.lower().endswith(".exe"):
            binary += ".exe"

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

        if include_override:
            include_flag = f'-I"{include_override}" -I"{project_root}" -I"{stdlib_dir}"'
        else:
            include_flag = f'-I"{project_root}" -I"{stdlib_dir}"'
        lib_flag = f' -L"{lib_dir_override}"' if lib_dir_override else ""
        math_flag = " -lm" if "math" in used_features else ""

        strict_flags = " -Wall -Wextra -Werror -Wno-unused-parameter -Wno-unused-function -Wno-unused-variable"

        compile_command = (
            f'"{cc}" -O3 -march=native -flto{strict_flags} -o "{binary}" '
            f'{all_sources_str} '
            f'{include_flag} '
            # Halkan hoose ayaa isbeddelka lagu sameeyay:
            f'{get_static_lib()} '
            f'{lib_flag}  {math_flag}'
        )
        import subprocess
        import re
        result = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
        compile_result = result.returncode

        if compile_result != 0:
            print("\n\033[1;31m[!] CILAD DHACDAY KA HOR SOO SAARIDA FAYLKA BINARY-GA (C-Level Compilation Error):\033[0m")
            print("\033[90m--------------------------------------------------------\033[0m")
            
            raw_errors = result.stderr or result.stdout or ""
            translated_lines = []
            
            def clean_diagnostics(text):
                # Clean up function/variable name mangling and entry points
                text = re.sub(r'__tusmo_main__', r'main', text)
                text = re.sub(r'__tusmo_(\w+)__', r'\1', text)
                text = re.sub(r'__tusmo_lambda_(\d+)', r'hawl_aan_magac_lahayn_\1', text)
                text = re.sub(r'__tusmo_temp_\d+', r'doorsoome_kumeelgaar', text)
                
                # Clean up standard I/O helper wrappers
                text = re.sub(r'tusmo_qor_walbo\((.*?)\)', r'qor(\1)', text)
                text = re.sub(r'tusmo_qor_tiro\((.*?)\)', r'qor(\1)', text)
                text = re.sub(r'tusmo_qor_jajab\((.*?)\)', r'qor(\1)', text)
                text = re.sub(r'tusmo_qor_eray\((.*?)\)', r'qor(\1)', text)
                text = re.sub(r'tusmo_qor_xaraf\((.*?)\)', r'qor(\1)', text)
                text = re.sub(r'tusmo_qor_miyaa\((.*?)\)', r'qor(\1)', text)
                
                text = re.sub(r'tusmo_gali_tiro\((.*?)\)', r'gali(\1)', text)
                text = re.sub(r'tusmo_gali_jajab\((.*?)\)', r'gali(\1)', text)
                text = re.sub(r'tusmo_gali_eray\((.*?)\)', r'gali(\1)', text)
                
                # Clean up transpiler array and dictionary types
                text = text.replace("TusmoString", "eray")
                text = text.replace("TusmoValue", "walbo")
                text = text.replace("TusmoTixTiro", "tiro[]")
                text = text.replace("TusmoTixJajab", "jajab[]")
                text = text.replace("TusmoTixEray", "eray[]")
                text = text.replace("TusmoTixXaraf", "xaraf[]")
                text = text.replace("TusmoTixMiyaa", "miyaa[]")
                text = text.replace("TusmoTixWalbo", "walbo[]")
                text = text.replace("TusmoQaamuus", "qaamuus")
                return text

            for line in raw_errors.splitlines():
                # Map generated C file back to original TUSMO file name
                if out_file in line:
                    line = line.replace(out_file, filename)
                elif out_file.replace(".c", "") in line:
                    line = line.replace(out_file.replace(".c", ""), filename.replace(".tus", ""))
                
                # Apply custom Somali cleanups to GCC diagnostics
                line = clean_diagnostics(line)
                
                # Replace standard diagnostic markers with Somali
                if "error: " in line:
                    line = line.replace("error: ", "\033[1;31mCilad:\033[0m ")
                if "warning: " in line:
                    line = line.replace("warning: ", "\033[1;33mDigniin:\033[0m ")
                if "note: " in line:
                    line = line.replace("note: ", "\033[1;36mFiiro Gaar Ah:\033[0m ")
                if "In function " in line:
                    line = line.replace("In function ", "Gudaha hawsha ")
                
                # Common compiler errors translations
                if "undeclared" in line:
                    line += " \033[1;35m// Doorsoomahan laguma qeexin koodhkaaga!\033[0m"
                elif "too few arguments" in line:
                    line += " \033[1;35m// Parameter-ada aad u dhiibtay hawsha way ka yaryihiin intii loo baahnaa!\033[0m"
                elif "too many arguments" in line:
                    line += " \033[1;35m// Parameter-ada aad u dhiibtay hawsha way ka badanyihiin intii loo baahnaa!\033[0m"
                elif "conflicting types" in line:
                    line += " \033[1;35m// Noocyada xogta ee aad isticmaashay way iska hor-imaanayaan!\033[0m"
                elif "expected" in line and "before" in line:
                    line += " \033[1;35m// Waxaa meashan ka maqan calaamad ama sumad (Syntax mismatch)!\033[0m"
                
                translated_lines.append(line)
            
            print("\n".join(translated_lines))
            print("\033[90m--------------------------------------------------------\033[0m")
            print(f"\nCilad ayaa ka dhacday isku-darka C code-ka. Faylka C wuxuu ku yaal: {out_file}")

        if remove_c_code and compile_result == 0:
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
