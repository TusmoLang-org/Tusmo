# semanticanalyzer.py (Final Fix for All Type Conflicts)

from compiler.frontend.parser.ast_nodes import (
    KeydNode, AssignmentNode, IdentifierNode, FunctionNode, FunctionCallNode,
    IfNode, QorNode, HelNode, ReturnStatementNode, BinaryOpNode, NumberNode,
    StringNode, FloatNode, CharNode, BooleanNode, FStringNode, TernaryOpNode, ASTNode,
    ArrayTypeNode, ArrayInitializationNode, ArrayAccessNode, ArrayAssignmentNode, ArrayTypeQueryNode,
    WhileNode, DoWhileNode, ForRangeNode, ForEachNode, MethodCallNode,
    ClassNode, ClassInstantiationNode, MemberAccessNode, ThisNode, CCallNode, WaalidNode,
    DictionaryInitializationNode, DictionaryAccessNode, DictionaryAssignmentNode,
    FunctionTypeNode, ParameterNode, BreakNode, ContinueNode, NamedArgument, TypeLiteralNode, WaxboNode,
    QeexNode, QaabNode, QaabQiimeNode
)
from compiler.midend.symbol_table import SymbolTable
from compiler.midend.built_in_fn import functions_
from compiler.midend.semantic_errors import *
from compiler.midend.lifetime_tracker import LifetimeTracker

class SemanticChecker:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.tracker = LifetimeTracker(symbol_table)
        self.current_function = None
        self.current_class = None
        self.loop_depth = 0
        self.active_cleanup_stack = []
        self.is_lhs = False

    def _is_valid_type(self, type_node):
        primitive_types = {"tiro", "jajab", "eray", "xaraf", "miyaa", "waxbo", "qaamuus"}

        if isinstance(type_node, ArrayTypeNode):
            if type_node.element_type is None:
                return True
            return self._is_valid_type(type_node.element_type)

        if isinstance(type_node, FunctionTypeNode):
            if not self._is_valid_type(type_node.return_type):
                return False
            return all(self._is_valid_type(p) for p in type_node.param_types)

        t = str(type_node).strip()
        if t in primitive_types:
            return True

        info = self.symbol_table.get(t)
        if not info:
            return False

        # Accept user-defined class/struct and explicitly-declared C types.
        return info[1] in ("class_definition", "struct_definition", "c_type")

    def _ensure_valid_type(self, type_node, node_for_error):
        if not self._is_valid_type(type_node):
            raise SemanticError(
                ERR_UNKNOWN_TYPE(str(type_node)),
                getattr(node_for_error, "filename", "unknown"),
                getattr(node_for_error, "line", "unknown"),
            )

    def _are_types_compatible(self, declared_type, value_type):
        if declared_type is None: return True
        dt = str(declared_type).strip()
        vt = str(value_type).strip()
        if dt == vt: return True
        if dt in ('dynamic_value', 'unknown', 'c_dynamic') or vt in ('dynamic_value', 'unknown', 'c_dynamic'):
            return True
        if vt in ('waxbo', 'nooc:waxbo'):
            if any(dt.startswith(t) for t in ['tix:', 'eray', 'qaamuus']): return True
            if dt and dt[0].isupper(): return True # Class/Struct types
            info = self.symbol_table.get(dt)
            if info and info[1] == 'struct_definition': return True
        if dt.startswith('tix:') and vt == 'tix': return True
        return False

    def check(self, node):
        if node is None: return
        if isinstance(node, list) and not self.active_cleanup_stack:
             # DO NOT push/pop a global scope for symbol_table because c_code_generator needs it later
             self.tracker.push_scope()
             for item in node: self.check(item)
             
             # Save global cleanup vars so the code generator can emit them at the end of main
             self.global_cleanup = self.tracker.pop_scope()
             return
        if isinstance(node, list):
            for item in node: self.check(item)
            return
        method_name = f"check_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_check)
        res = method(node)
        # print(f"DEBUG: check({type(node).__name__}) -> {res}")
        return res

    def generic_check(self, node):
        for attr_name in dir(node):
            if not attr_name.startswith("__"):
                value = getattr(node, attr_name)
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, ASTNode): self.check(item)
                elif isinstance(value, ASTNode): self.check(value)

    def get_expression_type(self, node: ASTNode, skip_context_check=False):
        if isinstance(node, NumberNode): return "tiro"
        if isinstance(node, FloatNode): return "jajab"
        if isinstance(node, StringNode): return "eray"
        if isinstance(node, CharNode): return "xaraf"
        if isinstance(node, BooleanNode): return "miyaa"
        if isinstance(node, WaxboNode): return "waxbo"
        if isinstance(node, FStringNode): return "eray"
        if isinstance(node, DictionaryInitializationNode): return "qaamuus"
        if isinstance(node, QaabQiimeNode): return node.struct_name
        if isinstance(node, CCallNode): return "dynamic_value"
        if isinstance(node, FunctionCallNode):
            if node.name == 'dherer': return "tiro"
            if node.name == 'nooc': return "eray"
            if node.name in functions_:
                return functions_[node.name]["return_type"]
            info = self.symbol_table.get(node.name)
            if info:
                if isinstance(info[1], FunctionTypeNode): return info[1].return_type
                if info[1] == "hawl": return info[0].return_type
            return "dynamic_value"
            
        if isinstance(node, ClassInstantiationNode): return node.class_name
        if isinstance(node, ThisNode):
            return self.current_class.name if self.current_class else "unknown"
        if isinstance(node, WaalidNode):
            return self.current_class.parent_name if self.current_class and self.current_class.parent_name else "unknown"
        if isinstance(node, MemberAccessNode):
            obj_type = self.get_expression_type(node.object_node)
            if str(obj_type) in ("dynamic_value", "qaamuus", "unknown"): return "dynamic_value"
            
            # Resolve inheritance depth
            class_info = self.symbol_table.get(str(obj_type))
            if class_info:
                if class_info[1] == 'class_definition':
                    current_class = class_info[0]
                    while current_class:
                        for m in current_class.members:
                            if m.var_name == node.member_name:
                                return str(m.var_type)
                        if getattr(current_class, 'parent_name', None):
                            parent_info = self.symbol_table.get(current_class.parent_name)
                            current_class = parent_info[0] if parent_info else None
                        else:
                            break
                elif class_info[1] == 'struct_definition':
                    current_struct = class_info[0]
                    for m in current_struct.members:
                        if m.var_name == node.member_name:
                            return str(m.var_type)
            return "unknown"
            
        if isinstance(node, MethodCallNode):
            obj_type = self.get_expression_type(node.object_node)
            if str(obj_type) in ("dynamic_value", "qaamuus", "eray", "unknown") or str(obj_type).startswith("tix"): 
                return "dynamic_value" # We assume string/array methods return dynamic or specific values handled at runtime
                
            class_info = self.symbol_table.get(str(obj_type))
            if class_info and class_info[1] == 'class_definition':
                current_class = class_info[0]
                while current_class:
                    for method in current_class.methods:
                        if method.name == node.method_name:
                            return str(method.return_type)
                    if getattr(current_class, 'parent_name', None):
                        parent_info = self.symbol_table.get(current_class.parent_name)
                        current_class = parent_info[0] if parent_info else None
                    else:
                        break
            return "dynamic_value"
            
        if isinstance(node, IdentifierNode):
            info = self.symbol_table.get(node.name)
            if info:
                # info[1] is the type (string or ASTNode)
                return str(info[1]).strip()
            return "unknown"
        
        if isinstance(node, BinaryOpNode):
            # Resolve type for binary operations
            left_type = self.get_expression_type(node.left)
            right_type = self.get_expression_type(node.right)
            
            if node.op == '+':
                if str(left_type) == 'eray' or str(right_type) == 'eray':
                    return "eray"
            
            if node.op in ('+', '-', '*', '/', '%'):
                if 'jajab' in (str(left_type), str(right_type)):
                    return "jajab"
                return "tiro"
            
            if node.op in ('==', '!=', '>', '<', '>=', '<=', 'iyo', 'ama'):
                return "miyaa"

        return "unknown"

    def check_KeydNode(self, node: KeydNode):
        self._ensure_valid_type(node.var_type, node)
        # Store the string representation of the type in SymbolTable
        self.symbol_table.set(node.var_name, str(node.var_type).strip())
        self.tracker.record_definition(node.var_name, node.var_type, node, is_initialized=(node.value is not None))
        
        if node.value:
            value_type = self.check(node.value)
            
            # Super intelligent: Record Move!
            if isinstance(node.value, IdentifierNode) and self.tracker.is_heap_type(node.var_type):
                self.tracker.record_move(node.value.name, node)
                
            if not self._are_types_compatible(node.var_type, value_type):
                raise SemanticError(
                    ERR_TYPE_MISMATCH(str(node.var_type), str(value_type)),
                    node.filename,
                    node.line
                )
        
        self.generic_check(node)

    def check_AssignmentNode(self, node: AssignmentNode):
        needs_cleanup = False
        target_type = self.get_expression_type(node.identifier)
        if isinstance(node.identifier, IdentifierNode) and self.tracker.is_heap_type(target_type):
            if not self.tracker.is_moved(node.identifier.name):
                needs_cleanup = True
                
        if isinstance(node.identifier, IdentifierNode):
            self.tracker.revive(node.identifier.name)
            self.tracker.mark_initialized(node.identifier.name)
            
        node.needs_cleanup = needs_cleanup
        value_type = self.check(node.expression)
        
        # Super intelligent: Record Move!
        if isinstance(node.expression, IdentifierNode) and self.tracker.is_heap_type(target_type):
            self.tracker.record_move(node.expression.name, node)
            
        if not self._are_types_compatible(target_type, value_type):
            raise SemanticError(
                ERR_ASSIGNMENT_TYPE_MISMATCH_SIMPLE(str(target_type), str(value_type)),
                node.filename,
                node.line
            )
        
        self.generic_check(node)

    def check_FunctionNode(self, node: FunctionNode):
        self._ensure_valid_type(node.return_type, node)
        for p in node.params:
            self._ensure_valid_type(p.param_type, p)
        self.symbol_table.set(node.name, "hawl", value=node)
        
        old_function = self.current_function
        self.current_function = node
        
        self.symbol_table.push_scope()
        self.tracker.push_scope()
        for p in node.params:
            self.symbol_table.set(p.name, str(p.param_type).strip())
            self.tracker.record_definition(p.name, p.param_type, p, is_initialized=True)
        self.check(node.body)
        node.cleanup_vars = self.tracker.pop_scope()
        self.symbol_table.pop_scope()
        
        self.current_function = old_function

    def check_IfNode(self, node: IfNode):
        node.cases_cleanup = []
        for cond, body in node.cases:
            self.check(cond)
            self.tracker.push_scope()
            self.check(body)
            node.cases_cleanup.append(self.tracker.pop_scope())
        if node.else_case:
            self.tracker.push_scope()
            self.check(node.else_case)
            node.else_cleanup = self.tracker.pop_scope()

    def check_WhileNode(self, node: WhileNode):
        self.check(node.condition)
        self.tracker.push_scope()
        self.check(node.body)
        node.cleanup_vars = self.tracker.pop_scope()

    def check_ArrayInitializationNode(self, node: ArrayInitializationNode):
        for elem in node.elements:
            self.check(elem)
        return "tix"

    def check_ForRangeNode(self, node: ForRangeNode):
        self.check(node.start_expr)
        self.check(node.end_expr)
        self.symbol_table.push_scope()
        self.tracker.push_scope()
        self.symbol_table.set(node.iterator_var_name, "tiro")
        self.tracker.record_definition(node.iterator_var_name, "tiro", node, is_initialized=True)
        self.check(node.body)
        node.cleanup_vars = self.tracker.pop_scope()
        self.symbol_table.pop_scope()

    def check_ForEachNode(self, node: ForEachNode):
        arr_type = self.check(node.array_expr)
        elem_type = "unknown"
        if isinstance(arr_type, ArrayTypeNode):
            elem_type = arr_type.element_type if arr_type.element_type else "dynamic_value"
        elif str(arr_type) == "eray":
            elem_type = "xaraf"
        self.symbol_table.push_scope()
        self.tracker.push_scope()
        self.symbol_table.set(node.iterator_var_name, str(elem_type))
        self.tracker.record_definition(node.iterator_var_name, elem_type, node, is_initialized=True)
        self.check(node.body)
        node.cleanup_vars = self.tracker.pop_scope()
        self.symbol_table.pop_scope()

    def check_NumberNode(self, node: NumberNode): return "tiro"
    def check_NumberNode(self, node: NumberNode): return "tiro"
    def check_FloatNode(self, node: FloatNode): return "jajab"
    def check_StringNode(self, node: StringNode): return "eray"
    def check_CharNode(self, node: CharNode): return "xaraf"
    def check_BooleanNode(self, node: BooleanNode): return "miyaa"
    def check_WaxboNode(self, node: WaxboNode): return "waxbo"
    def check_ArrayAccessNode(self, node: ArrayAccessNode):
        self.check(node.array_name_node)
        self.check(node.index_expression)
        return self.get_expression_type(node)

    def check_QaabQiimeNode(self, node: QaabQiimeNode):
        for val in node.values:
            self.check(val)
        return node.struct_name
    def check_IdentifierNode(self, node: IdentifierNode):
        if not self.symbol_table.get(node.name):
            raise SemanticError(ERR_IDENTIFIER_NOT_FOUND(node.name), node.filename, node.line)
        if self.tracker.is_moved(node.name):
            raise SemanticError(ERR_USE_AFTER_MOVE(node.name, "Moved"), node.filename, node.line)
        if not self.tracker.is_initialized(node.name):
            raise SemanticError(ERR_UNINITIALIZED_VARIABLE(node.name), node.filename, node.line)
        return self.get_expression_type(node)

    def check_FStringNode(self, node: FStringNode):
        for part_type, part_value in node.parts:
            if part_type == "expr":
                if isinstance(part_value, ASTNode):
                    self.check(part_value)
        return "eray"

    def check_TernaryOpNode(self, node: TernaryOpNode):
        self.check(node.condition)
        t_type = self.check(node.if_true)
        f_type = self.check(node.if_false)
        return t_type

    def check_ReturnStatementNode(self, node: ReturnStatementNode):
        if not self.current_function:
            raise SemanticError(ERR_RETURN_OUTSIDE_FUNCTION(), node.filename, node.line)
            
        value_type = self.check(node.expression) if node.expression else "waxbo"
        
        if not self._are_types_compatible(self.current_function.return_type, value_type):
            raise SemanticError(
                ERR_RETURN_TYPE_MISMATCH(str(self.current_function.return_type), str(value_type)),
                node.filename,
                node.line
            )
        
        # Super intelligent memory management: track all variables that need to be freed on return
        node.active_cleanup = self.tracker.get_all_active_heap_vars()
        
        return value_type

    def check_BreakNode(self, node: BreakNode):
        node.active_cleanup = self.tracker.get_active_heap_vars_for_loop()
        
    def check_ContinueNode(self, node: ContinueNode):
        node.active_cleanup = self.tracker.get_active_heap_vars_for_loop()


    def check_FunctionCallNode(self, node: FunctionCallNode):
        if node.name in functions_:
            for arg in node.params:
                self.check(arg)
            return functions_[node.name]["return_type"]

        info = self.symbol_table.get(node.name)
        if not info:
             raise SemanticError(ERR_FUNCTION_NOT_FOUND(node.name), node.filename, node.line)
        
        if isinstance(info[1], FunctionTypeNode):
             return info[1].return_type
             
        if info[1] == "hawl":
            func_node = info[0]
            if len(node.params) != len(func_node.params):
                required_params = [p for p in func_node.params if p.default_value is None]
                if len(node.params) < len(required_params) or len(node.params) > len(func_node.params):
                    raise SemanticError(
                        ERR_ARG_COUNT_MISMATCH(node.name, len(func_node.params), len(node.params)),
                        node.filename,
                        node.line
                    )
            
            for i, arg in enumerate(node.params):
                if i < len(func_node.params):
                    arg_type = self.check(arg)
                    expected_type = func_node.params[i].param_type
                    if not self._are_types_compatible(expected_type, arg_type):
                        raise SemanticError(
                            ERR_ARG_TYPE_MISMATCH_SIMPLE(i+1, node.name, str(expected_type), str(arg_type)),
                            node.filename,
                            node.line
                        )
            
            return func_node.return_type
            
        return "unknown"

    def check_QeexNode(self, node: QeexNode):
        if isinstance(node.value, IdentifierNode) and node.name == node.value.name:
            self.symbol_table.set(node.name, "c_type", value=node.value)
            return

        try:
            val_type = self.get_expression_type(node.value)
        except:
            val_type = 'c_dynamic'
        
        self.symbol_table.set(node.name, val_type, value=node.value)

    def check_QaabNode(self, node: QaabNode):
        for member in node.members:
            self._ensure_valid_type(member.var_type, member)
        self.symbol_table.set(node.name, 'struct_definition', value=node)

    def check_BinaryOpNode(self, node: BinaryOpNode):
        left_type = self.check(node.left)
        right_type = self.check(node.right)
        
        if node.op == '+':
            if str(left_type) == 'eray' or str(right_type) == 'eray':
                return "eray"
        
        if node.op in ('+', '-', '*', '/', '%'):
            if str(left_type) not in ('tiro', 'jajab') or str(right_type) not in ('tiro', 'jajab'):
                 raise SemanticError(
                    ERR_BINARY_OP_TYPE_MISMATCH(str(left_type), str(right_type), node.op),
                    node.filename,
                    node.line
                )
            return "jajab" if 'jajab' in (str(left_type), str(right_type)) else "tiro"
        
        if node.op in ('==', '!=', '>', '<', '>=', '<='):
            return "miyaa"
            
        if node.op in ('iyo', 'ama'):
            if str(left_type) != 'miyaa' or str(right_type) != 'miyaa':
                 raise SemanticError(
                    ERR_BINARY_OP_TYPE_MISMATCH(str(left_type), str(right_type), node.op),
                    node.filename,
                    node.line
                )
            return "miyaa"

        return "unknown"

    def check_ClassNode(self, node: ClassNode):
        self.symbol_table.set(node.name, 'class_definition', value=node)
        
        old_class = self.current_class
        self.current_class = node
        
        self.symbol_table.push_scope()
        self.tracker.push_scope()
        for m in node.methods: self.check(m)
        node.cleanup_vars = self.tracker.pop_scope()
        self.symbol_table.pop_scope()
        
        self.current_class = old_class

    def check_ClassInstantiationNode(self, node: ClassInstantiationNode):
        info = self.symbol_table.get(node.class_name)
        if not info or info[1] != 'class_definition':
            raise SemanticError(f"Kooxda '{node.class_name}' ma jirto", node.filename, node.line)
            
        class_node = info[0]
        constructor = None
        for method in class_node.methods:
            if method.name == 'dhis':
                constructor = method
                break
                
        if constructor:
            required_params = [p for p in constructor.params if p.default_value is None]
            if len(node.constructor_args) < len(required_params) or len(node.constructor_args) > len(constructor.params):
                raise SemanticError(
                    f"Dhismaha '{node.class_name}' wuxuu u baahan yahay {len(required_params)} ilaa {len(constructor.params)} qaybood, laakiin {len(node.constructor_args)} ayaa la siiyay",
                    node.filename, node.line
                )
            
            for i, arg in enumerate(node.constructor_args):
                if i < len(constructor.params):
                    arg_type = self.check(arg)
                    expected_type = constructor.params[i].param_type
                    if not self._are_types_compatible(expected_type, arg_type):
                        raise SemanticError(
                            f"Qaybta {i+1} ee dhismaha '{node.class_name}' waa inay ahaataa '{expected_type}', laakiin waa '{arg_type}'",
                            node.filename, node.line
                        )
        elif node.constructor_args:
            raise SemanticError(f"Kooxda '{node.class_name}' ma laha dhise(constructor) qaata qaybo", node.filename, node.line)
            
        return node.class_name

    def check_MemberAccessNode(self, node: MemberAccessNode):
        self.check(node.object_node)
        return self.get_expression_type(node)
        
    def check_MethodCallNode(self, node: MethodCallNode):
        self.check(node.object_node)
        for arg in node.args_list:
            self.check(arg)
            # Super intelligent: Record Move for 'gali'!
            if node.method_name == 'gali':
                val_node = arg.value if isinstance(arg, NamedArgument) else arg
                if isinstance(val_node, IdentifierNode):
                    arg_type = self.get_expression_type(val_node)
                    if self.tracker.is_heap_type(arg_type):
                        self.tracker.record_move(val_node.name, node)
        return self.get_expression_type(node)
        
    def check_ThisNode(self, node: ThisNode):
        return self.get_expression_type(node)
        
    def check_WaalidNode(self, node: WaalidNode):
        return self.get_expression_type(node)
