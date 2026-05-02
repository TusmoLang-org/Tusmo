import sys
import os
import re
from compiler.frontend.parser.ast_nodes import (
    KeenNode,
    IsticmaalNode,
    KeydNode,
    FunctionNode,
    ClassNode,
    QaabNode,
    QeexNode,
    EmbeddedCNode,
    Xidid
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
    if isinstance(node, QaabNode):
        return node.name
    if isinstance(node, QeexNode):
        return node.name
    return None

def _select_requested_nodes(resolved_imported_ast, requested_names, seen_metadata):
    selected_nodes = []
    found_names = set()
    requested_name_set = set(requested_names)

    for imported_node in resolved_imported_ast:
        is_metadata = isinstance(imported_node, (EmbeddedCNode, Xidid))
        
        if is_metadata:
            content = getattr(imported_node, 'code', None) or getattr(imported_node, 'aqoonsi', None)
            if content not in seen_metadata:
                selected_nodes.append(imported_node)
                seen_metadata.add(content)
            continue
            
        top_level_name = _get_top_level_name(imported_node)
        if top_level_name and top_level_name in requested_name_set:
            selected_nodes.append(imported_node)
            found_names.add(top_level_name)

    missing_names = [name for name in requested_names if name not in found_names]
    return selected_nodes, missing_names

def _find_missing_partial_import_dependencies(resolved_imported_ast, selected_nodes, requested_names, already_available_names):
    module_top_level_names = {
        name for name in (_get_top_level_name(n) for n in resolved_imported_ast) if name
    }
    requested_set = set(requested_names)
    available_set = set(already_available_names) | requested_set
    missing_reasons = {}

    def add_reason(dep, reason):
        reasons = missing_reasons.setdefault(dep, set())
        reasons.add(reason)

    # 1) Typed signature dependencies (function/keyd) must be explicitly imported.
    for node in selected_nodes:
        if isinstance(node, FunctionNode):
            ret = getattr(node, "return_type", None)
            if isinstance(ret, str) and ret in module_top_level_names and ret not in available_set:
                add_reason(ret, f"return type of '{node.name}'")
            for p in getattr(node, "params", []):
                ptype = getattr(p, "param_type", None)
                if isinstance(ptype, str) and ptype in module_top_level_names and ptype not in available_set:
                    add_reason(ptype, f"parameter '{p.name}' in '{node.name}'")
        elif isinstance(node, KeydNode):
            vtype = getattr(node, "var_type", None)
            if isinstance(vtype, str) and vtype in module_top_level_names and vtype not in available_set:
                add_reason(vtype, f"type of keyd '{node.var_name}'")

    # 2) Embedded C dependencies: if selected metadata references module symbols, require explicit import.
    metadata_text = []
    for n in selected_nodes:
        if isinstance(n, EmbeddedCNode):
            metadata_text.append(getattr(n, "code", "") or "")
        elif isinstance(n, Xidid):
            metadata_text.append(getattr(n, "aqoonsi", "") or "")
    merged_metadata = "\n".join(metadata_text)
    if merged_metadata:
        for name in module_top_level_names:
            if name in available_set:
                continue
            if re.search(rf"\b{re.escape(name)}\b", merged_metadata):
                add_reason(name, "embedded C wrapper code")

    result = []
    for dep in sorted(missing_reasons.keys()):
        result.append((dep, sorted(missing_reasons[dep])))
    return result

def _append_unique_nodes(target_ast, nodes_to_add, seen_top_level_names):
    for node in nodes_to_add:
        top_level_name = _get_top_level_name(node)
        if top_level_name:
            if top_level_name in seen_top_level_names:
                continue
            seen_top_level_names.add(top_level_name)
        target_ast.append(node)

def process_imports(initial_ast_nodes, base_directory, stdlib_path="stdlib", processed_files=None, active_files=None, seen_metadata=None, seen_top_level_names=None):
    """
    Wuxuu si is-daba-joog ah u raadiyaa dhammaan qodobbada 'keen', wuxuuna soo celiyaa
    hal AST oo la isku daray.
    """
    if processed_files is None:
        processed_files = set()
    if active_files is None:
        active_files = set()
    if seen_metadata is None:
        seen_metadata = set()
    if seen_top_level_names is None:
        seen_top_level_names = set()

    final_ast = []
    pending_dependency_checks = []

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
                    active_files,
                    seen_metadata
                )

                if isinstance(node, KeenNode):
                    processed_files.add(found_path)
                    # For full imports, the metadata deduplication is already handled inside the recursive call
                    _append_unique_nodes(final_ast, resolved_imported_ast, seen_top_level_names)
                else:
                    # isticmaal = partial import. We still need to deduplicate metadata from this specific branch.
                    requested_names = node.names or []
                    if not requested_names:
                        print(f"Cilad ayaa ku jirta '{node.filename}' sadarka {node.line}:")
                        print("Qoraalka 'isticmaal' waa in uu leeyahay ugu yaraan hal magac.")
                        sys.exit(1)

                    selected_nodes, missing_names = _select_requested_nodes(
                        resolved_imported_ast,
                        requested_names,
                        seen_metadata
                    )
                    missing_names = [name for name in missing_names if name not in seen_top_level_names]
                    if missing_names:
                        missing_str = ", ".join(missing_names)
                        print(f"\n\033[1;31m[!] KHALAD ISTICMAAL:\033[0m '{module_name}' kuma jiraan magacyadan: {missing_str}!")
                        print(f"\033[90m" + ("-" * 45) + "\033[0m")
                        print(f"\033[94mFaylka:\033[0m   {node.filename}")
                        print(f"\033[94mSaddarka:\033[0m {node.line}")
                        print(f"\033[1;35m// Ma waxaad rabtaa inaad isticmaasho wax aan dhisnayn? '{module_name}' dib u eeg!\033[0m\n")
                        sys.exit(1)
                    missing_deps = _find_missing_partial_import_dependencies(
                        resolved_imported_ast,
                        selected_nodes,
                        requested_names,
                        seen_top_level_names
                    )
                    if missing_deps:
                        pending_dependency_checks.append({
                            "module_name": module_name,
                            "filename": node.filename,
                            "line": node.line,
                            "missing_deps": missing_deps
                        })
                    _append_unique_nodes(final_ast, selected_nodes, seen_top_level_names)

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
            _append_unique_nodes(final_ast, [node], seen_top_level_names)

    # Validate partial-import dependencies after all imports in this file are processed.
    for check in pending_dependency_checks:
        unresolved = []
        for dep_name, dep_reasons in check["missing_deps"]:
            if dep_name not in seen_top_level_names:
                unresolved.append((dep_name, dep_reasons))
        if unresolved:
            missing_str = ", ".join([name for name, _ in unresolved])
            print(f"\n\033[1;31m[!] KHALAD ISTICMAAL:\033[0m '{check['module_name']}' waxaad ka maqnayd kuwan: {missing_str}!")
            print(f"\033[90m" + ("-" * 45) + "\033[0m")
            print(f"\033[94mFaylka:\033[0m   {check['filename']}")
            print(f"\033[94mSaddarka:\033[0m {check['line']}")
            for dep_name, dep_reasons in unresolved:
                why = "; ".join(dep_reasons)
                print(f"\033[94m- {dep_name}:\033[0m {why}")
            print(f"\033[1;35m// 'isticmaal' wuxuu qaataa kaliya waxa aad doorato. Ku dar magacyadan liiska 'isticmaal'.\033[0m\n")
            sys.exit(1)

    return final_ast
