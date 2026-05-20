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
import pathlib
from compiler.frontend.lexer.lexer import lexer
from compiler.frontend.parser.parser import parser
from compiler.midend.docstring_utils import preprocess_docstrings

def find_and_read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def parse_code_to_ast(code, filename):
    code = preprocess_docstrings(code)
    lexer.filename = filename
    lexer.lineno = 1
    ast = parser.parse(code, lexer=lexer)
    return ast if ast is not None else []

def _resolve_module_path(module_name, base_directory, stdlib_path):
    if module_name.endswith(".tus"):
        file_to_import = module_name
    else:
        file_to_import = module_name + ".tus"

    paths = [
        os.path.abspath(os.path.join(base_directory, file_to_import)),
        os.path.abspath(os.path.join(".lib", file_to_import)),
        os.path.abspath(os.path.join("lib", file_to_import)),
        os.path.abspath(os.path.join(stdlib_path, file_to_import))
    ]
    for p in paths:
        if os.path.exists(p): return p
    return None

def _get_top_level_name(node):
    if isinstance(node, KeydNode): return node.var_name
    if isinstance(node, FunctionNode): return node.name
    if isinstance(node, ClassNode): return node.name
    if isinstance(node, QaabNode): return node.name
    if isinstance(node, QeexNode): return node.name
    return None

def _find_c_calls_in_node(node):
    c_ids = set()
    node_str = str(node)
    matches = re.findall(r'___c__call_\s*\(\s*["\']([^"\']+)["\']', node_str)
    c_ids.update(matches)
    if isinstance(node, FunctionNode):
        for stmt in node.body:
            matches = re.findall(r'___c__call_\s*\(\s*["\']([^"\']+)["\']', str(stmt))
            c_ids.update(matches)
    return c_ids

def _select_requested_nodes(resolved_imported_ast, requested_names, seen_metadata, is_partial=False):
    selected_nodes = []
    found_names = set()
    requested_name_set = set(requested_names)

    # 1. Select named nodes
    for imported_node in resolved_imported_ast:
        if isinstance(imported_node, (EmbeddedCNode, Xidid)): continue
        name = _get_top_level_name(imported_node)
        if name and name in requested_name_set:
            selected_nodes.append(imported_node)
            found_names.add(name)

    # 2. Identify C-call dependencies
    needed_c_identifiers = set()
    if is_partial:
        for node in selected_nodes:
            needed_c_identifiers.update(_find_c_calls_in_node(node))

    # 3. Select metadata
    for imported_node in resolved_imported_ast:
        if not isinstance(imported_node, (EmbeddedCNode, Xidid)): continue
        content = getattr(imported_node, 'code', None) or getattr(imported_node, 'aqoonsi', None)
        if content in seen_metadata: continue
        
        if not is_partial:
            selected_nodes.append(imported_node)
            seen_metadata.add(content)
        else:
            if isinstance(imported_node, Xidid) or "#include" in (content or ""):
                selected_nodes.append(imported_node)
                seen_metadata.add(content)
            elif isinstance(imported_node, EmbeddedCNode):
                if any(re.search(rf"\b{re.escape(c_id)}\b", content) for c_id in needed_c_identifiers):
                    selected_nodes.append(imported_node)
                    seen_metadata.add(content)

    return selected_nodes, list(found_names)

def _find_missing_partial_import_dependencies(resolved_imported_ast, selected_nodes, requested_names, already_available_names):
    module_top_level_names = {name for name in (_get_top_level_name(n) for n in resolved_imported_ast) if name}
    available_set = set(already_available_names) | set(requested_names)
    missing_reasons = {}

    def add_reason(dep, reason):
        missing_reasons.setdefault(dep, set()).add(reason)

    for node in selected_nodes:
        if isinstance(node, FunctionNode):
            ret = getattr(node, "return_type", None)
            if isinstance(ret, str) and ret in module_top_level_names and ret not in available_set:
                add_reason(ret, f"nooca soo-celinta ee '{node.name}'")
            for p in getattr(node, "params", []):
                ptype = getattr(p, "param_type", None)
                if isinstance(ptype, str) and ptype in module_top_level_names and ptype not in available_set:
                    add_reason(ptype, f"nooca halbeegga '{p.name}' ee '{node.name}'")
        elif isinstance(node, KeydNode):
            vtype = getattr(node, "var_type", None)
            if isinstance(vtype, str) and vtype in module_top_level_names and vtype not in available_set:
                add_reason(vtype, f"nooca doorsoomaha '{node.var_name}'")

    for n in selected_nodes:
        if isinstance(n, EmbeddedCNode):
            code = getattr(n, "code", "")
            for name in module_top_level_names:
                if name in available_set: continue
                if re.search(rf"\b{re.escape(name)}\b", code):
                    match = re.findall(rf"(\w+)\s*\([^)]*\b{re.escape(name)}\b[^)]*\)\s*\{{", code)
                    ctx = f"C-wrapper '{match[0]}'" if match else "koodhka C"
                    add_reason(name, f"waxaa looga baahanyahay {ctx}")

    return [(dep, sorted(reasons)) for dep, reasons in sorted(missing_reasons.items())]

def _append_unique_nodes(target_ast, nodes_to_add, seen_top_level_names):
    for node in nodes_to_add:
        name = _get_top_level_name(node)
        if name:
            if name in seen_top_level_names: continue
            seen_top_level_names.add(name)
        target_ast.append(node)

def process_imports(initial_ast_nodes, base_directory, stdlib_path="stdlib", processed_files=None, active_files=None, seen_metadata=None, seen_top_level_names=None):
    if processed_files is None: processed_files = set()
    if active_files is None: active_files = set()
    if seen_metadata is None: seen_metadata = set()
    if seen_top_level_names is None: seen_top_level_names = set()

    final_ast = []
    pending_dependency_checks = []

    for node in initial_ast_nodes:
        if isinstance(node, (KeenNode, IsticmaalNode)):
            module_name = (node.filename if isinstance(node, KeenNode) else node.module).strip('"\'')
            found_path = _resolve_module_path(module_name, base_directory, stdlib_path)
            
            if not found_path or found_path in active_files:
                if not found_path:
                    print(f"\n\033[1;31m[!] KHALAD:\033[0m Lama helin '{module_name}'!")
                    sys.exit(1)
                continue

            # Skip if already fully imported via 'keen'
            if isinstance(node, KeenNode) and found_path in processed_files: continue

            try:
                active_files.add(found_path)
                imported_ast = parse_code_to_ast(find_and_read_file(found_path), found_path)
                
                # We need a LOCAL 'seen' set for the recursive call to get all nodes,
                # but we'll merge them into the global set afterwards.
                local_seen_names = set()
                resolved_imported_ast = process_imports(
                    imported_ast, os.path.dirname(found_path), stdlib_path,
                    processed_files, active_files, seen_metadata, local_seen_names
                )

                if isinstance(node, KeenNode):
                    processed_files.add(found_path)
                    # Merge names into the global context
                    for name in local_seen_names: seen_top_level_names.add(name)
                    final_ast.extend(resolved_imported_ast)
                else:
                    selected, found_list = _select_requested_nodes(
                        resolved_imported_ast, node.names or [], seen_metadata, is_partial=True
                    )
                    
                    found_set = set(found_list)
                    missing = [n for n in node.names if n not in found_set and n not in seen_top_level_names]
                    if missing:
                        print(f"\n\033[1;31m[!] KHALAD:\033[0m '{module_name}' kuma jiraan: {', '.join(missing)}!")
                        sys.exit(1)
                        
                    missing_deps = _find_missing_partial_import_dependencies(
                        resolved_imported_ast, selected, node.names, seen_top_level_names
                    )
                    if missing_deps:
                        pending_dependency_checks.append({
                            "module_name": module_name, "filename": node.filename,
                            "line": node.line, "missing_deps": missing_deps
                        })
                    _append_unique_nodes(final_ast, selected, seen_top_level_names)

            except Exception as e:
                print(f"Fashil: {found_path}:\n{e}")
                sys.exit(1)
            finally:
                active_files.discard(found_path)
        else:
            _append_unique_nodes(final_ast, [node], seen_top_level_names)

    for check in pending_dependency_checks:
        unresolved = [(d, r) for d, r in check["missing_deps"] if d not in seen_top_level_names]
        if unresolved:
            print(f"\n\033[1;31m[!] KHALAD:\033[0m '{check['module_name']}' waxaa ka dhiman: {', '.join([n for n, _ in unresolved])}!")
            sys.exit(1)

    return final_ast
