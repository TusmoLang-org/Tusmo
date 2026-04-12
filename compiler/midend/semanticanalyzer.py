# semanticanalyzer.py (Final Clean Version)

from compiler.frontend.parser.ast_nodes import (
    KeydNode, AssignmentNode, IdentifierNode, FunctionNode, FunctionCallNode,
    IfNode, QorNode, HelNode, ReturnStatementNode, BinaryOpNode, NumberNode,
    StringNode, FloatNode, CharNode, BooleanNode, FStringNode, TernaryOpNode, ASTNode,
    ArrayTypeNode, ArrayInitializationNode, ArrayAccessNode, ArrayAssignmentNode, ArrayTypeQueryNode,
    WhileNode, DoWhileNode, ForRangeNode, ForEachNode, MethodCallNode,
    ClassNode, ClassInstantiationNode, MemberAccessNode, ThisNode, CCallNode, WaalidNode,
    DictionaryInitializationNode, DictionaryAccessNode, DictionaryAssignmentNode,
    FunctionTypeNode, ParameterNode, BreakNode, ContinueNode, NamedArgument, TypeLiteralNode
)
from compiler.midend.symbol_table import SymbolTable
from compiler.midend.built_in_fn import functions_

from compiler.midend.semantic_errors import *

class SemanticChecker:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.current_function = None
        self.current_class = None
        self.loop_depth = 0

    def _are_types_compatible(self, declared_type, value_type):
        if declared_type is None: return True
        if isinstance(declared_type, ASTNode) and not isinstance(declared_type, FunctionTypeNode):
            declared_type = str(declared_type)
        if isinstance(value_type, ASTNode) and not isinstance(value_type, FunctionTypeNode):
            value_type = str(value_type)
        if declared_type == value_type:
            return True

        if isinstance(declared_type, str) and isinstance(value_type, str):
            if declared_type == 'dynamic_value' or value_type == 'dynamic_value':
                return True
            
            if declared_type == 'None': # Mixed array
                return True
            
            # Empty array [] is compatible with any typed array
            if declared_type.startswith('tix:') and value_type == 'tix':
                return True

            # Empty 2D array [[]] is compatible with any typed 2D array
            if declared_type.startswith('tix:tix:') and (value_type == 'tix:tix' or value_type.startswith('tix:tix:')):
                return True

            if declared_type == 'qaamuus' and value_type == 'qaamuus':
                return True
            
            if declared_type == 'hawl' and value_type == 'hawl':
                return True

        if isinstance(declared_type, FunctionTypeNode) and isinstance(value_type, FunctionTypeNode):
            if len(declared_type.param_types) != len(value_type.param_types):
                return False
            return all(self._are_types_compatible(dt, vt) for dt, vt in zip(declared_type.param_types, value_type.param_types)) and self._are_types_compatible(declared_type.return_type, value_type.return_type)
        
        if isinstance(declared_type, FunctionTypeNode) and value_type == 'hawl': return True
        if declared_type == 'hawl' and isinstance(value_type, FunctionTypeNode): return True
        return False

    def _get_array_depth(self, array_type):
        """Get the depth of nested arrays (1 for tix:tiro, 2 for tix:tix:tiro, etc.)"""
        depth = 0
        current = array_type
        while isinstance(current, ArrayTypeNode):
            depth += 1
            current = current.element_type
        return depth

    def _resolve_call_arguments(self, args, params, call_node, context="call"):
        """
        Reorder positional/keyword args to match parameter order and fill defaults.
        Returns ordered list and sets call_node.ordered_args.
        """
        param_index = {p.name: idx for idx, p in enumerate(params)}
        ordered = [None] * len(params)
        provided = [False] * len(params)
        next_pos = 0
        seen_named = False

        for arg in args:
            if isinstance(arg, NamedArgument):
                seen_named = True
                if arg.name not in param_index:
                    raise SemanticError(ERR_UNRECOGNIZED_NAMED_ARG(arg.name, context), arg.filename, arg.line)
                
                idx = param_index[arg.name]
                if provided[idx]:
                    raise SemanticError(ERR_DUPLICATE_NAMED_ARG(arg.name, context), arg.filename, arg.line)
                ordered[idx] = arg.value
                provided[idx] = True
            else:
                if seen_named:
                    raise SemanticError(ERR_POSITIONAL_AFTER_NAMED(context), arg.filename, arg.line)
                if next_pos >= len(params):
                    raise SemanticError(ERR_TOO_MANY_ARGS(context), call_node.filename, call_node.line)
                ordered[next_pos] = arg
                provided[next_pos] = True
                next_pos += 1

        for i, p in enumerate(params):
            if not provided[i]:
                if p.default_value is not None:
                    ordered[i] = p.default_value
                else:
                    khalad_list = ", ".join([param.name for param in params if param.name != p.name])
                    sax_list = ", ".join([param.name for param in params])
                    raise SemanticError(ERR_MISSING_ARG(p.name, context, khalad_list, sax_list), call_node.filename, call_node.line)
        
        call_node.ordered_args = ordered
        return ordered



    def check(self, node):

        if node is None: return
        if isinstance(node, list):
            for item in node: self.check(item)
            return
        method_name = f"check_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_check)
        return method(node)



    def generic_check(self, node):
        for attr_name in dir(node):
            if not attr_name.startswith("__"):
                value = getattr(node, attr_name)

                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, ASTNode): self.check(item)
                elif isinstance(value, ASTNode): self.check(value)



    def get_expression_type(self, node: ASTNode, skip_context_check=False):

        """

        Get the type of an expression node.

        

        Args:

            node: The AST node to get the type of

            skip_context_check: If True, skip validation checks (used during code generation)

        """

        if not isinstance(node, ASTNode):
            print(f"get_expression_type waxaa la siiyay wax aan ASTNode ahayn: {type(node).__name__}")

        if isinstance(node, NumberNode): return "tiro"

        if isinstance(node, FloatNode): return "jajab"

        if isinstance(node, StringNode): return "eray"

        if isinstance(node, CharNode): return "xaraf"

        if isinstance(node, BooleanNode): return "miyaa"
        if isinstance(node, NamedArgument): return self.get_expression_type(node.value, skip_context_check)

        if isinstance(node, FStringNode):
            return "eray"

        if isinstance(node, TypeLiteralNode):
            return f"nooc:{node.type_name}"

        if isinstance(node, DictionaryInitializationNode): return "qaamuus"
        
        if isinstance(node, WaalidNode):
            if self.current_class and self.current_class.parent_name:
                return self.current_class.parent_name
            return None

        if isinstance(node, ThisNode):
            # First try the current_class attribute
            if self.current_class:
                return self.current_class.name
            
            # Then try looking up 'kan' in the symbol table (it's set in check_FunctionNode for methods)
            kan_info = self.symbol_table.get('kan')
            if kan_info:
                return kan_info[1]
            
            # If both fail, and we are not skipping context checks, it's an error
            if not skip_context_check:
                raise SemanticError(ERR_KAN_OUTSIDE_KOOX(), node.filename, node.line)
            return None

        

        if isinstance(node, ArrayTypeQueryNode):
            var_info = self.symbol_table.get(node.identifier)
            # Check if the variable exists and if it is actually an array
            if not skip_context_check:
                if not var_info:
                    raise SemanticError(ERR_UNDEFINED_VARIABLE(node.identifier), node.filename, node.line)
                
                # This is the key check:
                if not isinstance(var_info[1], (ArrayTypeNode, str)) or (isinstance(var_info[1], str) and "tix" not in var_info[1]):
                     # If it's a string like 'tiro', it's not an array
                     if not isinstance(var_info[1], ArrayTypeNode):
                        raise SemanticError(ERR_NOT_AN_ARRAY(node.identifier, var_info[1]), node.filename, node.line)

            return var_info[1] if var_info else None

        if isinstance(node, IdentifierNode):
            var_info = self.symbol_table.get(node.name)
            if not skip_context_check and not var_info:
                raise SemanticError(ERR_UNDEFINED_VARIABLE(node.name), node.filename, node.line)
            return var_info[1] if var_info else "dynamic_value"

        if isinstance(node, ClassInstantiationNode):

            class_info = self.symbol_table.get(node.class_name)

            if not skip_context_check and (not class_info or class_info[1] != 'class_definition'):

                raise SemanticError(ERR_UNDEFINED_CLASS(node.class_name), node.filename, node.line)

            return node.class_name

        if isinstance(node, MemberAccessNode):

            object_type_name = str(self.get_expression_type(node.object_node, skip_context_check))

            # If we couldn't determine the object type during code generation,

            # it might be 'kan' (ThisNode) - try to infer from the identifier lookup

            if not object_type_name or object_type_name == 'None':

                # Check if the object_node is an IdentifierNode and look it up

                if isinstance(node.object_node, IdentifierNode):

                    var_info = self.symbol_table.get(node.object_node.name)

                    if var_info:

                        object_type_name = str(var_info[1])

            

            if not object_type_name or object_type_name == 'None':

                return None

                

            class_info = self.symbol_table.get(object_type_name)

            if not skip_context_check and (not class_info or not isinstance(class_info[0], ClassNode)):

                raise SemanticError(ERR_NOT_A_CLASS(object_type_name), node.filename, node.line)

            if not class_info:

                return None

            class_node = class_info[0]
            current_class = class_node
            
            while current_class:
                member = next((m for m in current_class.members if m.var_name == node.member_name), None)
                if member:
                    return member.var_type
                
                if getattr(current_class, 'parent_class', None):
                    current_class = current_class.parent_class
                else:
                    break

            if not skip_context_check:
                raise SemanticError(ERR_MEMBER_NOT_FOUND(object_type_name, node.member_name), node.filename, node.line)

            return None


        if isinstance(node, MethodCallNode):
            object_type = self.get_expression_type(node.object_node, skip_context_check)
            
            if isinstance(object_type, ArrayTypeNode):
                if node.method_name == 'gali':
                    if len(node.args_list) == 1:
                        # Append: gali(value) - can be single element OR array
                        arg_type = self.get_expression_type(node.args_list[0])
                        
                        # Check if arg is an array with compatible element type
                        if isinstance(arg_type, ArrayTypeNode):
                            # Check if this is adding to a nested array (e.g., adding row to 2D array)
                            obj_depth = self._get_array_depth(object_type)
                            arg_depth = self._get_array_depth(arg_type)
                            
                            if obj_depth > arg_depth:
                                # Adding a flatter array to a deeper nested array (e.g., [1,2,3] to tix:tix:tiro)
                                # This is adding a row, which is OK - let code gen handle it
                                pass
                            else:
                                # Normal extend - check element type compatibility
                                obj_elem = object_type.element_type
                                arg_elem = arg_type.element_type
                                if isinstance(obj_elem, ArrayTypeNode):
                                    # Nested array element
                                    if not self._are_types_compatible(obj_elem, arg_elem):
                                        raise SemanticError(ERR_TYPE_MISMATCH(object_type.element_type, arg_type.element_type), node.filename, node.line)
                                elif not self._are_types_compatible(obj_elem, arg_elem):
                                    raise SemanticError(ERR_TYPE_MISMATCH(object_type.element_type, arg_type), node.filename, node.line)
                        elif not self._are_types_compatible(object_type.element_type, arg_type):
                            raise SemanticError(ERR_TYPE_MISMATCH(object_type.element_type, arg_type), node.filename, node.line)
                    elif len(node.args_list) == 2:
                        # Insert: gali(boos=i, value)
                        # Check first arg is named 'boos'
                        first_arg = node.args_list[0]
                        if not isinstance(first_arg, NamedArgument) or first_arg.name != 'boos':
                             raise SemanticError(ERR_GALI_BOOS_MISSING(), node.filename, node.line)
                        
                        index_type = self.get_expression_type(first_arg.value)
                        if str(index_type) != 'tiro':
                             raise SemanticError(ERR_INDEX_NOT_INT(), node.filename, node.line)
                        
                        val_type = self.get_expression_type(node.args_list[1])
                        if not self._are_types_compatible(object_type.element_type, val_type):
                             raise SemanticError(ERR_TYPE_MISMATCH(object_type.element_type, val_type), node.filename, node.line)
                    else:
                        raise SemanticError(ERR_GALI_ARG_COUNT(), node.filename, node.line)
                    return 'waxbo'

                elif node.method_name == 'kasaar':
                    if len(node.args_list) != 1:
                        raise SemanticError(ERR_KASAAR_ARG_COUNT(), node.filename, node.line)
                    
                    arg = node.args_list[0]
                    if isinstance(arg, NamedArgument) and arg.name == 'boos':
                        # Remove by index: kasaar(boos=i)
                        index_type = self.get_expression_type(arg.value)
                        if str(index_type) != 'tiro':
                             raise SemanticError(ERR_INDEX_NOT_INT(), node.filename, node.line)
                        return object_type.element_type
                    else:
                        # Remove by value: kasaar(value)
                        val_type = self.get_expression_type(arg)
                        if not self._are_types_compatible(object_type.element_type, val_type):
                             raise SemanticError(ERR_ARRAY_TYPE_MISMATCH(object_type.element_type, val_type), node.filename, node.line)
                        return 'miyaa'

                elif not skip_context_check:
                    raise SemanticError(ERR_METHOD_NOT_FOUND_ON_ARRAY(node.method_name), node.filename, node.line)

            if str(object_type) == 'qaamuus':
                if node.method_name == 'kasaar': return 'waxbo'
                if node.method_name == 'majiraa': return 'miyaa'
                return None
            
            # Handle string methods
            if str(object_type) == 'eray':
                # String methods: XarafWeyn, XarafYar, kaReeb, Bkareeb, Mkareeb, kuBadal, sooRaadi, lagaHelay, qaybi
                if node.method_name in ['XarafWeyn', 'XarafYar', 'kaReeb', 'Bkareeb', 'Mkareeb', 'kuBadal']:
                    return 'eray'
                if node.method_name == 'sooRaadi':
                    return 'tiro'
                if node.method_name == 'lagaHelay':
                    return 'miyaa'
                if node.method_name == 'qaybi':
                    return 'tix:eray'
                return None

            class_info = self.symbol_table.get(str(object_type))
            if not class_info: return None
            
            class_node = class_info[0]
            for method in class_node.methods:
                if method.name == node.method_name:
                    return method.return_type
            return None
        if isinstance(node, ArrayAccessNode):
            base_type = self.get_expression_type(node.array_name_node, skip_context_check)

            if not skip_context_check and not isinstance(base_type, ArrayTypeNode) and str(base_type) != 'eray' and str(base_type) != 'qaamuus' and str(base_type) != 'dynamic_value':

                raise SemanticError(ERR_NOT_AN_ARRAY_SIMPLE(), node.filename, node.line)

            if isinstance(base_type, ArrayTypeNode):

                # If the array holds dictionaries or is mixed, access returns a dynamic value

                if base_type.element_type is None or str(base_type.element_type) == 'qaamuus':

                    return "dynamic_value"

                return base_type.element_type

            if str(base_type) == 'eray':

                return 'xaraf'

            if str(base_type) == 'qaamuus':
                return "dynamic_value"

            # dynamic_value is a TusmoValue from a mixed array - accessing it returns another dynamic_value
            if str(base_type) == 'dynamic_value':

                return "dynamic_value"

            return None

        if isinstance(node, DictionaryAccessNode):
            base_type = self.get_expression_type(node.dictionary_node, skip_context_check)

            if not skip_context_check and str(base_type) != 'qaamuus':

                raise SemanticError(ERR_NOT_A_DICTIONARY_SIMPLE(), node.filename, node.line)
            
            # Validate key type (only when not skipping context check)
            if not skip_context_check:
                key_type = self.get_expression_type(node.key_node, skip_context_check)
                if str(key_type) != 'eray':
                    raise SemanticError(ERR_DICT_KEY_NOT_STRING(key_type), node.key_node.filename, node.key_node.line)

            return "dynamic_value" # Dictionaries hold dynamic values

        if isinstance(node, ArrayInitializationNode):

            if not node.elements:

                return ArrayTypeNode(line=node.line, element_type=None, filename=node.filename)

            

            # Check if all elements have the same type

            first_element_type = self.get_expression_type(node.elements[0], skip_context_check)

            is_homogeneous = True

            

            for elem in node.elements[1:]:

                elem_type = self.get_expression_type(elem, skip_context_check)

                if str(elem_type) != str(first_element_type):

                    is_homogeneous = False

                    break

            

            if is_homogeneous:

                # All elements have the same type - homogeneous array

                return ArrayTypeNode(line=node.line, element_type=first_element_type, filename=node.filename)

            else:

                # Elements have different types - heterogeneous/mixed array

                return ArrayTypeNode(line=node.line, element_type=None, filename=node.filename)

        if isinstance(node, BinaryOpNode):

            op = node.op
            left_type = self.get_expression_type(node.left, skip_context_check)
            right_type = self.get_expression_type(node.right, skip_context_check)

            if op in ('>', '<', '>=', '<=', '==', '!=', 'iyo', 'ama', '&&', '||'):
                # Allow type comparison for == and !=
                if op in ('==', '!=') and (str(left_type).startswith("nooc:") or str(right_type).startswith("nooc:")):
                    return "miyaa"
                return "miyaa"

            if op == '+' and ('eray' in (str(left_type), str(right_type))): return 'eray'

            return left_type

        if isinstance(node, FunctionCallNode):

            if node.name == 'tix_cayiman':

                return ArrayTypeNode(line=node.line, element_type=None, filename=node.filename)



            func_info = self.symbol_table.get(node.name)

        

            # Check if it's a built-in function

            is_builtin = node.name in functions_

        

            if not skip_context_check and (not func_info or (func_info[1] != 'hawl' and not isinstance(func_info[1], FunctionTypeNode))) and not is_builtin:

                raise SemanticError(

                    f"Cilad Macne: Hawsha '{node.name}' lama helin ama maaha hawl.\n"

                    f"\t\tFaylka: '{node.filename}', Sadarka: {node.line}"

                )

        

            # Return type from symbol table for user-defined functions

            if func_info:
                if isinstance(func_info[1], FunctionTypeNode):
                    return func_info[1].return_type
                else: # 'hawl'
                    return func_info[2]

        

            # Return type from built-in functions registry

            if is_builtin:

                return_type = functions_[node.name].get('return_type')

                if return_type:

                    return return_type



            return None

        if isinstance(node, TernaryOpNode):

            return self.get_expression_type(node.if_true, skip_context_check)

        if isinstance(node, CCallNode):
            # No hardcoded mappings - all types defined in stdlib wrappers!
            if node.c_function_name == "tusmo_qaamuus_has_key":
                return "miyaa"
            if self.current_function:
                return self.current_function.return_type
            return "dynamic_value"

        if not skip_context_check:

            raise SemanticError(ERR_UNKNOWN_EXPR_TYPE(type(node).__name__), node.filename, getattr(node, 'line', 'unknown'))

        return None



    def check_ClassNode(self, node: ClassNode):
        if not node.name[0].isupper():
            raise SemanticError(ERR_CLASS_NAME_NOT_CAPITAL(node.name), node.filename, node.line)

        if self.symbol_table.exists_in_current_scope(node.name):
            raise SemanticError(ERR_CLASS_REDEFINED(node.name), node.filename, node.line)

        self.symbol_table.set(node.name, 'class_definition', value=node)
        
        # Inheritance Logic
        if node.parent_name:
            parent_info = self.symbol_table.get(node.parent_name)
            if not parent_info or parent_info[1] != 'class_definition':
                 raise SemanticError(ERR_CLASS_INHERITS_UNKNOWN(node.name, node.parent_name), node.filename, node.line)
            
            parent_node = parent_info[0]
            node.parent_class = parent_node # Link to AST
            
            # 1. Cycle Detection
            current = parent_node
            while getattr(current, 'parent_name', None):
                if current.parent_name == node.name:
                    raise SemanticError(ERR_INHERITANCE_CYCLE(node.name, parent_node.name), node.filename, node.line)
                
                 # Look up grand-parent
                grand_parent_info = self.symbol_table.get(current.parent_name)
                if grand_parent_info and grand_parent_info[1] == 'class_definition':
                    current = grand_parent_info[0]
                else:
                    break
        else:
             node.parent_class = None



        previous_class = self.current_class

        self.current_class = node

        self.symbol_table.push_scope()



        for member in node.members:

            self.check(member)

        for method in node.methods:

            self.check(method)



        self.symbol_table.pop_scope()

        self.current_class = previous_class



    def check_ClassInstantiationNode(self, node: ClassInstantiationNode):

        class_info = self.symbol_table.get(node.class_name)

        if not class_info or class_info[1] != 'class_definition':

            raise SemanticError(ERR_CLASS_INSTANTIATION_NOT_A_CLASS(node.class_name), node.filename, node.line)

        class_node = class_info[0]

        constructor = next((m for m in class_node.methods if m.name == 'dhis'), None)

        if not constructor and node.constructor_args:
            raise SemanticError(ERR_NO_CONSTRUCTOR(node.class_name, len(node.constructor_args)), node.filename, node.line)

        if constructor:

            node.constructor_args = self._resolve_call_arguments(node.constructor_args, constructor.params, node, context="constructor")

            for i, arg_node in enumerate(node.constructor_args):

                arg_type = self.get_expression_type(arg_node)

                param_def = constructor.params[i]
                if isinstance(param_def, ParameterNode):
                    param_type = param_def.param_type
                else:
                    param_type = param_def[1]

                if not self._are_types_compatible(param_type, arg_type):

                    raise SemanticError(ERR_CONSTRUCTOR_ARG_TYPE_MISMATCH(i+1, node.class_name, param_type, arg_type), node.filename, node.line)

        self.check(node.constructor_args)



    def check_KeydNode(self, node: KeydNode):

        if self.symbol_table.exists_in_current_scope(node.var_name):

            raise SemanticError(ERR_VARIABLE_REDEFINED(node.var_name), node.filename, node.line)

        if isinstance(node.var_type, str):

            type_info = self.symbol_table.get(node.var_type)

            is_primitive = node.var_type in ['tiro', 'eray', 'jajab', 'miyaa', 'xaraf', 'waxbo', 'qaamuus']

            is_known_class = type_info and type_info[1] == 'class_definition'

            if not is_primitive and not is_known_class:

                 raise SemanticError(ERR_UNKNOWN_TYPE(node.var_type), node.filename, node.line)

        if node.value:
            value_type = self.get_expression_type(node.value)
            
            # Also validate function calls (e.g., check for missing required args)
            if isinstance(node.value, FunctionCallNode):
                self.check(node.value)

            if not self._are_types_compatible(node.var_type, value_type):

                 raise SemanticError(ERR_ASSIGNMENT_TYPE_MISMATCH_SIMPLE(str(node.var_type), str(value_type)), node.filename, node.line)

        self.symbol_table.set(node.var_name, node.var_type, value=node.value)



    def check_AssignmentNode(self, node: AssignmentNode):

        assign_target_node = node.identifier

        if not isinstance(assign_target_node, (IdentifierNode, MemberAccessNode, ArrayAccessNode)):

            raise SemanticError(ERR_ASSIGNMENT_NON_LVALUE(), node.filename, node.line)

        declared_type = self.get_expression_type(assign_target_node)

        value_type = self.get_expression_type(node.expression)

        if not self._are_types_compatible(declared_type, value_type):

            raise SemanticError(ERR_ASSIGNMENT_TYPE_MISMATCH_SIMPLE(str(declared_type), str(value_type)), node.filename, node.line)

        self.check(assign_target_node)

        self.check(node.expression)



    def check_FunctionNode(self, node: FunctionNode):
        if node.name != 'dhis' and not node.name[0].islower():
            raise SemanticError(ERR_FUNCTION_NAME_NOT_LOWERCASE(node.name), node.filename, node.line)

        is_method = self.current_class is not None

        if is_method:
            if self.symbol_table.exists_in_current_scope(node.name):
                raise SemanticError(ERR_FUNCTION_REDEFINED(node.name, is_method=True), node.filename, node.line)
            self.symbol_table.set(node.name, "hawl", value=node, return_type=node.return_type)
        else:
            if self.symbol_table.exists_in_global_scope(node.name):
                raise SemanticError(ERR_FUNCTION_REDEFINED(node.name, is_method=False), node.filename, node.line)
            self.symbol_table.set_global(node.name, "hawl", value=node, return_type=node.return_type)

        previous_function = self.current_function
        self.current_function = node
        self.symbol_table.push_scope()

        if is_method:
            self.symbol_table.set("kan", self.current_class.name)

        has_default = False
        for param in node.params:
            if param.default_value:
                has_default = True
                # Check the type of the default value
                default_value_type = self.get_expression_type(param.default_value)
                if not self._are_types_compatible(param.param_type, default_value_type):
                    raise SemanticError(ERR_DEFAULT_ARG_TYPE_MISMATCH(param.name, param.param_type, default_value_type), node.filename, param.line)
            elif has_default:
                raise SemanticError(ERR_DEFAULT_ARG_ORDER(), node.filename, param.line)

            self.symbol_table.set(param.name, param.param_type)

        self.check(node.body)

        self.symbol_table.pop_scope()
        self.current_function = previous_function





    def check_MethodCallNode(self, node: MethodCallNode):
        self.check(node.object_node)
        object_type = self.get_expression_type(node.object_node)
        if isinstance(object_type, ArrayTypeNode):
            self.get_expression_type(node)
            return
        
        # Handle string methods
        if str(object_type) == 'eray':
            valid_string_methods = ['XarafWeyn', 'XarafYar', 'kaReeb', 'Bkareeb', 'Mkareeb', 'kuBadal', 'sooRaadi', 'lagaHelay', 'qaybi']
            if node.method_name not in valid_string_methods:
                raise SemanticError(ERR_METHOD_NOT_FOUND_ON_STRING(node.method_name), node.filename, node.line)
            return
        
        class_info = self.symbol_table.get(str(object_type))
        if not class_info or class_info[1] != 'class_definition':
            raise SemanticError(ERR_CANNOT_CALL_ON_OBJECT(node.method_name, object_type), node.filename, node.line)

        class_node = class_info[0]
        
        # Look for method in class or parents
        method = None
        current_class = class_node
        method_source_class = None
        while current_class:
            method = next((m for m in current_class.methods if m.name == node.method_name), None)
            if method: 
                method_source_class = current_class
                break
            
            # Use parent_class AST node if linked, else fail
            if getattr(current_class, 'parent_class', None):
                current_class = current_class.parent_class
            else:
                current_class = None

        if not method:
            raise SemanticError(ERR_MEMBER_NOT_FOUND(object_type, node.method_name), node.filename, node.line)

        node.method_source_class = method_source_class

        # Resolve arguments against method parameters
        node.args_list = self._resolve_call_arguments(node.args_list, method.params, node, context=f"method '{node.method_name}'")

        # Type check arguments
        for i, arg_node in enumerate(node.args_list):
            
            arg_type = self.get_expression_type(arg_node)
            param_def = method.params[i]
            if isinstance(param_def, ParameterNode):
                 param_type = param_def.param_type
            else:
                 param_type = param_def[1]
                 
            if not self._are_types_compatible(param_type, arg_type):
                raise SemanticError(ERR_METHOD_ARG_TYPE_MISMATCH(node.args_list[i], node.method_name, param_type, arg_type), node.filename, node.line)
        self.check(node.args_list)



    def check_ReturnStatementNode(self, node: ReturnStatementNode):

        if not self.current_function:

            raise SemanticError(ERR_RETURN_OUTSIDE_FUNCTION(), node.filename, node.line)

        if node.expression:

            return_type = self.get_expression_type(node.expression)

            expected_type = self.current_function.return_type

            if not self._are_types_compatible(expected_type, return_type):

                raise SemanticError(ERR_RETURN_TYPE_MISMATCH(expected_type, return_type), node.filename, node.line)



    def check_IdentifierNode(self, node: IdentifierNode):
        if not self.symbol_table.get(node.name):
            raise SemanticError(ERR_IDENTIFIER_NOT_FOUND(node.name), node.filename, node.line)



    def check_MemberAccessNode(self, node: MemberAccessNode):

        self.check(node.object_node)



    def check_ThisNode(self, node: ThisNode):

        pass



    def check_IfNode(self, node: IfNode):

        self.generic_check(node)



    def check_BinaryOpNode(self, node: BinaryOpNode):

        self.generic_check(node)



    def check_TernaryOpNode(self, node: TernaryOpNode):

        self.generic_check(node)



    def check_QorNode(self, node: QorNode):
        for expr in node.expressions:
            self.check(expr)
            expr_type = self.get_expression_type(expr)
            
            # If the type is a class name (not a primitive)
            if isinstance(expr_type, str):
                type_info = self.symbol_table.get(expr_type)
                if type_info and type_info[1] == 'class_definition':
                    raise SemanticError(ERR_CANNOT_PRINT_TYPE(expr_type), node.filename, node.line)



    def check_HelNode(self, node: HelNode):

        self.generic_check(node)



    def check_FStringNode(self, node: FStringNode):
        for part_type, part_value in node.parts:
            if part_type == "expr" and isinstance(part_value, ASTNode):
                self.check(part_value)



    def check_FunctionCallNode(self, node: FunctionCallNode):
        func_info = self.symbol_table.get(node.name)
        is_builtin = node.name in functions_

        if not func_info and not is_builtin:
            raise SemanticError(ERR_FUNCTION_NOT_FOUND(node.name), node.filename, node.line)

        if is_builtin:
            # Handle built-in functions separately if they have different calling conventions
            # For now, assume they are handled by the transpiler
            for arg in node.params:
                if isinstance(arg, NamedArgument):
                    raise SemanticError(ERR_BUILTIN_NAMED_ARG(node.name), arg.filename, arg.line)
            self.generic_check(node)
            return
        else:
            func_node = func_info[0]
            func_type = func_info[1]

            if isinstance(func_type, FunctionTypeNode):
                expected_params = func_type.param_types or []
                for arg in node.params:
                    if isinstance(arg, NamedArgument):
                        raise SemanticError(ERR_FUNCTION_VAR_NAMED_ARGS(), arg.filename, arg.line)
                if len(node.params) != len(expected_params):
                    raise SemanticError(ERR_ARG_COUNT_MISMATCH(node.name, len(expected_params), len(node.params)), node.filename, node.line)
                for i, (arg_node, expected_type) in enumerate(zip(node.params, expected_params)):
                    arg_type = self.get_expression_type(arg_node)
                    if not self._are_types_compatible(expected_type, arg_type):
                        raise SemanticError(ERR_ARG_TYPE_MISMATCH_SIMPLE(i+1, node.name, expected_type, arg_type), arg_node.filename, arg_node.line)
                self.generic_check(node)
                return

            # Normal user-defined function
            ordered_args = self._resolve_call_arguments(node.params, func_node.params, node, context=f"{node.name}")

            for i, arg_node in enumerate(ordered_args):
                arg_type = self.get_expression_type(arg_node)
                param_type = func_node.params[i].param_type
                if not self._are_types_compatible(param_type, arg_type):
                    raise SemanticError(ERR_ARG_TYPE_MISMATCH_SIMPLE(i+1, node.name, param_type, arg_type), getattr(arg_node, 'filename', node.filename), getattr(arg_node, 'line', node.line))

        self.generic_check(node)



    def check_ArrayAccessNode(self, node: ArrayAccessNode):

        self.generic_check(node)


    def check_ArrayTypeQueryNode(self, node: ArrayTypeQueryNode):
        """
        Validate nooc(arr[]) - check that arr is actually an array
        """
        var_info = self.symbol_table.get(node.identifier)
        
        if not var_info:
            raise SemanticError(ERR_UNDEFINED_VARIABLE(node.identifier), node.filename, node.line)
        
        if not isinstance(var_info[1], (ArrayTypeNode, str)) or (isinstance(var_info[1], str) and "tix" not in var_info[1]):
            if not isinstance(var_info[1], ArrayTypeNode):
                raise SemanticError(ERR_NOT_AN_ARRAY(node.identifier, var_info[1]), node.filename, node.line)



    def check_ArrayAssignmentNode(self, node: ArrayAssignmentNode):

        self.generic_check(node)



    def check_DictionaryInitializationNode(self, node: DictionaryInitializationNode):

        for key, value in node.pairs:

            key_type = self.get_expression_type(key)

            if str(key_type) != 'eray':

                raise SemanticError(ERR_DICT_KEY_NOT_STRING(key_type), key.filename, key.line)

            self.check(value)



    def check_DictionaryAccessNode(self, node: DictionaryAccessNode):
        self.check(node.dictionary_node)
        dict_type = self.get_expression_type(node.dictionary_node)
        
        if str(dict_type) != 'qaamuus':
            raise SemanticError(ERR_DICT_ACCESS_NON_DICT(dict_type), node.filename, node.line)
        key_type = self.get_expression_type(node.key_node)

        if str(key_type) != 'eray':
            raise SemanticError(ERR_DICT_KEY_NOT_STRING(key_type), node.key_node.filename, node.key_node.line)



    def check_DictionaryAssignmentNode(self, node: DictionaryAssignmentNode):
        self.check(node.dictionary_access_node)
        self.check(node.value_node)



    def check_WhileNode(self, node: WhileNode):
        self.check(node.condition)
        self.loop_depth += 1
        self.check(node.body)
        self.loop_depth -= 1


    def check_DoWhileNode(self, node: DoWhileNode):
        self.loop_depth += 1
        self.check(node.body)
        self.loop_depth -= 1
        self.check(node.condition)



    def check_ForRangeNode(self, node: ForRangeNode):
        self.check(node.start_expr)
        self.check(node.end_expr)
        start_type = self.get_expression_type(node.start_expr)
        end_type = self.get_expression_type(node.end_expr)

        if str(start_type) != 'tiro' or str(end_type) != 'tiro':
            raise SemanticError(ERR_FOR_RANGE_NOT_INT(start_type, end_type), node.filename, node.line)

        self.symbol_table.push_scope()
        self.symbol_table.set(node.iterator_var_name, 'tiro')
        self.loop_depth += 1
        self.check(node.body)
        self.loop_depth -= 1
        self.symbol_table.pop_scope()

    def check_BreakNode(self, node: BreakNode):
        if self.loop_depth == 0:
            raise SemanticError(ERR_BREAK_OUTSIDE_LOOP(), node.filename, node.line)

    def check_ContinueNode(self, node: ContinueNode):
        if self.loop_depth == 0:
            raise SemanticError(ERR_CONTINUE_OUTSIDE_LOOP(), node.filename, node.line)



    def check_ForEachNode(self, node: ForEachNode):
        self.check(node.array_expr)
        iterable_type = self.get_expression_type(node.array_expr)

        element_type = None
        if isinstance(iterable_type, ArrayTypeNode):
            element_type = iterable_type.element_type or "dynamic_value"
        elif str(iterable_type) == 'eray':
            element_type = 'xaraf'
        else:
            raise SemanticError(ERR_FOR_EACH_NOT_ITERABLE(iterable_type), node.filename, node.line)

        self.symbol_table.push_scope()
        self.symbol_table.set(node.iterator_var_name, element_type)
        self.loop_depth += 1
        self.check(node.body)
        self.loop_depth -= 1
        self.symbol_table.pop_scope()



    def check_NumberNode(self, node: NumberNode):
        pass

    def check_FloatNode(self, node: FloatNode):
        pass


    def check_StringNode(self, node: StringNode):
        pass


    def check_CharNode(self, node: CharNode):
        pass

    def check_BooleanNode(self, node: BooleanNode):
        pass
