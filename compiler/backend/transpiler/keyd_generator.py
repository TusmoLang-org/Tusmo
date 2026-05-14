from compiler.frontend.parser.ast_nodes import ArrayTypeNode, FunctionTypeNode

class KeydGenerator:
    def __init__(self, main_generator, expr_generator):
        self.main_generator = main_generator
        self.symbol_table = main_generator.symbol_table
        self.expr_generator = expr_generator

    def generate(self, node):
        """Main method to generate C code for variable declarations."""
        var_name = self.main_generator.mangle_name(node.var_name)
        var_type = node.var_type
        value = node.value
        is_top_level = not self.main_generator.inside_function

        # Add the variable to the symbol table for the current scope
        self.symbol_table.set(var_name, var_type)

        # Handle Function Type (Function Pointers)
        if isinstance(var_type, FunctionTypeNode):
            decl = self.main_generator.get_c_type(var_type, name=var_name)
            self._emit_declaration_raw(decl, is_top_level)
            if value:
                init_c = self.expr_generator.generate_expression(value)
                self.main_generator.c_code += f"    {var_name} = {init_c};\n"
            else:
                self.main_generator.c_code += f"    {var_name} = NULL;\n"
            return

        # Handle qaamuus type
        if str(var_type) == "qaamuus":
            self.main_generator.used_features.add("dictionary")
            c_type = "TusmoQaamuus*"
            self._emit_declaration(c_type, var_name, is_top_level)
            if value:
                init_c = self.expr_generator.generate_expression(value)
                right_type = self.main_generator.semantic_checker.get_expression_type(value, skip_context_check=True)
                if str(right_type) == "walbo":
                    init_c = f"({init_c}).value.as_qaamuus"
                self.main_generator.c_code += f"    {var_name} = {init_c};\n"
                # Move Semantics NULLing
                if value.__class__.__name__ == 'IdentifierNode':
                    ident_c = self.expr_generator.generate_expression(value)
                    self.main_generator.c_code += f"    {ident_c} = NULL;\n"
            else:
                self.main_generator.c_code += f"    {var_name} = tusmo_qaamuus_create();\n"
            return

        # Handle array types
        if isinstance(var_type, ArrayTypeNode):
            c_type = self.main_generator.array_generator.get_c_type_from_tusmo_type(var_type)
            self._emit_declaration(c_type, var_name, is_top_level)
            if value:
                # Check if it's a tix_cayiman function call
                if (hasattr(value, '__class__') and value.__class__.__name__ == 'FunctionCallNode' 
                    and value.name == 'tix_cayiman'):
                    # Validate that the function has at least one parameter
                    if not hasattr(value, 'params') or not value.params or len(value.params) < 1:
                        raise ValueError(f"tix_cayiman requires at least one parameter (size) for variable {var_name}")
                    # Generate the appropriate create function based on the declared type
                    size_expr = self.expr_generator.generate_expression(value.params[0])
                    element_type = var_type.element_type
                    element_type_str = str(element_type)
                    
                    if element_type is None or element_type_str == "None" or element_type_str == "qaamuus":
                        # Mixed/heterogeneous array
                        init_c = f"tusmo_tix_mixed_create({size_expr})"
                    elif isinstance(element_type, ArrayTypeNode):
                        # Multi-dimensional array
                        init_c = f"tusmo_tix_generic_create({size_expr})"
                    else:
                        # Homogeneous array
                        init_c = f"tusmo_hp_tix_{element_type_str}_create({size_expr})"
                    
                    self.main_generator.c_code += f"    {var_name} = {init_c};\n"
                # Check if it's an array initialization
                elif hasattr(value, '__class__') and value.__class__.__name__ == 'ArrayInitializationNode':
                    # Use the declared type instead of inferred type for empty arrays
                    init_c = self.main_generator.array_generator._generate_recursive_initializer(var_type, value.elements)
                    self.main_generator.c_code += f"    {var_name} = {init_c};\n"
                else:
                    # Other initializations
                    init_c = self.expr_generator.generate_expression(value)
                    self.main_generator.c_code += f"    {var_name} = {init_c};\n"
                    # Move Semantics NULLing
                    if value.__class__.__name__ == 'IdentifierNode':
                        self.main_generator.c_code += f"    {init_c} = NULL;\n"
            else:
                # Array without initialization - set to NULL
                self.main_generator.c_code += f"    {var_name} = NULL;\n"
        # Handle class types
        elif isinstance(var_type, str):
            type_info = self.symbol_table.get(var_type)
            is_class = type_info and type_info[1] == 'class_definition'
            
            if is_class:
                # Class type declaration
                c_type = f"{var_type}*"
                self._emit_declaration(c_type, var_name, is_top_level)
                if value:
                    init_c = self.expr_generator.generate_expression(value)
                    self.main_generator.c_code += f"    {var_name} = {init_c};\n"
                    # Move Semantics NULLing
                    if value.__class__.__name__ == 'IdentifierNode':
                        self.main_generator.c_code += f"    {init_c} = NULL;\n"
                else:
                    self.main_generator.c_code += f"    {var_name} = NULL;\n"
            else:
                # Primitive type
                if value:
                    # Declaration with initialization
                    c_primitive_type = self._get_primitive_c_type(var_type)
                    self._emit_declaration(c_primitive_type, var_name, is_top_level)
                    init_c = self.expr_generator.generate_expression(value)
                    
                    # Super intelligent: wrap eray literals in strdup
                    if str(var_type) == "eray" and value.__class__.__name__ == 'StringNode':
                        self.main_generator.used_features.add("string")
                        init_c = f"tusmo_strdup({init_c})"
                        
                    # Unwrap walbo if assigning from dictionaries/mixed arrays
                    right_type = self.main_generator.semantic_checker.get_expression_type(value, skip_context_check=True)
                    if str(right_type) == "walbo" and value.__class__.__name__ != 'CCallNode':
                        unwrap_map = {
                            "tiro": "as_tiro",
                            "jajab": "as_jajab",
                            "eray": "as_eray",
                            "miyaa": "as_miyaa",
                            "xaraf": "as_xaraf",
                            "qaamuus": "as_qaamuus",
                            "tix": "as_tix",
                        }
                        member = unwrap_map.get(str(var_type))
                        if member:
                            init_c = f"({init_c}).value.{member}"
                    self.main_generator.c_code += f"    {var_name} = {init_c};\n"
                    # Move Semantics NULLing
                    if value.__class__.__name__ == 'IdentifierNode' and self.main_generator.semantic_checker.tracker.is_heap_type(var_type):
                        self.main_generator.c_code += f"    {init_c} = NULL;\n"
                else:
                    # Declaration without initialization - use defaults
                    c_primitive_type = self._get_primitive_c_type(var_type)
                    self._emit_declaration(c_primitive_type, var_name, is_top_level)
                    self.generate_default_init(var_name, var_type)

    def _get_primitive_c_type(self, var_type):
        if var_type == "tiro":
            return "int"
        elif var_type == "jajab":
            return "double"
        elif var_type == "xaraf":
            return "char"
        elif var_type == "miyaa":
            return "bool"
        elif var_type == "eray":
            return "char*"
        elif var_type == "waxbo":
            return "void*"
        info = self.symbol_table.get(var_type) if isinstance(var_type, str) else None
        if info:
            if info[1] == "c_type": return var_type
            if info[1] == "struct_definition": return var_type
        return "void*"

    def _emit_declaration(self, c_type, var_name, is_top_level):
        if is_top_level:
            self.main_generator.global_declarations += f"{c_type} {var_name};\n"
        else:
            self.main_generator.c_code += f"    {c_type} {var_name};\n"

    def _emit_declaration_raw(self, decl, is_top_level):
        if is_top_level:
            self.main_generator.global_declarations += f"{decl};\n"
        else:
            self.main_generator.c_code += f"    {decl};\n"

    def generate_default_init(self, var_name, var_type):
        """Generates an assignment to a default value if no initializer was provided."""
        if var_type == "tiro":
            self.main_generator.c_code += f"    {var_name} = 0;\n"
        elif var_type == "jajab":
            self.main_generator.c_code += f"    {var_name} = 0.0;\n"
        elif var_type == "xaraf":
            self.main_generator.c_code += f"    {var_name} = '\\0';\n"
        elif var_type == "miyaa":
            self.main_generator.c_code += f"    {var_name} = false;\n"
        elif var_type == "eray":
            self.main_generator.c_code += f"    {var_name} = NULL;\n"
        elif var_type == "waxbo":
            self.main_generator.c_code += f"    {var_name} = NULL;\n"
