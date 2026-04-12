import sys
import os
from compiler.frontend.parser.ast_nodes import (
    KeenNode,
    IsticmaalNode,
    KeydNode,
    FunctionNode,
    ClassNode,
)
from compiler.frontend.lexer.lexer import lexer
from compiler.frontend.parser.parser import parser
from compiler.midend.docstring_utils import preprocess_docstrings

def find_and_read_file(file_path):
    """Wuxuu si badbaado leh u furaa oo u akhriyaa fayl."""
    with open(file_path, "r") as f:
        return f.read()

def parse_code_to_ast(code, filename):
    """
    Wuxuu u beddelaa koodka qoran AST.
    Wuxuu u sheegayaa lexer-ka magaca faylka si ay u saxmaan fariimaha cilladaha.
    """
    code = preprocess_docstrings(code)
    lexer.filename = filename
    lexer.lineno = 1
    
    ast = parser.parse(code, lexer=lexer)
    if ast is None:
        return []
    return ast

def _resolve_module_path(module_name, base_directory, stdlib_path):
    if module_name.endswith(".tus"):
        file_to_import = module_name
    else:
        file_to_import = module_name + ".tus"

    potential_local_path = os.path.abspath(os.path.join(base_directory, file_to_import))
    if os.path.exists(potential_local_path):
        return potential_local_path

    potential_hidden_lib_path = os.path.abspath(os.path.join(".lib", file_to_import))
    if os.path.exists(potential_hidden_lib_path):
        return potential_hidden_lib_path

    potential_library_path = os.path.abspath(os.path.join("lib", file_to_import))
    if os.path.exists(potential_library_path):
        return potential_library_path

    potential_stdlib_path = os.path.abspath(os.path.join(stdlib_path, file_to_import))
    if os.path.exists(potential_stdlib_path):
        return potential_stdlib_path

    return None

def _get_top_level_name(node):
    if isinstance(node, KeydNode):
        return node.var_name
    if isinstance(node, FunctionNode):
        return node.name
    if isinstance(node, ClassNode):
        return node.name
    return None

def _select_requested_nodes(resolved_imported_ast, requested_names):
    selected_nodes = []
    found_names = set()
    requested_name_set = set(requested_names)

    for imported_node in resolved_imported_ast:
        top_level_name = _get_top_level_name(imported_node)
        if top_level_name and top_level_name in requested_name_set:
            selected_nodes.append(imported_node)
            found_names.add(top_level_name)

    missing_names = [name for name in requested_names if name not in found_names]
    return selected_nodes, missing_names

def process_imports(initial_ast_nodes, base_directory, stdlib_path="stdlib", processed_files=None, active_files=None):
    """
    Wuxuu si is-daba-joog ah u raadiyaa dhammaan qodobbada 'keen', wuxuuna soo celiyaa
    hal AST oo la isku daray.
    """
    if processed_files is None:
        processed_files = set()
    if active_files is None:
        active_files = set()

    final_ast = []

    for node in initial_ast_nodes:
        if isinstance(node, (KeenNode, IsticmaalNode)):
            if isinstance(node, KeenNode):
                module_name = node.filename.strip('"\'')
            else:
                module_name = node.module.strip('"\'')

            found_path = _resolve_module_path(module_name, base_directory, stdlib_path)

            if not found_path:
                error_filename = node.filename or getattr(lexer, 'filename', '<faylka isha>')
                print(f"\n\033[1;31m[!] KHALAD SOO-KEENID:\033[0m Lama helin module-ka '{module_name}'!")
                print(f"\033[90m" + ("-" * 45) + "\033[0m")
                print(f"\033[94mFaylka:\033[0m   {error_filename}")
                print(f"\033[94mSaddarka:\033[0m {node.line}")
                print(f"\033[1;35m// Halkee ka raadinnaa '{module_name}'? Ma galka deegaanka, 'lib', mise 'stdlib' ayuu ku jiraa?\033[0m\n")
                sys.exit(1)

            # keen = old behavior (dedupe full-module include)
            if isinstance(node, KeenNode) and found_path in processed_files:
                continue

            # Ka hortag import isku-wareeg ah inta recursion-ku socdo
            if found_path in active_files:
                continue

            try:
                active_files.add(found_path)
                imported_code = find_and_read_file(found_path)
                imported_ast = parse_code_to_ast(imported_code, found_path)
                
                new_base_dir = os.path.dirname(found_path)
                resolved_imported_ast = process_imports(
                    imported_ast,
                    new_base_dir,
                    stdlib_path,
                    processed_files,
                    active_files
                )

                if isinstance(node, KeenNode):
                    processed_files.add(found_path)
                    final_ast.extend(resolved_imported_ast)
                else:
                    requested_names = node.names or []
                    if not requested_names:
                        print(f"Cilad ayaa ku jirta '{node.filename}' sadarka {node.line}:")
                        print("Qoraalka 'isticmaal' waa in uu leeyahay ugu yaraan hal magac.")
                        sys.exit(1)

                    selected_nodes, missing_names = _select_requested_nodes(
                        resolved_imported_ast,
                        requested_names
                    )
                    if missing_names:
                        missing_str = ", ".join(missing_names)
                        print(f"\n\033[1;31m[!] KHALAD ISTICMAAL:\033[0m '{module_name}' kuma jiraan magacyadan: {missing_str}!")
                        print(f"\033[90m" + ("-" * 45) + "\033[0m")
                        print(f"\033[94mFaylka:\033[0m   {node.filename}")
                        print(f"\033[94mSaddarka:\033[0m {node.line}")
                        print(f"\033[1;35m// Ma waxaad rabtaa inaad isticmaasho wax aan dhisnayn? '{module_name}' dib u eeg!\033[0m\n")
                        sys.exit(1)
                    final_ast.extend(selected_nodes)

            except FileNotFoundError:
                print(f"Cilad Isku-dubaraha: Faylka '{found_path}' wuu lumay intii lagu kuda jiray.")
                sys.exit(1)
            except Exception as e:
                # Tani waxay qabanaysaa ciladaha naxwaha ee parser-ka.
                print(f"Way fashilantay in la soo shaqeysiiyo '{found_path}':\n{e}")
                sys.exit(1)
            finally:
                active_files.discard(found_path)
        else:
            final_ast.append(node)
            
    return final_ast
