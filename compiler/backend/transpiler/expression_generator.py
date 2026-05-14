# expression_generator.py (Corrected and Final)

from compiler.frontend.parser.ast_nodes import (
    TernaryOpNode, StringNode, NumberNode, FloatNode,
    CharNode, IdentifierNode, BinaryOpNode, FStringNode, BooleanNode,
    FunctionCallNode, ArrayAccessNode, ArrayTypeNode, MethodCallNode,
    ClassInstantiationNode, MemberAccessNode, ThisNode, WaalidNode, ArrayInitializationNode, ArrayTypeQueryNode,
    ASTNode, CCallNode, DictionaryInitializationNode, DictionaryAccessNode, FunctionTypeNode, NamedArgument, TypeLiteralNode, WaxboNode,
    QaabQiimeNode, LambdaNode, FunctionNode, ReturnStatementNode
)

from compiler.backend.transpiler.expression_errors import *
from compiler.midend.built_in_fn import functions_ as built_in_functions
class ExpressionGenerator:
    def __init__(self, main_generator):
        self.main_generator = main_generator
        self.symbol_table = main_generator.symbol_table

    def get_expression_type(self, node):
        if isinstance(node, WaalidNode):
             if self.main_generator.current_class and self.main_generator.current_class.parent_name:
                 return self.main_generator.current_class.parent_name
             return None
        return self.main_generator.semantic_checker.get_expression_type(node, skip_context_check=True)

    def generate_expression(self, node):
        if not isinstance(node, ASTNode):
            raise Cilad(ERR_NOT_AST_NODE(type(node).__name__))

        if isinstance(node, NumberNode):
            return str(node.value)
        elif isinstance(node, FloatNode):
            return str(node.value)
        elif isinstance(node, StringNode):
            return self._escape_c_string_literal(node.value)
        elif isinstance(node, CharNode):
            return f"'{node.value}'"
        elif isinstance(node, BooleanNode):
            return "true" if node.value else "false"
        elif isinstance(node, IdentifierNode):
            return self.main_generator.mangle_name(node.name)
        elif isinstance(node, WaxboNode):
            return "NULL"
        elif isinstance(node, CCallNode):
            args = [self.generate_expression(arg) for arg in node.args]
            return f"{node.c_function_name}({', '.join(args)})"
        elif isinstance(node, ThisNode):
            return "kan"
        elif isinstance(node, WaalidNode):
            # 'waalid' refers to the parent struct embedded in 'kan' (this).
            # We return its address to treat it as a pointer to the parent class.
            return "&kan->parent"
        elif isinstance(node, BinaryOpNode):
            return self._generate_binary_op(node)
        elif isinstance(node, TernaryOpNode):
            return self._generate_ternary_op(node)
        elif isinstance(node, FStringNode):
            return self._generate_fstring(node)
        elif isinstance(node, ArrayInitializationNode):
            return self._generate_array_initialization(node)
        elif isinstance(node, DictionaryInitializationNode):
            self.main_generator.used_features.add("dictionary")
            return self.main_generator.dictionary_generator.generate_initialization(node)

        elif isinstance(node, LambdaNode):
            return self._generate_lambda(node)

        elif isinstance(node, DictionaryAccessNode):
            self.main_generator.used_features.add("dictionary")
            return self.main_generator.dictionary_generator.generate_access(node)

        elif isinstance(node, QaabQiimeNode):
            vals_c = [self.generate_expression(v) for v in node.values]
            return f"({node.struct_name}){{ {', '.join(vals_c)} }}"

        # Consolidated Access Logic for [...] syntax
        elif isinstance(node, ArrayAccessNode):
            base_type = self.get_expression_type(node.array_name_node)
            base_expr_c = self.generate_expression(node.array_name_node)
            index_c = self.generate_expression(node.index_expression)
            index_type = self.get_expression_type(node.index_expression)

            # Case 1: It's a direct dictionary variable. Generate a get() call.
            if str(base_type) == 'qaamuus':
                self.main_generator.used_features.add("dictionary")
                # Wrap dictionary variable in null check
                safe_base = f"TUSMO_SAFE_ACCESS({base_expr_c}, \"{node.filename}\", {node.line})"
                return f"tusmo_qaamuus_get({safe_base}, {index_c})"

            # Case 2: It's a value from a mixed array. Use tusmo_tix_mixed_get_nested for proper type-switching.
            elif str(base_type) == 'walbo':
                temp_var = self.main_generator.get_temp_var()
                # Evaluate once so we can branch based on runtime type
                self.main_generator.c_code += f"    TusmoValue {temp_var} = {base_expr_c};\n"
                
                if str(index_type) == 'eray':
                    self.main_generator.used_features.add("dictionary")
                    return f"tusmo_qaamuus_get({temp_var}.value.as_qaamuus, {index_c})"
                else:
                    self.main_generator.used_features.add("array")
                    # Use tusmo_tix_mixed_get_nested which handles type-switching for typed nested arrays
                    return f"tusmo_tix_mixed_get_nested({temp_var}, {index_c})"

            # Case 3: It's a string. Generate C string indexing.
            elif str(base_type) == 'eray':
                return f"{base_expr_c}[{index_c}]"

            # Case 4: It's a standard, typed Tusmo array.
            else:
                return self.main_generator.array_generator.generate_access(node)

        elif isinstance(node, ClassInstantiationNode):
            return self._generate_class_instantiation(node)
        elif isinstance(node, MemberAccessNode):
            object_c = self.generate_expression(node.object_node)
            object_type = self.get_expression_type(node.object_node)

            # NEW: Handle walbo (dictionary from mixed array)
            if str(object_type) == "walbo":
                # Check if it's coming from an array access (tix:qaamuus element)
                if isinstance(node.object_node, ArrayAccessNode):
                    self.main_generator.used_features.add("dictionary")
                    key_c = f'"{node.member_name}"'
                    return f"tusmo_qaamuus_get({object_c}.value.as_qaamuus, {key_c})"
           
            # Resolve inheritance depth
            class_info = self.symbol_table.get(str(object_type))
            depth = 0
            if class_info and class_info[1] == 'class_definition':
                current_class = class_info[0]
                while current_class:
                    if any(m.var_name == node.member_name for m in current_class.members):
                        break
                    if getattr(current_class, 'parent_class', None):
                        current_class = current_class.parent_class
                        depth += 1
                    else:
                        break
            
            # Build access string
            if class_info and class_info[1] == 'struct_definition':
                # Structs are passed by value, so use dot operator directly
                return f"{object_c}.{node.member_name}"
                
            if depth == 0:
                # Original access: {object_c}->{node.member_name}
                # Wrapped: TUSMO_SAFE_ACCESS({object_c}, \"{node.filename}\", {node.line})->{node.member_name}
                return f"TUSMO_SAFE_ACCESS({object_c}, \"{node.filename}\", {node.line})->{node.member_name}"
            else:
                parents = ".parent" * depth
                # Wrapped: TUSMO_SAFE_ACCESS({object_c}, \"{node.filename}\", {node.line})->{parents[1:]}.{node.member_name}
                return f"TUSMO_SAFE_ACCESS({object_c}, \"{node.filename}\", {node.line})->{parents[1:]}.{node.member_name}"
                 
        elif isinstance(node, MethodCallNode):
            return self._generate_method_call(node)
        elif isinstance(node, FunctionCallNode):
            return self._generate_function_call(node)
        elif isinstance(node, CCallNode):
            return self._generate_ccall(node)
        elif isinstance(node, TypeLiteralNode):
            return f'"{node.type_name}"'
        else:
            raise Cilad(ERR_NO_GEN_LOGIC(type(node).__name__))

    def _generate_array_initialization(self, node: ArrayInitializationNode):
        array_type = self.get_expression_type(node)
        return self.main_generator.array_generator._generate_recursive_initializer(array_type, node.elements)

    def _generate_class_instantiation(self, node: ClassInstantiationNode):
        creator_func = f"_create_{node.class_name}"
        args = self._unwrap_args(getattr(node, "ordered_args", None), node.constructor_args)
        arg_exprs = [self.generate_expression(arg) for arg in args]
        return f"{creator_func}({', '.join(arg_exprs)})"

    def _generate_method_call(self, node: MethodCallNode):
        object_type = self.get_expression_type(node.object_node)
        if isinstance(object_type, ArrayTypeNode) or str(object_type).startswith('tix'):
            return self.main_generator.array_generator.generate_method_call(node)
        
        if str(object_type) == 'qaamuus':
            self.main_generator.used_features.add("dictionary")
            object_c = self.generate_expression(node.object_node)
            args = self._unwrap_args(getattr(node, "ordered_args", None), node.args_list)
            
            if node.method_name == 'kasaar':
                key_c = self.generate_expression(args[0])
                safe_object = f"TUSMO_SAFE_ACCESS({object_c}, \"{node.filename}\", {node.line})"
                return f"tusmo_qaamuus_delete({safe_object}, {key_c})"
            
            if node.method_name == 'majiraa':
                key_c = self.generate_expression(args[0])
                safe_object = f"TUSMO_SAFE_ACCESS({object_c}, \"{node.filename}\", {node.line})"
                return f"tusmo_qaamuus_has_key({safe_object}, {key_c})"
        
        # Handle string methods
        if str(object_type) == 'eray':
            self.main_generator.used_features.add("string")
            object_c = self.generate_expression(node.object_node)
            args = self._unwrap_args(getattr(node, "ordered_args", None), node.args_list)
            safe_object = f"TUSMO_SAFE_ACCESS({object_c}, \"{node.filename}\", {node.line})"
            
            # XarafWeyn() - uppercase
            if node.method_name == 'XarafWeyn':
                return f"tusmo_str_upper({safe_object})"
            
            # XarafYar() - lowercase
            if node.method_name == 'XarafYar':
                return f"tusmo_str_lower({safe_object})"
            
            # kaReeb() - trim
            if node.method_name == 'kaReeb':
                return f"tusmo_str_trim({safe_object})"
            
            # Bkareeb() - left trim (trim start)
            if node.method_name == 'Bkareeb':
                return f"tusmo_str_ltrim({safe_object})"
            
            # Mkareeb() - right trim (trim end)
            if node.method_name == 'Mkareeb':
                return f"tusmo_str_rtrim({safe_object})"
            
            # kuBadal(old, new) - replace
            if node.method_name == 'kuBadal':
                if len(args) != 2:
                    raise Cilad("kuBadal() waxay u baahan tahay 2 qayb (qadim, cusub)")
                old_c = self.generate_expression(args[0])
                new_c = self.generate_expression(args[1])
                return f"tusmo_str_replace({safe_object}, {old_c}, {new_c})"
            
            # sooRaadi(substr) - find index
            if node.method_name == 'sooRaadi':
                if len(args) != 1:
                    raise Cilad("sooRaadi() waxay u baahan tahay 1 qayb")
                substr_c = self.generate_expression(args[0])
                return f"tusmo_str_find({safe_object}, {substr_c})"
            
            # lagaHelay(substr) - contains check
            if node.method_name == 'lagaHelay':
                if len(args) != 1:
                    raise Cilad("lagaHelay() waxay u baahan tahay 1 qayb")
                substr_c = self.generate_expression(args[0])
                return f"tusmo_str_contains({safe_object}, {substr_c})"
            
            # qaybi(delimiter) - split
            if node.method_name == 'qaybi':
                self.main_generator.used_features.add("array")  # qaybi returns tix:eray
                if len(args) != 1:
                    raise Cilad("qaybi() needs 1 argument (delimiter)")
                delim_c = self.generate_expression(args[0])
                return f"tusmo_str_split({safe_object}, {delim_c})"
            
            # Unknown string method - raise error
            raise Cilad(f"Hawsha '{node.method_name}' ma ahan mid jirta oo ku shuban eray (string). Hawlgalaha erayga waa: XarafWeyn, XarafYar, kaReeb, Bkareeb, Mkareeb, kuBadal, sooRaadi, lagaHelay, qaybi")
        
        # Guard against NULL objects before method call
        # object_c = self.generate_expression(node.object_node)
        # However, for regular methods, we wrap cast_object_c which is used as 'kan'
        object_c = self.generate_expression(node.object_node)
        
        # Use recorded source class for name mangling
        source_class = getattr(node, 'method_source_class', None)
        if source_class:
            class_name = source_class.name
        else:
            class_name = str(object_type)
            
        mangled_name = f"{class_name}_{node.method_name}"
        
        # If the method is inherited, we need to cast 'kan' (object_c) to the parent type.
        # However, in our C implementation, we use &child->parent for waalid access.
        # For an inherited call b.s(), we want A_s(&b->parent).
        # We need to find the depth of inheritance.
        
        cast_object_c = object_c
        if source_class and source_class.name != str(object_type):
            # Calculate depth from child to source parent
            child_info = self.symbol_table.get(str(object_type))
            if child_info and child_info[1] == 'class_definition':
                current = child_info[0]
                depth = 0
                while current and current.name != source_class.name:
                    current = getattr(current, 'parent_class', None)
                    depth += 1
                
                if depth > 0:
                    parents = ".parent" * depth
                    # object_c is pointer, so ->parent gives the first parent struct.
                    # We need the ADDRESS of that parent struct to pass as the new 'kan' (pointer).
                    cast_object_c = f"&({object_c}->{parents[1:]})"

        args = self._unwrap_args(getattr(node, "ordered_args", None), node.args_list)
        # Wrap the 'kan' (first argument) in a null check
        safe_kan = f"TUSMO_SAFE_ACCESS({cast_object_c}, \"{node.filename}\", {node.line})"
        arg_exprs = [safe_kan] + [self.generate_expression(arg) for arg in args]
        return f"{mangled_name}({', '.join(arg_exprs)})"

    def _generate_binary_op(self, node):
        left_c = self.generate_expression(node.left)
        right_c = self.generate_expression(node.right)
        left_type = self.get_expression_type(node.left)
        right_type = self.get_expression_type(node.right)
        if node.op == '+' and ('eray' in (str(left_type), str(right_type))):
            self.main_generator.used_features.add("string")
            left_c_converted = self._ensure_string_operand(left_c, left_type)
            right_c_converted = self._ensure_string_operand(right_c, right_type)
            return f"tusmo_concat_cstr({left_c_converted}, {right_c_converted})"
        if node.op in ('==', '!=') and ('eray' in (str(left_type), str(right_type))):
            self.main_generator.used_features.add("string")
            cmp = f"strcmp({left_c}, {right_c})"
            if node.op == '==':
                return f"({cmp} == 0)"
            else:
                return f"({cmp} != 0)"
        op_map = {'+': '+', '-': '-', '*': '*', '/': '/', '%': '%',
                  'iyo': '&&', 'ama': '||', '==': '==', '!=': '!=',
                  '>': '>', '<': '<', '>=': '>=', '<=': '<=', '+=': '+=', '-=': '-=', '*=': '*=', '/=': '/=',
                  'ahayn': '!', '!': '!'}  # Logical NOT
        
        # Handle Type Comparison (e.g., n == tiro)
        if node.op in ('==', '!='):
            lt_str = str(left_type)
            rt_str = str(right_type)
            
            if lt_str.startswith("nooc:") or rt_str.startswith("nooc:"):
                # One of them is a type literal
                if lt_str.startswith("nooc:"):
                    type_name = lt_str[5:]
                    other_c = right_c
                    other_type = rt_str
                else:
                    type_name = rt_str[5:]
                    other_c = left_c
                    other_type = lt_str
                
                is_equal = node.op == '=='
                
                # Case 1: Other side is a dynamic value
                if other_type == "walbo":
                    self.main_generator.used_features.add("conversion")
                    self.main_generator.used_features.add("string")
                    res = f'(strcmp(tusmo_type_of({other_c}), "{type_name}") == 0)'
                    return res if is_equal else f"(!{res})"
                
                # Case 2: Other side is already a string (e.g. nooc(x) == tiro)
                elif other_type == "eray":
                    self.main_generator.used_features.add("string")
                    res = f'(strcmp({other_c}, "{type_name}") == 0)'
                    return res if is_equal else f"(!{res})"
                
                # Case 3: Other side is another type literal
                elif other_type.startswith("nooc:"):
                    other_type_name = other_type[5:]
                    res = "true" if type_name == other_type_name else "false"
                    return res if is_equal else ("false" if res == "true" else "true")
                
                # Case 4: Static type resolve
                else:
                    res = "true" if type_name == other_type else "false"
                    return res if is_equal else ("false" if res == "true" else "true")

        c_op = op_map.get(node.op)
        if c_op:
            if node.op == '/':
                return f"TUSMO_SAFE_DIV({left_c}, {right_c}, \"{node.filename}\", {node.line})"
            if node.op == '%':
                return f"TUSMO_SAFE_MOD({left_c}, {right_c}, \"{node.filename}\", {node.line})"
            # Handle unary NOT (ahayn and !) - only use right operand
            if node.op == 'ahayn' or node.op == '!':
                return f"(!{right_c})"
            return f"({left_c} {c_op} {right_c})"
        else:
            raise Cilad(ERR_UNKNOWN_OP(node.op))

    def _generate_ternary_op(self, node):
        condition_c = self.generate_expression(node.condition)
        if_true_c = self.generate_expression(node.if_true)
        if_false_c = self.generate_expression(node.if_false)
        return f"({condition_c} ? {if_true_c} : {if_false_c})"

    def _escape_c_string_literal(self, s):
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        s = s.replace('\n', '\\n')
        s = s.replace('\r', '\\r')
        s = s.replace('\t', '\\t')
        return f'"{s}"'

    def _generate_lambda(self, node):
        """Generates a global C function for an anonymous function and returns its name."""
        self.main_generator.lambda_counter += 1
        lambda_name = f"__tusmo_lambda_{self.main_generator.lambda_counter}"
        node.generated_name = lambda_name

        # Prepare the body
        if node.is_concise:
            # For concise lambdas: hawl(x) => x + 1
            # We wrap the expression in a return statement
            body = [ReturnStatementNode(node.body, line=node.line, filename=node.filename)]
        else:
            # For block lambdas: hawl(x) { qor(x); soo_celi x + 1 }
            body = node.body

        # Create a temporary FunctionNode to leverage existing function generation logic
        temp_func_node = FunctionNode(
            return_type=node.return_type,
            name=lambda_name,
            params=node.params,
            body=body,
            line=node.line,
            filename=node.filename
        )
        # Copy metadata needed for cleanup
        if hasattr(node, 'cleanup_vars'):
            temp_func_node.cleanup_vars = node.cleanup_vars

        # Generate the C function definition
        self.main_generator.function_generator.generate(temp_func_node)

        # Return the function name (which acts as a function pointer in C)
        return lambda_name

    def _generate_fstring(self, node: FStringNode):
        self.main_generator.used_features.add("string")
        segments = []
        for part_type, part_value in node.parts:
            if part_type == "text":
                if part_value:
                    segments.append(self._escape_c_string_literal(part_value))
            elif part_type == "expr":
                expr_node = part_value if isinstance(part_value, ASTNode) else StringNode(str(part_value), line=node.line, filename=node.filename)
                expr_code = self.generate_expression(expr_node)
                expr_type = self.get_expression_type(expr_node)
                segments.append(self._ensure_string_operand(expr_code, expr_type))
        if not segments:
            return '""'
        result = segments[0]
        for segment in segments[1:]:
            result = f"tusmo_concat_cstr({result}, {segment})"
        return result

    def _generate_ccall(self, node):
        '''Registering c call fn'''
        c_function_name = node.c_function_name
        if c_function_name in ["tusmo_init_random", "tusmo_random_int", "tusmo_random_double"]:
            self.main_generator.used_features.add("nasiib")
        
        elif "tusmo_time" in c_function_name or "tusmo_get" in c_function_name:
            self.main_generator.used_features.add("wakhti")
        
        elif "tusmo_os" in c_function_name:
            self.main_generator.used_features.add("os")
            if c_function_name == "tusmo_os_list_dir":
                self.main_generator.used_features.add("array")
        elif "tusmo_http" in c_function_name:
            self.main_generator.used_features.add("http")
            if c_function_name == "tusmo_http_server_accept":
                self.main_generator.used_features.add("dictionary")
            if c_function_name == "tusmo_http_qaamuus_to_json":
                self.main_generator.used_features.add("dictionary")
        elif "tusmo_socket" in c_function_name:
            self.main_generator.used_features.add("socket")
        elif "tusmo_ws" in c_function_name:
            self.main_generator.used_features.add("websocket")
            self.main_generator.used_features.add("socket")  # WebSocket needs socket
            self.main_generator.used_features.add("dictionary")  # For decode_frame result
        elif "tusmo_gl" in c_function_name:
            self.main_generator.used_features.add("opengl")
        elif c_function_name in ["tusmo_sin", "tusmo_cos", "tusmo_sqrt", "tusmo_abs_d", 
                                  "tusmo_pow", "tusmo_floor", "tusmo_ceil", "tusmo_round"]:
            self.main_generator.used_features.add("math")
        c_args = [self.generate_expression(arg) for arg in node.args]

        return f'{c_function_name}({", ".join(c_args)})'

    def _ensure_string_operand(self, expr_code, expr_type):
        
        expr_type_str = str(expr_type)
       

        if expr_type_str in ('eray', 'c_dynamic', 'unknown'):
            return expr_code
        if expr_type_str == 'xaraf':
            self.main_generator.used_features.add("string")
            return f'tusmo_str_format("%c", {expr_code})'
        if expr_type_str == 'tiro':
            self.main_generator.used_features.add("string")
            return f'tusmo_str_format("%d", {expr_code})'
        if expr_type_str == 'jajab':
            self.main_generator.used_features.add("string")
            return f'tusmo_str_format("%f", {expr_code})'
        if expr_type_str == 'miyaa':
            return f"(({expr_code}) ? \"run\" : \"been\")"
        if expr_type_str == 'walbo':
            self.main_generator.used_features.add("conversion")
            self.main_generator.used_features.add("string")
            return f"tusmo_to_eray({expr_code})"
        
        raise Cilad(ERR_FSTRING_TYPE())

    def _generate_function_call(self, node: FunctionCallNode):
        # Handle Type Casting Functions
        if node.name in ["eray", "tiro", "jajab", "miyaa"]:
            self.main_generator.used_features.add("conversion")
            args = self._unwrap_args(getattr(node, "ordered_args", None), node.params)
            if len(args) != 1:
                raise Cilad(ERR_CAST_ARG_COUNT(node.name, len(args)))
            
            arg_node = args[0]
            arg_c = self.generate_expression(arg_node)
            arg_type = self.get_expression_type(arg_node)

            # If the argument is already a TusmoValue (dynamic array element), pass it straight through.
            if str(arg_type) == "walbo":
                c_func_name = f"tusmo_to_{node.name}"
                return f"{c_func_name}({arg_c})"

            # Create a TusmoValue struct on the stack
            val_var = self.main_generator.get_temp_var()
            self.main_generator.c_code += f"    TusmoValue {val_var};\n"
            self.main_generator.c_code += f"    {val_var}.type = {self._get_tusmo_type_enum(arg_type)};\n"
            self.main_generator.c_code += f"    {val_var}.value.{self._get_union_member(arg_type)} = {arg_c};\n"

            c_func_name = f"tusmo_to_{node.name}"
            return f"{c_func_name}({val_var})"

        if node.name in built_in_functions:
            feature = built_in_functions[node.name].get("feature")
            if feature:
                self.main_generator.used_features.add(feature)
        if node.name == 'dherer':
            if len(node.params) != 1:
                raise Cilad(ERR_DHERER_ARG_COUNT(len(node.params)))
            arg_expr = self.generate_expression(node.params[0])
            arg_type = self.main_generator.semantic_checker.get_expression_type(node.params[0], skip_context_check=True)
            if str(arg_type) == 'eray':
                return f"strlen({arg_expr})"
            elif isinstance(arg_type, ArrayTypeNode) or str(arg_type).startswith("tix") or str(arg_type) == "walbo":
                return f"{arg_expr}->size"
            else:
                raise Cilad(ERR_DHERER_TYPE(arg_type))
        if node.name == 'nooc':
            if len(node.params) != 1:
                raise Cilad(ERR_NOOC_ARG_COUNT())
            arg_node = node.params[0]
            # Special case: nooc(arr[]) asks for the element type of a tix.
            if isinstance(arg_node, ArrayTypeQueryNode):
                base_type = self.main_generator.semantic_checker.get_expression_type(arg_node, skip_context_check=True)
                if not isinstance(base_type, ArrayTypeNode):
                    raise Cilad(ERR_NOOC_TIX_QUERY())
                self.main_generator.used_features.add("array")
                elem_type = base_type.element_type
                type_str = "tix:dynamic" if elem_type is None else f"tix:{elem_type}"
                return f'"{type_str}"'

            arg_type = self.main_generator.semantic_checker.get_expression_type(arg_node, skip_context_check=True)
            if isinstance(arg_type, ArrayTypeNode):
                self.main_generator.used_features.add("array")
            # If it's a mixed-array element (walbo), ask the runtime for the actual tag.
            if str(arg_type) == "walbo":
                self.main_generator.used_features.add("conversion")
                arg_expr = self.generate_expression(arg_node)
                return f"tusmo_type_of({arg_expr})"
            type_str = str(arg_type)
            return f'"{type_str}"'
        
        # qor_tiro() - convert char to integer (ASCII value)
        if node.name == 'qor_tiro':
            if len(node.params) != 1:
                raise Cilad("qor_tiro() waxay u baahan tahay 1 parameter (xaraf)")
            arg_expr = self.generate_expression(node.params[0])
            return f"(int)({arg_expr})"
        
        # qor_xaraf() - convert integer (ASCII) to char
        if node.name == 'qor_xaraf':
            if len(node.params) != 1:
                raise Cilad("qor_xaraf() waxay u baahan tahay 1 parameter (tiro)")
            arg_expr = self.generate_expression(node.params[0])
            return f"(char)({arg_expr})"
        if node.name == 'tix_cayiman':
            self.main_generator.used_features.add("array")
            raise Cilad(ERR_TIX_CAYIMAN_USAGE())
        
        func_info = self.symbol_table.get(node.name)
        if not func_info:
            # This should have been caught by the semantic analyzer, but as a safeguard:
            raise Cilad(ERR_FUNC_NOT_FOUND(node.name))

        # Check if it's a direct function call or an indirect call through a variable
        if isinstance(func_info[1], FunctionTypeNode):
            # Indirect call through a variable
            c_func_name = self.main_generator.mangle_name(node.name)
            args = self._unwrap_args(getattr(node, "ordered_args", None), node.params)
            arg_exprs = [self.generate_expression(arg) for arg in args]
            return f"{c_func_name}({', '.join(arg_exprs)})"
        else:
            # Direct function call
            func_node = func_info[0]
            if func_node is None:
                # Symbol exists but is not a callable with AST body (e.g. c_type/constant).
                raise Cilad(ERR_FUNC_NOT_FOUND(node.name))
            args = self._unwrap_args(getattr(node, "ordered_args", None), node.params)

            arg_exprs = []
            for i, arg in enumerate(args):
                arg_c = self.generate_expression(arg)
                
                # Check if the parameter expects an 'eray'
                if i < len(func_node.params):
                    param_type = str(func_node.params[i].param_type)
                    if param_type == "eray":
                        # If the argument is not already a safe heap allocation (like a previous strdup or concat), duplicate it.
                        if not arg_c.startswith("tusmo_strdup") and not arg_c.startswith("tusmo_concat_cstr") and not arg_c.startswith("tusmo_to_eray"):
                            self.main_generator.used_features.add("string")
                            arg_c = f"tusmo_strdup({arg_c})"
                            
                arg_exprs.append(arg_c)
            
            num_provided_args = len(arg_exprs)
            num_required_params = len(func_node.params)

            if num_provided_args < num_required_params:
                for i in range(num_provided_args, num_required_params):
                    param = func_node.params[i]
                    if param.default_value:
                        arg_exprs.append(self.generate_expression(param.default_value))
                    else:
                        # This should also be caught by the semantic analyzer
                        raise Cilad(ERR_MISSING_PARAM(param.name))

            c_func_name = self.main_generator.mangle_name(node.name)
            return f"{c_func_name}({', '.join(arg_exprs)})"

    def _get_tusmo_type_enum(self, type_str):
        type_map = {
            "tiro": "TUSMO_TIRO",
            "jajab": "TUSMO_JAJAB",
            "eray": "TUSMO_ERAY",
            "miyaa": "TUSMO_MIYAA",
            "xaraf": "TUSMO_XARAF",
        }
        return type_map.get(str(type_str), "TUSMO_ERAY") # Default to string for unknown

    def _get_union_member(self, type_str):
        member_map = {
            "tiro": "as_tiro",
            "jajab": "as_jajab",
            "eray": "as_eray",
            "miyaa": "as_miyaa",
            "xaraf": "as_xaraf",
        }
        return member_map.get(str(type_str), "as_eray")

    def _unwrap_args(self, ordered, raw_list):
        if ordered is not None:
            return ordered
        result = []
        for a in raw_list:
            if isinstance(a, NamedArgument):
                result.append(a.value)
            else:
                result.append(a)
        return result
