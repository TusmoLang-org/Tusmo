class HelGenerator:
    def __init__(self, main_generator):
        self.main_generator = main_generator
        self.symbol_table = main_generator.symbol_table

    def generate(self, node):
        var_name = node.identifier
        var_info = self.symbol_table.get(var_name)

        if not var_info:
            return

        if node.prompt:
            self.main_generator.c_code += f'    printf("{node.prompt}");\n'

        if var_info[1] == "eray":
            if getattr(node, "needs_cleanup", False):
                self.main_generator.c_code += f'    if ({var_name}) tusmo_free_eray({var_name});\n'
            self.main_generator.c_code += f'    {var_name} = hel_str();\n'

        if var_info[1] == "tiro":
            self.main_generator.c_code += f'    scanf("%d", &{var_name});\n'
            self.main_generator.c_code += f'    {{ int c; while((c = getchar()) != \'\\n\' && c != EOF); }}\n'

        if var_info[1] == "jajab":
            self.main_generator.c_code += f'    scanf("%lf", &{var_name});\n'
            self.main_generator.c_code += f'    {{ int c; while((c = getchar()) != \'\\n\' && c != EOF); }}\n'
