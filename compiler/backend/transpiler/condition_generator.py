
class ConditionGenerator:
    def __init__(self, main_generator, expr_generator):
        self.main_generator = main_generator
        self.expr_generator = expr_generator
        self.symbol_table = main_generator.symbol_table

    def generate(self, node):
        is_first_case = True
        cases_cleanup = getattr(node, 'cases_cleanup', [])
        
        for i, (condition, body) in enumerate(node.cases):
            keyword = "if" if is_first_case else "else if"
            condition_c = self.expr_generator.generate_expression(condition)
            self.main_generator.c_code += f"    {keyword} ({condition_c}) {{\n"
            self.symbol_table.push_scope()
            self.main_generator._generate_node(body)
            
            # --- NEW: Inject Cleanup code ---
            cleanup_vars = cases_cleanup[i] if i < len(cases_cleanup) else []
            for var in cleanup_vars:
                name = var['name']
                free_fn = var.get('free_fn', 'free')
                self.main_generator.c_code += f"        if ({name}) {free_fn}({name});\n"
                
            self.symbol_table.pop_scope()
            self.main_generator.c_code += f"    }}\n"
            is_first_case = False

        if node.else_case:
            self.main_generator.c_code += f"    else {{\n"
            self.symbol_table.push_scope()
            self.main_generator._generate_node(node.else_case)
            
            # --- NEW: Inject Cleanup code ---
            else_cleanup = getattr(node, 'else_cleanup', [])
            for var in else_cleanup:
                name = var['name']
                free_fn = var.get('free_fn', 'free')
                self.main_generator.c_code += f"        if ({name}) {free_fn}({name});\n"
                
            self.symbol_table.pop_scope()
            self.main_generator.c_code += f"    }}\n"