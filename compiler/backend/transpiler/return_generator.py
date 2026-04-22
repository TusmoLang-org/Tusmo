
class ReturnGenerator:
    def __init__(self, main_generator, expr_generator):
        self.main_generator = main_generator
        self.expr_generator = expr_generator

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

        self.main_generator.c_code += cleanup_code

        expression_node = node.expression
        if expression_node:
            expr_c_code = self.expr_generator.generate_expression(expression_node)
            self.main_generator.c_code += f"    return {expr_c_code};\n"
        else:
            self.main_generator.c_code += "    return;\n"