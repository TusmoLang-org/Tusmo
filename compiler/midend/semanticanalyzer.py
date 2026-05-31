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
    QeexNode, QaabNode, QaabQiimeNode, LambdaNode
)
from compiler.midend.symbol_table import SymbolTable
from compiler.midend.semantic_errors import *
from compiler.midend.lifetime_tracker import LifetimeTracker
from compiler.backend.transpiler.expression_errors import ERR_NOOC_TIX_QUERY

class SemanticChecker:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.tracker = LifetimeTracker(symbol_table)
        self.current_function = None
        self.current_class = None
        self.loop_depth = 0
        self.active_cleanup_stack = []
        self.is_lhs = False

    def _is_borrowed_param_type(self, param_type):
        """
        Parameters that are passed by reference-like semantics should not be
        freed by the callee. Strings are intentionally excluded because they are
        duplicated at the call site when needed.
        """
        if isinstance(param_type, ArrayTypeNode):
            return True

        type_str = str(param_type).strip()
        if type_str.startswith("tix"):
            return True
        if type_str == "qaamuus":
            return True
        if type_str and type_str[0].isupper():
            return True
        return False

    def is_borrowed_param_type(self, param_type):
        return self._is_borrowed_param_type(param_type)

    def _is_valid_type(self, type_node):
        primitive_types = {"tiro", "jajab", "eray", "xaraf", "miyaa", "waxbo", "qaamuus", "walbo"}

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
        if dt in ('walbo', 'unknown', 'c_dynamic') or vt in ('walbo', 'unknown', 'c_dynamic'):
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
             # --- PRE-PASS: Register all types (Structs/Classes) to allow out-of-order usage ---
             for item in node:
                 if item.__class__.__name__ == 'ClassNode':
                     self.symbol_table.set(item.name, 'class_definition', value=item)
                 elif item.__class__.__name__ == 'QaabNode':
                     self.symbol_table.set(item.name, 'struct_definition', value=item)
                 elif item.__class__.__name__ == 'QeexNode':
                     if isinstance(item.value, IdentifierNode) and item.name == item.value.name:
                         self.symbol_table.set(item.name, "c_type", value=item.value)
                 elif item.__class__.__name__ == 'FunctionNode':
                     self.symbol_table.set(item.name, "hawl", value=item)
                 elif item.__class__.__name__ == 'KeydNode':
                     self.symbol_table.set(item.var_name, str(item.var_type).strip(), value=item)

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
        if isinstance(node, TypeLiteralNode): return f"nooc:{node.type_name}"
        if isinstance(node, DictionaryInitializationNode): return "qaamuus"
        if isinstance(node, QaabQiimeNode): return node.struct_name
        if isinstance(node, CCallNode): return "walbo"
        if isinstance(node, ArrayTypeQueryNode): return "eray"
        if isinstance(node, FunctionCallNode):
            if node.name == "tix_cayiman":
                return "tix"
            info = self.symbol_table.get(node.name)
            if info:
                if isinstance(info[1], FunctionTypeNode): return info[1].return_type
                if info[1] == "hawl": return info[0].return_type
            return "walbo"
            
        if isinstance(node, LambdaNode):
            param_types = [p.param_type for p in node.params]
            return FunctionTypeNode(node.line, param_types, node.return_type, node.filename)

        if isinstance(node, ArrayAccessNode):
            array_type = self.get_expression_type(node.array_name_node)
            if isinstance(array_type, ArrayTypeNode):
                return str(array_type.element_type) if array_type.element_type else "walbo"
            if isinstance(array_type, str) and array_type.startswith("tix:"):
                return array_type[4:]
            return "walbo"

        if isinstance(node, DictionaryAccessNode):
            return "walbo"

        if isinstance(node, ClassInstantiationNode): return node.class_name
        if isinstance(node, ThisNode):
            return getattr(node, 'resolved_class_name', self.current_class.name if self.current_class else "unknown")
        if isinstance(node, WaalidNode):
            return getattr(node, 'resolved_parent_name', self.current_class.parent_name if self.current_class and self.current_class.parent_name else "unknown")
        if isinstance(node, MemberAccessNode):
            obj_type = self.get_expression_type(node.object_node)
            if str(obj_type) in ("walbo", "qaamuus", "unknown"): return "walbo"
            
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
            
            if str(obj_type).startswith("tix") or str(obj_type) == "tix": 
                return "walbo" # Array methods often return elements (walbo) or specific types handled elsewhere

            if str(obj_type) in ("eray", "tiro", "jajab", "miyaa", "xaraf", "qaamuus"):
                info = self.symbol_table.get(node.method_name)
                if info and info[1] == "hawl":
                    return str(info[0].return_type)
                return "unknown"
                
            if str(obj_type) in ("walbo", "unknown"): 
                return "walbo" 
                
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
            return "walbo"
            
        if isinstance(node, ArrayInitializationNode):
            if not node.elements:
                return ArrayTypeNode(node.line, None, node.filename) # Empty mixed array
            first_type = self.get_expression_type(node.elements[0])
            # Check if all elements are the same type
            is_homogeneous = True
            for i in range(1, len(node.elements)):
                if str(self.get_expression_type(node.elements[i])) != str(first_type):
                    is_homogeneous = False
                    break
            if is_homogeneous:
                return ArrayTypeNode(node.line, first_type, node.filename)
            else:
                return ArrayTypeNode(node.line, None, node.filename) # Mixed array

        if isinstance(node, IdentifierNode):
            info = self.symbol_table.get(node.name)
            if info:
                # If the identifier is a function, reconstruct its full FunctionTypeNode
                if info[1] == "hawl":
                    func_node = info[0]
                    return FunctionTypeNode(
                        func_node.line, 
                        [p.param_type for p in func_node.params], 
                        func_node.return_type, 
                        func_node.filename
                    )
                # Otherwise return the standard type string
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
            
            if node.op in ('==', '!=', '>', '<', '>=', '<=', '=<', '===', 'iyo', 'ama', '&&', '||', '!', 'ahayn'):
                return "miyaa"

        return "unknown"
    
    def check_IdentifierNode(self, node: IdentifierNode):
        if not self.symbol_table.get(node.name):
            raise SemanticError(ERR_IDENTIFIER_NOT_FOUND(node.name), node.filename, node.line)
        if self.tracker.is_moved(node.name):
            move_node = self.tracker.get_move_node(node.name)
            move_line = move_node.line if move_node else "aan la aqoon"
            raise SemanticError(ERR_USE_AFTER_MOVE(node.name, move_line), node.filename, node.line)
        if not self.tracker.is_initialized(node.name):
            raise SemanticError(ERR_UNINITIALIZED_VARIABLE(node.name), node.filename, node.line)
        return self.get_expression_type(node)

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


    def check_AssignmentNode(self, node: AssignmentNode):
        needs_cleanup = False
        if isinstance(node.identifier, IdentifierNode):
            target_type = self.get_expression_type(node.identifier)
        else:
            target_type = self.check(node.identifier)
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
            self.symbol_table.set(p.name, p.param_type)
            p.borrowed = self._is_borrowed_param_type(p.param_type)
            self.tracker.record_definition(
                p.name,
                p.param_type,
                p,
                is_initialized=True,
                borrowed=p.borrowed,
            )
        self.check(node.body)
        node.cleanup_vars = self.tracker.pop_scope()
        self.symbol_table.pop_scope()
        
        self.current_function = old_function

    def check_LambdaNode(self, node: LambdaNode):
        # Determine return type
        if node.is_concise:
            # For concise lambdas (=> expr), we'll infer the type after checking the expression
            pass
        else:
            self._ensure_valid_type(node.return_type, node)

        for p in node.params:
            self._ensure_valid_type(p.param_type, p)

        old_function = self.current_function
        self.current_function = node # Lambda acts as a function context for 'soo_celi'
        
        self.symbol_table.push_scope()
        self.tracker.push_scope()
        for p in node.params:
            self.symbol_table.set(p.name, p.param_type)
            p.borrowed = self._is_borrowed_param_type(p.param_type)
            self.tracker.record_definition(
                p.name,
                p.param_type,
                p,
                is_initialized=True,
                borrowed=p.borrowed,
            )
        
        ret_type = node.return_type
        if node.is_concise:
            # In concise lambdas, the body is a single expression
            ret_type = self.check(node.body)
            # Update the node's return_type for code generation
            node.return_type = ret_type
        else:
            # Check the body statements
            self.check(node.body)
        
        node.cleanup_vars = self.tracker.pop_scope()
        self.symbol_table.pop_scope()
        self.current_function = old_function

        # Return the FunctionTypeNode representing this lambda
        param_types = [p.param_type for p in node.params]
        return FunctionTypeNode(node.line, param_types, ret_type, node.filename)

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
            elem_type = arr_type.element_type if arr_type.element_type else "walbo"
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
    def check_CCallNode(self, node: CCallNode): return "walbo"
    def check_TypeLiteralNode(self, node: TypeLiteralNode):
        return f"nooc:{node.type_name}"

    def _resolve_array_query_type(self, identifier_name, node):
        info = self.symbol_table.get(identifier_name)
        if not info:
            raise SemanticError(ERR_IDENTIFIER_NOT_FOUND(identifier_name), node.filename, node.line)

        array_type = info[1]

        if isinstance(array_type, ArrayTypeNode):
            if array_type.element_type is None:
                return "walbo"
            return str(array_type.element_type)

        array_type_str = str(array_type).strip()
        if not array_type_str.startswith("tix"):
            raise SemanticError(ERR_NOOC_TIX_QUERY(), node.filename, node.line)

        if array_type_str == "tix":
            return "walbo"

        return array_type_str[4:]

    def check_ArrayTypeQueryNode(self, node: ArrayTypeQueryNode):
        self._resolve_array_query_type(node.identifier, node)
        return "eray"

    def check_ArrayAccessNode(self, node: ArrayAccessNode):
        self.check(node.array_name_node)
        self.check(node.index_expression)
        return self.get_expression_type(node)

    def check_DictionaryAccessNode(self, node: DictionaryAccessNode):
        self.check(node.dictionary_node)
        self.check(node.key_node)
        return "walbo"

    def check_DictionaryAssignmentNode(self, node: DictionaryAssignmentNode):
        self.check(node.dictionary_access_node)
        self.check(node.value_node)

    def check_QaabQiimeNode(self, node: QaabQiimeNode):
        for val in node.values:
            self.check(val)
        return node.struct_name
    

    #
    """
        this code i commented becuase it ordering matter here is the issue i am getting:

            keyd:tiro n = 1; i declare n
            then i move n to n1
            keyd:tiro n1 = n; //so the issue is happening because in i got message ERR_USE_AFTER_MOVE in this block i commeted so why i am getting this bexuase of in check_keydnode was recorded that variable in the moved_variables variable through record_move function and this block of code was latter excuted and it sees that the variable was already in moved_variables dictionary list
    """
    
    # def check_IdentifierNode(self, node: IdentifierNode):
    #     if not self.symbol_table.get(node.name):
    #         raise SemanticError(ERR_IDENTIFIER_NOT_FOUND(node.name), node.filename, node.line)
    #     if self.tracker.is_moved(node.name):
    #         print("Kani horey ayaa loo wareejiyay ", node.name)
    #         raise SemanticError(ERR_USE_AFTER_MOVE(node.name, "Moved"), node.filename, node.line)
    #     if not self.tracker.is_initialized(node.name):
    #         raise SemanticError(ERR_UNINITIALIZED_VARIABLE(node.name), node.filename, node.line)
    #     return self.get_expression_type(node)

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

    def check_HelNode(self, node: HelNode):
        info = self.symbol_table.get(node.identifier)
        if not info:
            raise SemanticError(ERR_IDENTIFIER_NOT_FOUND(node.identifier), node.filename, node.line)

        var_type = str(info[1]).strip()
        node.needs_cleanup = (
            var_type == "eray"
            and self.tracker.is_initialized(node.identifier)
            and not self.tracker.is_moved(node.identifier)
        )

        self.tracker.revive(node.identifier)
        self.tracker.mark_initialized(node.identifier)
        return var_type


    def check_FunctionCallNode(self, node: FunctionCallNode):
        if node.name == "tix_cayiman":
            for arg in node.params:
                self.check(arg)
            return "tix"

        info = self.symbol_table.get(node.name)
        if not info:
             raise SemanticError(ERR_FUNCTION_NOT_FOUND(node.name), node.filename, node.line)
        
        if isinstance(info[1], FunctionTypeNode):
             func_type = info[1]
             if len(node.params) != len(func_type.param_types):
                 raise SemanticError(
                     ERR_ARG_COUNT_MISMATCH(node.name, len(func_type.param_types), len(node.params)), 
                     node.filename, node.line
                 )
             for i, arg in enumerate(node.params):
                 arg_type = self.check(arg)
                 expected_type = func_type.param_types[i]
                 if not self._are_types_compatible(expected_type, arg_type):
                     raise SemanticError(
                         ERR_ARG_TYPE_MISMATCH_SIMPLE(i+1, node.name, str(expected_type), str(arg_type)),
                         node.filename,
                         node.line
                     )
             return func_type.return_type
             
        if info[1] == "hawl":
            func_node = info[0]
            
            # Support Named Arguments & Defaults
            ordered_args = [None] * len(func_node.params)
            provided_names = set()
            
            # First pass: Positional arguments
            positional_count = 0
            for i, arg in enumerate(node.params):
                if isinstance(arg, NamedArgument):
                    break # Stop positional at the first named argument
                if i >= len(func_node.params):
                    raise SemanticError(
                        ERR_ARG_COUNT_MISMATCH(node.name, len(func_node.params), len(node.params)), 
                        node.filename, node.line
                    )
                ordered_args[i] = arg
                provided_names.add(func_node.params[i].name)
                positional_count += 1
                
            # Second pass: Named arguments
            for i in range(positional_count, len(node.params)):
                arg = node.params[i]
                if not isinstance(arg, NamedArgument):
                    raise SemanticError(
                        ERR_POSITIONAL_AFTER_NAMED(node.name), 
                        node.filename, node.line
                    )
                
                # Find the parameter in the function signature
                param_idx = -1
                for p_idx, p in enumerate(func_node.params):
                    if p.name == arg.name:
                        param_idx = p_idx
                        break
                
                if param_idx == -1:
                    raise SemanticError(
                        ERR_UNRECOGNIZED_NAMED_ARG(arg.name, node.name), 
                        node.filename, node.line
                    )
                
                if func_node.params[param_idx].name in provided_names:
                    raise SemanticError(
                        ERR_DUPLICATE_NAMED_ARG(arg.name, node.name), 
                        node.filename, node.line
                    )
                
                ordered_args[param_idx] = arg.value
                provided_names.add(arg.name)
                
            # Third pass: Apply defaults for missing arguments
            for i, p in enumerate(func_node.params):
                if ordered_args[i] is None:
                    if p.default_value is not None:
                        ordered_args[i] = p.default_value
                    else:
                        raise SemanticError(
                            ERR_MISSING_ARG(p.name, node.name, "...", "..."), 
                            node.filename, node.line
                        )
            
            # Store ordered_args for the code generator to use
            node.ordered_args = ordered_args
            
            # Check argument types against the function signature
            for i, arg in enumerate(ordered_args):
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

    def check_DictionaryInitializationNode(self, node: DictionaryInitializationNode):
        for key, value in node.pairs:
            self.check(key)
            self.check(value)
        return "qaamuus"

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
        
        if node.op in ('==', '!=', '>', '<', '>=', '<=', '=<', '==='):
            return "miyaa"
            
        # Logical operations
        if node.op in ('iyo', 'ama', '&&', '||'):
            if not self._are_types_compatible('miyaa', left_type) or not self._are_types_compatible('miyaa', right_type):
                 raise SemanticError(
                    ERR_BINARY_OP_TYPE_MISMATCH(str(left_type), str(right_type), node.op),
                    node.filename,
                    node.line
                )
            return "miyaa"

        # Unary logical negation parsed as binary
        if node.op in ('!', 'ahayn'):
            if not self._are_types_compatible('miyaa', right_type):
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
        obj_type = self.check(node.object_node)

        # Prevent accessing members on primitive types (except classes/structs)
        primitive_types = {"tiro", "jajab", "eray", "xaraf", "miyaa", "waxbo"}
        if str(obj_type) in primitive_types:
             raise SemanticError(ERR_NOT_A_CLASS(str(obj_type)), node.filename, node.line)

        # Check if the member exists
        res_type = self.get_expression_type(node)
        if res_type == "unknown":
             raise SemanticError(ERR_MEMBER_NOT_FOUND(str(obj_type), node.member_name), node.filename, node.line)

        return res_type

    def check_MethodCallNode(self, node: MethodCallNode):
        obj_type = self.check(node.object_node)
        for arg in node.args_list:
            self.check(arg)

        # Check if it's an array method. Array methods are still somewhat special due to generics.
        if str(obj_type).startswith("tix") or str(obj_type) == "tix":
            valid_arr_methods = {"gali", "kasaar", "dherer"}
            if node.method_name not in valid_arr_methods:
                raise SemanticError(ERR_METHOD_NOT_FOUND_ON_ARRAY(node.method_name), node.filename, node.line)
            return "walbo"

        # Primitive Method Fallback: If obj_type is a primitive (like 'eray', 'tiro'), check for a global function.
        if str(obj_type) in ("eray", "tiro", "jajab", "miyaa", "xaraf", "qaamuus"):
            info = self.symbol_table.get(node.method_name)
            if info and info[1] == "hawl":
                func_node = info[0]
                # Check if the first parameter matches the object type (or is 'walbo')
                if not func_node.params or not self._are_types_compatible(func_node.params[0].param_type, obj_type):
                    raise SemanticError(f"Hawsha '{node.method_name}' ma aqbasho nooca '{obj_type}' in ay tahay parameter-ka kowaad.", node.filename, node.line)
                
                # Verify remaining arguments match
                if len(node.args_list) != len(func_node.params) - 1:
                    raise SemanticError(f"Hawsha '{node.method_name}' waxay u baahan tahay {len(func_node.params) - 1} argument, laakiin waxaad siisay {len(node.args_list)}.", node.filename, node.line)
                
                # Note: For full type checking of arguments, we would do it here, but skipping for brevity
                node.is_primitive_method = True
                return func_node.return_type
            else:
                raise SemanticError(f"Hawsha '{node.method_name}' ma ahan mid jirta oo ku shuban nooca '{obj_type}'.", node.filename, node.line)


        # Resolve the method in the class hierarchy
        res_type = self.get_expression_type(node)
        if res_type != "unknown": 
             class_info = self.symbol_table.get(str(obj_type))
             if class_info and class_info[1] == 'class_definition':
                 found = False
                 current_class = class_info[0]
                 while current_class:
                     for m in current_class.methods:
                         if m.name == node.method_name:
                             node.method_node = m
                             node.method_source_class = current_class
                             found = True
                             break
                     if found: break
                     
                     if getattr(current_class, 'parent_name', None):
                         parent_info = self.symbol_table.get(current_class.parent_name)
                         current_class = parent_info[0] if parent_info else None
                     else:
                         break
                 if not found:
                     raise SemanticError(ERR_MEMBER_NOT_FOUND(str(obj_type), node.method_name), node.filename, node.line)

        return res_type
    def check_ThisNode(self, node: ThisNode):
        if self.current_class:
            node.resolved_class_name = self.current_class.name
        return self.get_expression_type(node)
        
    def check_WaalidNode(self, node: WaalidNode):
        if self.current_class and getattr(self.current_class, 'parent_name', None):
            node.resolved_parent_name = self.current_class.parent_name
        return self.get_expression_type(node)
