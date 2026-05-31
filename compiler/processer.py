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
        os.path.abspath(file_to_import),
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

def _find_c_calls_in_node(node, visited=None):
    if visited is None:
        visited = set()
    if id(node) in visited:
        return set()
    visited.add(id(node))

    c_ids = set()
    if isinstance(node, (list, tuple)):
        for item in node:
            c_ids.update(_find_c_calls_in_node(item, visited))
        return c_ids
    elif isinstance(node, dict):
        for val in node.values():
            c_ids.update(_find_c_calls_in_node(val, visited))
        return c_ids

    cls_name = node.__class__.__name__
    if cls_name == "CCallNode":
        if hasattr(node, "c_function_name") and isinstance(node.c_function_name, str):
            c_ids.add(node.c_function_name.strip("\"'"))

    for attr in dir(node):
        if attr.startswith("__") or attr in ("line", "filename", "lineno"):
            continue
        try:
            val = getattr(node, attr, None)
        except Exception:
            continue
        if val is None:
            continue
        if isinstance(val, (list, tuple)):
            for v in val:
                if v is not None and not isinstance(v, (str, int, float, bool)):
                    c_ids.update(_find_c_calls_in_node(v, visited))
        elif not isinstance(val, (str, int, float, bool)):
            c_ids.update(_find_c_calls_in_node(val, visited))
    return c_ids

def _find_function_calls(node, visited=None):
    if visited is None:
        visited = set()
    if id(node) in visited:
        return set()
    visited.add(id(node))

    calls = set()
    if isinstance(node, (list, tuple)):
        for item in node:
            calls.update(_find_function_calls(item, visited))
        return calls
    elif isinstance(node, dict):
        for val in node.values():
            calls.update(_find_function_calls(val, visited))
        return calls

    cls_name = node.__class__.__name__
    if cls_name == "FunctionCallNode":
        if hasattr(node, "name"):
            calls.add(node.name)
    elif cls_name == "IdentifierNode":
        if hasattr(node, "name"):
            calls.add(node.name)

    for attr in dir(node):
        if attr.startswith("__") or attr in ("line", "filename", "lineno"):
            continue
        try:
            val = getattr(node, attr, None)
        except Exception:
            continue
        if val is None:
            continue
        if isinstance(val, (list, tuple)):
            for v in val:
                if v is not None and not isinstance(v, (str, int, float, bool)):
                    calls.update(_find_function_calls(v, visited))
        elif not isinstance(val, (str, int, float, bool)):
            calls.update(_find_function_calls(val, visited))
    return calls

def _select_requested_nodes(resolved_imported_ast, requested_names, seen_metadata, is_partial=False):
    selected_nodes = []
    found_names = set()
    requested_name_set = set(requested_names)

    # Map from top-level name in the module to its AST node(s)
    name_to_nodes = {}
    for imported_node in resolved_imported_ast:
        if isinstance(imported_node, (EmbeddedCNode, Xidid)): continue
        name = _get_top_level_name(imported_node)
        if name:
            name_to_nodes.setdefault(name, []).append(imported_node)

    # Transitive closure of dependencies
    queue = list(requested_name_set)
    processed = set()

    while queue:
        name = queue.pop(0)
        if name in processed: continue
        processed.add(name)

        if name in name_to_nodes:
            for node in name_to_nodes[name]:
                if node not in selected_nodes:
                    selected_nodes.append(node)
                    found_names.add(name)
                    # Scan for internal references
                    refs = _find_function_calls(node)
                    for ref in refs:
                        if ref in name_to_nodes and ref not in processed:
                            queue.append(ref)

    # 2. Identify C-call dependencies
    needed_c_identifiers = set()
    if is_partial:
        for node in selected_nodes:
            needed_c_identifiers.update(_find_c_calls_in_node(node))

    # 3. Select metadata
    for imported_node in resolved_imported_ast:
        if not isinstance(imported_node, (EmbeddedCNode, Xidid)): continue
        content = getattr(imported_node, 'code', None) or getattr(imported_node, 'aqoonsi', None)

        # For partial imports, keep module-level C support code and linker
        # metadata together with the selected symbols.
        if isinstance(imported_node, EmbeddedCNode):
            if is_partial:
                has_needed_c = False
                for c_id in needed_c_identifiers:
                    if re.search(rf"\b{re.escape(c_id)}\b", content or ""):
                        has_needed_c = True
                        break
                if not has_needed_c: continue
        else:
            # Xidid (library linking) should still use global seen_metadata to prevent duplicates.
            if content in seen_metadata: continue
            seen_metadata.add(content)

        selected_nodes.append(imported_node)

    return selected_nodes, list(found_names)

def _find_missing_partial_import_dependencies(resolved_imported_ast, selected_nodes, requested_names, already_available_names):
    module_top_level_names = {name for name in (_get_top_level_name(n) for n in resolved_imported_ast) if name}
    available_set = set(already_available_names) | {name for name in (_get_top_level_name(n) for n in selected_nodes) if name}
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

        # Deep FFI / nested code dependency analysis
        referenced_names = _find_function_calls(node)
        for ref_name in referenced_names:
            if ref_name in module_top_level_names and ref_name not in available_set:
                node_name = getattr(node, "name", None) or getattr(node, "var_name", None) or "koodhka"
                add_reason(ref_name, f"waxaa looga baahanyahay gudaha '{node_name}'")

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

def validate_embedded_c_includes(ast_nodes, project_root, runtime_dir=None, stdlib_path=None):
    include_pattern = re.compile(r'#include\s+"([^"]+)"')

    def iter_nodes(nodes):
        for node in nodes:
            if isinstance(node, list):
                yield from iter_nodes(node)
            else:
                yield node

    def resolve_include(include_path, source_dir):
        candidates = [
            os.path.abspath(os.path.join(source_dir, include_path)),
            os.path.abspath(os.path.join(project_root, include_path)),
            os.path.abspath(include_path),
        ]
        if runtime_dir:
            candidates.append(os.path.abspath(os.path.join(runtime_dir, include_path)))
        if stdlib_path:
            candidates.append(os.path.abspath(os.path.join(stdlib_path, include_path)))
        return any(os.path.exists(path) for path in candidates)

    for node in iter_nodes(ast_nodes):
        if not isinstance(node, EmbeddedCNode):
            continue

        code = getattr(node, "code", "") or ""
        source_dir = os.path.dirname(os.path.abspath(getattr(node, "filename", "") or project_root))
        for include_path in include_pattern.findall(code):
            if resolve_include(include_path, source_dir):
                continue

            print(
                f"\n\033[1;31m[!] KHALAD:\033[0m "
                f"Embedded C include '{include_path}' lagama helin '{getattr(node, 'filename', '<unknown>')}'."
            )
            sys.exit(1)

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
                # initialized as a copy of parent seen names to prevent nested redefinition.
                local_seen_names = set(seen_top_level_names)
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
