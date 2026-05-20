from compiler.frontend.parser.ast_nodes import ArrayTypeNode, IdentifierNode, StringNode


class ReturnGenerator:
    def __init__(self, main_generator, expr_generator):
        self.main_generator = main_generator
        self.expr_generator = expr_generator

    def _should_clone_array_return(self, expression_node, ret_type_node):
        if not isinstance(expression_node, IdentifierNode):
            return False

        if not isinstance(ret_type_node, ArrayTypeNode):
            return False

        current_function = getattr(self.main_generator, 'current_function_node', None)
        if not current_function:
            return False

        for param in getattr(current_function, 'params', []):
            if param.name == expression_node.name:
                return bool(getattr(param, 'borrowed', False))

        return False

    def _should_duplicate_eray_literal_return(self, expression_node, ret_type_node):
        if str(ret_type_node) != "eray":
            return False

        if isinstance(expression_node, StringNode):
            return True

        if isinstance(expression_node, IdentifierNode):
            symbol_info = self.main_generator.symbol_table.get(expression_node.name)
            if symbol_info and isinstance(symbol_info[0], StringNode):
                return True

        return False

    def generate(self, node):
        # --- NEW: Inject Cleanup for Early Return ---
        cleanup_code = ""
        active_cleanup = getattr(node, 'active_cleanup', [])

        # Identify variable being returned to skip it
        returned_var = None
        if node.expression and hasattr(node.expression, 'name'):
            returned_var = node.expression.name

        for var in active_cleanup:
            name = var['name']
            free_fn = var.get('free_fn', 'free')
            if name == returned_var:
                continue
            cleanup_code += f"    if ({name}) {free_fn}({name});\n"

        expression_node = node.expression
        if expression_node:
            expr_c_code = self.expr_generator.generate_expression(expression_node)
            # To avoid use-after-free when a variable used in the return expression is cleaned up,
            # we evaluate it into a temporary variable first.
            
            # Determine the return type for the temporary variable
            ret_type_node = getattr(self.main_generator, 'current_function_node').return_type if getattr(self.main_generator, 'current_function_node', None) else "waxbo"
            c_ret_type = self.main_generator.get_c_type(ret_type_node)
            
            temp_var = self.main_generator.get_temp_var()

            if self._should_clone_array_return(expression_node, ret_type_node):
                clone_create = self.main_generator.array_generator.get_create_function(ret_type_node)
                clone_extend = self.main_generator.array_generator.get_extend_function(ret_type_node)
                if clone_create and clone_extend:
                    clone_var = self.main_generator.get_temp_var()
                    expr_c_code = f"({expr_c_code})"
                    self.main_generator.c_code += f"    {c_ret_type} {clone_var} = {clone_create}({expr_c_code}->size);\n"
                    self.main_generator.c_code += f"    {clone_extend}({clone_var}, {expr_c_code});\n"
                    expr_c_code = clone_var
            
            if self._should_duplicate_eray_literal_return(expression_node, ret_type_node):
                expr_c_code = f"tusmo_strdup({expr_c_code})"
            
            # Dynamic value unwrapping logic (similar to assignments)
            right_side_type = self.main_generator.semantic_checker.get_expression_type(expression_node, skip_context_check=True)
            if str(right_side_type) == "walbo" and str(ret_type_node) != "walbo" and expression_node.__class__.__name__ != 'CCallNode':
                unwrap_map = {
                    "tiro": "as_tiro",
                    "jajab": "as_jajab",
                    "eray": "as_eray",
                    "miyaa": "as_miyaa",
                    "xaraf": "as_xaraf",
                    "qaamuus": "as_qaamuus",
                    "tix": "as_tix",
                }
                member = unwrap_map.get(str(ret_type_node))
                if member:
                    expr_c_code = f"({expr_c_code}).value.{member}"

            self.main_generator.c_code += f"    {c_ret_type} {temp_var} = {expr_c_code};\n"
            
            # Now run the cleanup code safely
            self.main_generator.c_code += cleanup_code
            
            self.main_generator.c_code += f"    return {temp_var};\n"
        else:
            self.main_generator.c_code += cleanup_code
            self.main_generator.c_code += "    return;\n"
