from compiler.frontend.parser.ast_nodes import (
  ArrayTypeNode, 
    ArrayAccessNode, MethodCallNode, ArrayAssignmentNode, NamedArgument
)
from compiler.midend.symbol_table import SymbolTable

class ArrayGenerator:
    def __init__(self, main_generator, expr_generator):
        self.main_generator = main_generator
        self.expr_generator = expr_generator
        self.symbol_table = main_generator.symbol_table

    # Mapping from base element type string to type suffix for nested arrays
    # Used to build type names like TusmoTixTiroNested, TusmoTixTiroNested2
    TYPE_SUFFIX_MAP = {
        'tiro': 'Tiro',
        'jajab': 'Jajab',
        'eray': 'Eray',
        'miyaa': 'Miyaa',
        'xaraf': 'Xaraf',
    }

    def get_c_type_map(self):
        return {'tiro': 'int', 'jajab': 'double', 'eray': 'char*', 'miyaa': 'bool', 'xaraf': 'char', 'waxbo': 'void', 'qaamuus': 'TusmoQaamuus*'}

    def get_tix_struct_name(self, element_type_str):
        # If the element type string is None or 'None', it's a dynamic array.
        if element_type_str is None or element_type_str == 'None':
            return "TusmoTixMixed"
            
        type_map = {'tiro': 'Tiro', 'jajab': 'Jajab', 'eray': 'Eray', 'miyaa': 'Miyaa', 'qaamuus': 'Mixed', 'xaraf': 'Xaraf'}
        return f"TusmoTix{type_map.get(element_type_str)}"

    def get_nested_depth_and_base_type(self, tusmo_type_node, depth=0):
        """
        Calculate the nesting depth and find the base element type.
        Returns (depth, base_type_str) where base_type_str is the innermost type.
        
        Examples:
            tix:tiro -> (1, 'tiro')      # 1D array of int
            tix:tix:tiro -> (2, 'tiro')  # 2D array of int
            tix:tix:tix:tiro -> (3, 'tiro')  # 3D array of int
        """
        if isinstance(tusmo_type_node, ArrayTypeNode):
            element = tusmo_type_node.element_type
            if isinstance(element, ArrayTypeNode):
                return self.get_nested_depth_and_base_type(element, depth + 1)
            else:
                return (depth + 1, str(element))
        else:
            return (1, str(tusmo_type_node))

    def get_c_type_from_tusmo_type(self, tusmo_type_node):
        if not isinstance(tusmo_type_node, ArrayTypeNode):
            return self.get_c_type_map().get(str(tusmo_type_node), "void*")
        
        depth, base_type = self.get_nested_depth_and_base_type(tusmo_type_node)
        
        # For dynamic/mixed arrays (depth 1 but base_type is 'None' or 'qaamuus')
        if depth == 1 and (base_type == 'None' or base_type == 'qaamuus'):
            return "TusmoTixMixed*"
        
        # For typed nested arrays
        if base_type in self.TYPE_SUFFIX_MAP:
            type_suffix = self.TYPE_SUFFIX_MAP[base_type]
            if depth == 1:
                # 1D array
                return f"TusmoTix{type_suffix}*"
            elif depth == 2:
                # 2D array - use nested type
                return f"TusmoTix{type_suffix}Nested*"
            elif depth == 3:
                # 3D array - use nested2 type
                return f"TusmoTix{type_suffix}Nested2*"
            else:
                # depth >= 4: use generic for unlimited dimensions
                return "TusmoTixGeneric*"
        
        # Fallback for unknown types - use generic
        return "TusmoTixGeneric*"

    def _generate_recursive_initializer(self, type_node, element_nodes):
        """
        Generate C code for array initialization.
        Uses typed nested arrays (TusmoTixTiroNested, TusmoTixTiroNested2, etc.)
        so that GC can trace pointers properly.
        """
        self.main_generator.used_features.add("array")
        temp_var = self.main_generator.get_temp_var()
        c_type = self.get_c_type_from_tusmo_type(type_node)
        capacity = len(element_nodes) if element_nodes else 8

        # Check if this is a nested array (element is another ArrayTypeNode)
        if isinstance(type_node.element_type, ArrayTypeNode):
            # Calculate depth and base type for this nested array
            depth, base_type = self.get_nested_depth_and_base_type(type_node)
            
            # Determine which create/append functions to use based on depth
            original_depth = depth  # Track original depth for wrap enum
            if base_type in self.TYPE_SUFFIX_MAP:
                type_suffix = self.TYPE_SUFFIX_MAP[base_type]
                if depth == 1:
                    # 1D array - use typed array functions
                    create_func = f"tusmo_hp_tix_{type_suffix.lower()}_create"
                    append_func = f"tusmo_hp_tix_{type_suffix.lower()}_append"
                elif depth == 2:
                    # 2D array - use nested type functions
                    create_func = f"tusmo_tix_{type_suffix.lower()}_nested_create"
                    append_func = f"tusmo_tix_{type_suffix.lower()}_nested_append"
                elif depth == 3:
                    # 3D array - use nested2 type functions
                    create_func = f"tusmo_tix_{type_suffix.lower()}_nested2_create"
                    append_func = f"tusmo_tix_{type_suffix.lower()}_nested2_append"
                else:
                    # For depth >= 4, limit to 3D - deeper nesting uses TusmoTixMixed
                    original_depth = depth  # Save original for wrap enum
                    depth = 3  # Cap at 3D
                    c_type = "TusmoTixMixed*"
                    create_func = "tusmo_tix_mixed_create"
                    append_func = "tusmo_tix_mixed_append"
            else:
                # Fallback to generic for unknown types
                create_func = "tusmo_tix_generic_create"
                append_func = "tusmo_tix_generic_append"
            
            self.main_generator.c_code += f"    {c_type} {temp_var} = {create_func}({capacity});\n"
            # For typed nested arrays (2D, 3D), we need to wrap in TusmoValue when appending to mixed
            needs_wrap = depth >= 2 and create_func == "tusmo_tix_mixed_create"
            
            # Determine the correct type enum for wrapping based on the ACTUAL depth of the sub-array
            # When storing typed arrays in TusmoValue, we need to use the correct enum:
            # - 1D sub-array -> TUSMO_TIX_XXX (e.g., TUSMO_TIX_TIRO)
            # - 2D sub-array -> TUSMO_TIX_XXX_NESTED (e.g., TUSMO_TIX_TIRO_NESTED)
            # - 3D sub-array -> TUSMO_TIX_XXX_NESTED2 (e.g., TUSMO_TIX_TIRO_NESTED2)
            # - 4D+ sub-array -> TUSMO_TIX (generic, use as_tix) - can't express 4D+ as typed
            wrap_enum = "TUSMO_TIX"
            wrap_union = "as_tix"
            if base_type in self.TYPE_SUFFIX_MAP:
                type_suffix = self.TYPE_SUFFIX_MAP[base_type]
                if original_depth == 2:
                    # 1D array: use TUSMO_TIX_XXX (e.g., TUSMO_TIX_TIRO)
                    wrap_enum = f"TUSMO_TIX_{type_suffix.upper()}"
                    wrap_union = f"as_{type_suffix.lower()}_tix"
                elif original_depth == 3:
                    # 2D array: use TUSMO_TIX_XXX_NESTED
                    wrap_enum = f"TUSMO_TIX_{type_suffix.upper()}_NESTED"
                    wrap_union = f"as_{type_suffix.lower()}_nested"
                elif original_depth == 4:
                    # 3D array: use TUSMO_TIX_XXX_NESTED2
                    wrap_enum = f"TUSMO_TIX_{type_suffix.upper()}_NESTED2"
                    wrap_union = f"as_{type_suffix.lower()}_nested2"
                # For original_depth >= 5: use TUSMO_TIX with as_tix (can't express 4D+ as typed)
                # wrap_enum and wrap_union already set to TUSMO_TIX and as_tix
            
            # Recursively initialize each sub-array
            for sub_array_literal_node in element_nodes:
                sub_array_type = type_node.element_type
                sub_array_elements = sub_array_literal_node.elements
                sub_init_var = self._generate_recursive_initializer(sub_array_type, sub_array_elements)
                
                if needs_wrap:
                    # Wrap typed nested arrays in TusmoValue with correct type enum
                    wrap_var = self.main_generator.get_temp_var()
                    if wrap_union == "as_tix":
                        # For generic mixed (4D+), cast sub-array to TusmoTixMixed*
                        self.main_generator.c_code += f"    TusmoValue {wrap_var} = (TusmoValue){{.type = {wrap_enum}, .value.{wrap_union} = (TusmoTixMixed*){sub_init_var}}};\n"
                    else:
                        # For typed arrays (1D, 2D, 3D), use as-is
                        self.main_generator.c_code += f"    TusmoValue {wrap_var} = (TusmoValue){{.type = {wrap_enum}, .value.{wrap_union} = {sub_init_var}}};\n"
                    self.main_generator.c_code += f"    tusmo_tix_mixed_append({temp_var}, {wrap_var});\n"
                else:
                    self.main_generator.c_code += f"    {append_func}({temp_var}, {sub_init_var});\n"
        
        # Handle 1D arrays (not nested)
        else:
            element_type_str = str(type_node.element_type)

            # Check if we are creating a dynamic (mixed-type) array
            if element_type_str == 'None' or element_type_str == 'qaamuus':
                create_func = "tusmo_tix_mixed_create"
                append_func = "tusmo_tix_mixed_append"
                self.main_generator.c_code += f"    {c_type} {temp_var} = {create_func}({capacity});\n"
                
                # For mixed arrays, each element must be wrapped in a TusmoValue struct
                for element_node in element_nodes:
                    self.generate_mixed_append_call(temp_var, element_node)
            
            # Otherwise, it's a normal homogeneous 1D array
            else:
                create_func = f"tusmo_hp_tix_{element_type_str}_create"
                append_func = f"tusmo_hp_tix_{element_type_str}_append"
                self.main_generator.c_code += f"    {c_type} {temp_var} = {create_func}({capacity});\n"
                for primitive_node in element_nodes:
                    element_c_code = self.expr_generator.generate_expression(primitive_node)
                    self.main_generator.c_code += f"    {append_func}({temp_var}, {element_c_code});\n"
                
        return temp_var

    def generate_access(self, node: ArrayAccessNode):
        self.main_generator.used_features.add("array")
        base_expr_c = self.expr_generator.generate_expression(node.array_name_node)
        index_c = self.expr_generator.generate_expression(node.index_expression)
        base_tusmo_type = self.expr_generator.get_expression_type(node.array_name_node)

        base_type_str = str(base_tusmo_type)

        # For dynamic_value (TusmoValue from a mixed array), we use tusmo_tix_mixed_get_nested
        # which handles type-switching for typed nested arrays (2D, 3D) stored in TusmoValue.
        if base_type_str == 'dynamic_value':
            temp_var = self.main_generator.get_temp_var()
            self.main_generator.c_code += f"    TusmoValue {temp_var} = {base_expr_c};\n"
            return f"tusmo_tix_mixed_get_nested({temp_var}, {index_c})"

        # For regular array types, the bounds check uses the base pointer
        checked_index = f"tusmo_bounds_check({index_c}, {base_expr_c}->size)"

        # For dynamic arrays (tix with element_type = None or string "None")
        is_dynamic = False
        if isinstance(base_tusmo_type, ArrayTypeNode):
            if base_tusmo_type.element_type is None or str(base_tusmo_type.element_type) == 'None':
                is_dynamic = True
            elif isinstance(base_tusmo_type.element_type, ArrayTypeNode):
                inner = base_tusmo_type.element_type
                while isinstance(inner, ArrayTypeNode):
                    if inner.element_type is None or str(inner.element_type) == 'None':
                        is_dynamic = True
                        break
                    inner = inner.element_type
        
        if is_dynamic:
            return f"tusmo_tix_mixed_get({base_expr_c}, {checked_index})"

        # For typed nested arrays (2D, 3D), need to cast to proper pointer type
        if isinstance(base_tusmo_type, ArrayTypeNode) and isinstance(base_tusmo_type.element_type, ArrayTypeNode):
            element_tusmo_type = base_tusmo_type.element_type
            element_c_type = self.get_c_type_from_tusmo_type(element_tusmo_type)
            return f"(({element_c_type})({base_expr_c}->data[{checked_index}]))"
        
        # For typed 1D arrays
        return f"({base_expr_c}->data[{checked_index}])"

    def generate_assignment(self, node: ArrayAssignmentNode):
        access_c = self.generate_access(node.array_access_node)
        value_c = self.expr_generator.generate_expression(node.value_expression)
        self.main_generator.c_code += f"    {access_c} = {value_c};\n"
        
    # In array_generator.py, replace the generate_method_call method with this:
    def generate_method_call(self, node: MethodCallNode):
        self.main_generator.used_features.add("array")
        object_c = self.expr_generator.generate_expression(node.object_node)
        object_type = self.expr_generator.get_expression_type(node.object_node)
        args = node.args_list # Use raw args list as we handle named args manually

        if node.method_name == 'gali':
            if len(args) == 2:
                # Insert: gali(boos=i, value)
                # First arg is boos=i (NamedArgument)
                index_node = args[0].value
                value_node = args[1]
                self.generate_insert_call(object_c, object_type, index_node, value_node)
            else:
                # Append: gali(value)
                self.generate_append_call(object_c, object_type, args[0])
            return ""

        if node.method_name == 'kasaar':
            arg = args[0]
            if isinstance(arg, NamedArgument) and arg.name == 'boos':
                # Pop: kasaar(boos=i)
                return self.generate_pop_call(object_c, object_type, arg.value)
            else:
                # Remove: kasaar(value)
                return self.generate_remove_call(object_c, object_type, arg)
        
        return ""

    def generate_append_call(self, array_c_name, array_type_node, element_node):
        element_type = array_type_node.element_type
        
        if element_type is None:
            self.generate_mixed_append_call(array_c_name, element_node)
        elif isinstance(element_type, ArrayTypeNode): # Nested array
            element_c_code = self.expr_generator.generate_expression(element_node)
            self.main_generator.c_code += f"    tusmo_tix_generic_append({array_c_name}, {element_c_code});\n"
        elif not isinstance(element_type, ArrayTypeNode):
            element_c_code = self.expr_generator.generate_expression(element_node)
            append_func = f"tusmo_hp_tix_{element_type}_append"
            self.main_generator.c_code += f"    {append_func}({array_c_name}, {element_c_code});\n"

    def generate_insert_call(self, array_c_name, array_type_node, index_node, element_node):
        element_type = array_type_node.element_type
        index_c = self.expr_generator.generate_expression(index_node)
        
        if element_type is None:
            self.generate_mixed_insert_call(array_c_name, index_c, element_node)
        elif isinstance(element_type, ArrayTypeNode): # Nested array
            element_c_code = self.expr_generator.generate_expression(element_node)
            self.main_generator.c_code += f"    tusmo_tix_generic_insert({array_c_name}, {index_c}, {element_c_code});\n"
        elif not isinstance(element_type, ArrayTypeNode):
            element_c_code = self.expr_generator.generate_expression(element_node)
            insert_func = f"tusmo_hp_tix_{element_type}_insert"
            self.main_generator.c_code += f"    {insert_func}({array_c_name}, {index_c}, {element_c_code});\n"

    def generate_pop_call(self, array_c_name, array_type_node, index_node):
        element_type = array_type_node.element_type
        index_c = self.expr_generator.generate_expression(index_node)
        
        if element_type is None:
            return f"tusmo_tix_mixed_pop({array_c_name}, {index_c})"
        elif isinstance(element_type, ArrayTypeNode): # Nested array
             # Return type needs cast to appropriate generic type, or just void*
             # But compiler expects valid C expr.
             # The correct return type for tix:tix:tiro is TusmoTixTiro*.
             # generic_pop returns void*. We need to cast it.
             # We can't easily determine the exact C struct name here without recursion logic, 
             # but get_c_type_from_tusmo_type does that.
             ret_type = self.get_c_type_from_tusmo_type(element_type)
             return f"(({ret_type})tusmo_tix_generic_pop({array_c_name}, {index_c}))"
        elif not isinstance(element_type, ArrayTypeNode):
            pop_func = f"tusmo_hp_tix_{element_type}_pop"
            return f"{pop_func}({array_c_name}, {index_c})"
        return "0" 

    def generate_remove_call(self, array_c_name, array_type_node, element_node):
        element_type = array_type_node.element_type
        
        if element_type is None:
            return self.generate_mixed_remove_call(array_c_name, element_node)
        elif isinstance(element_type, ArrayTypeNode): # Nested array
            element_c_code = self.expr_generator.generate_expression(element_node)
            return f"tusmo_tix_generic_remove({array_c_name}, (void*){element_c_code})"
        elif not isinstance(element_type, ArrayTypeNode):
            element_c_code = self.expr_generator.generate_expression(element_node)
            remove_func = f"tusmo_hp_tix_{str(element_type).lower()}_remove"
            return f"{remove_func}({array_c_name}, {element_c_code})"
        return "false"

    def _calculate_array_depth(self, type_node, depth=0):
        """Calculate the nesting depth of an array type."""
        if isinstance(type_node, ArrayTypeNode):
            element = type_node.element_type
            if isinstance(element, ArrayTypeNode):
                return self._calculate_array_depth(element, depth + 1)
            else:
                return depth + 1
        return depth

    def _is_array_type(self, type_node):
        """Check if a type node is an array type (returns depth, or 0 if not an array)."""
        if isinstance(type_node, ArrayTypeNode):
            return self._calculate_array_depth(type_node)
        return 0

    def _get_nested_array_type_info(self, type_node, depth=0):
        """
        Get the type info for nested arrays.
        Returns (enum_name, union_member) for the innermost type.
        """
        if isinstance(type_node, ArrayTypeNode):
            element = type_node.element_type
            if isinstance(element, ArrayTypeNode):
                # Nested deeper - get info from inner type
                return self._get_nested_array_type_info(element, depth + 1)
            else:
                # Base type found - determine the right enum/union member based on depth
                base_type = str(element)
                if depth == 1:
                    # 2D array
                    enum_map = {
                        'tiro': 'TUSMO_TIX_TIRO_NESTED', 'jajab': 'TUSMO_TIX_JAJAB_NESTED',
                        'eray': 'TUSMO_TIX_ERAY_NESTED', 'miyaa': 'TUSMO_TIX_MIYAA_NESTED',
                        'xaraf': 'TUSMO_TIX_XARAF_NESTED'
                    }
                    union_map = {
                        'tiro': 'as_tiro_nested', 'jajab': 'as_jajab_nested',
                        'eray': 'as_eray_nested', 'miyaa': 'as_miyaa_nested',
                        'xaraf': 'as_xaraf_nested'
                    }
                elif depth >= 2:
                    # 3D+ array
                    enum_map = {
                        'tiro': 'TUSMO_TIX_TIRO_NESTED2', 'jajab': 'TUSMO_TIX_JAJAB_NESTED2',
                        'eray': 'TUSMO_TIX_ERAY_NESTED2', 'miyaa': 'TUSMO_TIX_MIYAA_NESTED2',
                        'xaraf': 'TUSMO_TIX_XARAF_NESTED2'
                    }
                    union_map = {
                        'tiro': 'as_tiro_nested2', 'jajab': 'as_jajab_nested2',
                        'eray': 'as_eray_nested2', 'miyaa': 'as_miyaa_nested2',
                        'xaraf': 'as_xaraf_nested2'
                    }
                else:
                    # depth 0 - shouldn't happen
                    return (None, None)
                
                return (enum_map.get(base_type), union_map.get(base_type))
        return (None, None)

    def _generate_tusmo_value(self, element_node):
        """Helper to generate a TusmoValue struct initialization code."""
        element_c_code = self.expr_generator.generate_expression(element_node)
        element_tusmo_type = self.expr_generator.get_expression_type(element_node)
        
        type_enum_map = {'tiro': 'TUSMO_TIRO', 'eray': 'TUSMO_ERAY', 'jajab': 'TUSMO_JAJAB', 'miyaa': 'TUSMO_MIYAA', 'xaraf': 'TUSMO_XARAF', 'qaamuus': 'TUSMO_QAAMUUS'}
        union_member_map = {'tiro': 'as_tiro', 'eray': 'as_eray', 'jajab': 'as_jajab', 'miyaa': 'as_miyaa', 'xaraf': 'as_xaraf', 'qaamuus': 'as_qaamuus'}
        
        type_str = str(element_tusmo_type)
        temp_var = self.main_generator.get_temp_var()
        
        self.main_generator.c_code += f"    TusmoValue {temp_var};\n"
        
        # Check if this is an array type
        is_array = isinstance(element_tusmo_type, ArrayTypeNode)
        
        if is_array:
            # For arrays in dynamic arrays, use typed nested enum/union
            depth = element_tusmo_type.get_array_depth()
            base_type = element_tusmo_type.get_base_type()
            if depth >= 4:
                # 4D+ arrays - use generic TUSMO_TIX with cast
                self.main_generator.c_code += f"    {temp_var}.type = TUSMO_TIX;\n"
                self.main_generator.c_code += f"    {temp_var}.value.as_tix = (TusmoTixMixed*){element_c_code};\n"
            elif depth >= 2:
                # 2D or 3D nested array
                enum_name, union_member = self._get_nested_array_type_info(element_tusmo_type)
                if enum_name and union_member:
                    self.main_generator.c_code += f"    {temp_var}.type = {enum_name};\n"
                    self.main_generator.c_code += f"    {temp_var}.value.{union_member} = {element_c_code};\n"
                else:
                    self.main_generator.c_code += f"    {temp_var}.type = TUSMO_WAXBA;\n"
            else:
                # 1D array in dynamic array - use typed 1D array enum
                # base_type is already computed above
                enum_map = {
                    'tiro': 'TUSMO_TIX_TIRO', 'jajab': 'TUSMO_TIX_JAJAB',
                    'eray': 'TUSMO_TIX_ERAY', 'miyaa': 'TUSMO_TIX_MIYAA',
                    'xaraf': 'TUSMO_TIX_XARAF'
                }
                union_map = {
                    'tiro': 'as_tiro_tix', 'jajab': 'as_jajab_tix',
                    'eray': 'as_eray_tix', 'miyaa': 'as_miyaa_tix',
                    'xaraf': 'as_xaraf_tix'
                }
                enum_name = enum_map.get(base_type)
                union_member = union_map.get(base_type)
                if enum_name and union_member:
                    self.main_generator.c_code += f"    {temp_var}.type = {enum_name};\n"
                    self.main_generator.c_code += f"    {temp_var}.value.{union_member} = {element_c_code};\n"
                else:
                    # Fallback to generic TUSMO_TIX
                    self.main_generator.c_code += f"    {temp_var}.type = TUSMO_TIX;\n"
                    self.main_generator.c_code += f"    {temp_var}.value.as_tix = {element_c_code};\n"
        elif type_str in type_enum_map:
            self.main_generator.c_code += f"    {temp_var}.type = {type_enum_map[type_str]};\n"
            self.main_generator.c_code += f"    {temp_var}.value.{union_member_map[type_str]} = {element_c_code};\n"
        elif type_str == 'qaamuus':
            self.main_generator.c_code += f"    {temp_var}.type = TUSMO_QAAMUUS;\n"
            self.main_generator.c_code += f"    {temp_var}.value.as_qaamuus = {element_c_code};\n"
        elif type_str == 'tix' or type_str == 'None':
            self.main_generator.c_code += f"    {temp_var}.type = TUSMO_TIX;\n"
            self.main_generator.c_code += f"    {temp_var}.value.as_tix = {element_c_code};\n"
        else:
            self.main_generator.c_code += f"    {temp_var}.type = TUSMO_WAXBA;\n"
            
        return temp_var

    def generate_mixed_append_call(self, array_c_name, element_node):
        temp_var = self._generate_tusmo_value(element_node)
        self.main_generator.c_code += f"    tusmo_tix_mixed_append({array_c_name}, {temp_var});\n"

    def generate_mixed_insert_call(self, array_c_name, index_c, element_node):
        temp_var = self._generate_tusmo_value(element_node)
        self.main_generator.c_code += f"    tusmo_tix_mixed_insert({array_c_name}, {index_c}, {temp_var});\n"

    def generate_mixed_remove_call(self, array_c_name, element_node):
        # For remove, we need to pass the value to check against
        # But _generate_tusmo_value emits statements, so we can't use it directly in an expression.
        # We need to emit the setup code and then call the function.
        # Since this method is expected to return an expression string (bool),
        # we might need to use a statement expression or pre-calculate.
        # However, generate_remove_call is called where an expression is expected.
        # This is tricky in C if we need multiple statements.
        # Solution: Use the comma operator or a statement expression if GCC extension is allowed.
        # Or better: generate the setup code BEFORE the current expression context?
        # The expression generator expects a string return.
        # If we are inside a larger expression, we can't easily emit statements.
        # BUT `generate_method_call` is usually called as a statement (for void methods) or expression.
        # `kasaar` returns a bool, so it's an expression.
        # We can use the GCC statement expression extension `({ ... })` which is standard in many C compilers including GCC/Clang.
        
        temp_var = self.main_generator.get_temp_var()
        element_c_code = self.expr_generator.generate_expression(element_node)
        element_tusmo_type = self.expr_generator.get_expression_type(element_node)
        type_str = str(element_tusmo_type)
        
        type_enum_map = {'tiro': 'TUSMO_TIRO', 'eray': 'TUSMO_ERAY', 'jajab': 'TUSMO_JAJAB', 'miyaa': 'TUSMO_MIYAA', 'xaraf': 'TUSMO_XARAF', 'qaamuus': 'TUSMO_QAAMUUS'}
        union_member_map = {'tiro': 'as_tiro', 'eray': 'as_eray', 'jajab': 'as_jajab', 'miyaa': 'as_miyaa', 'xaraf': 'as_xaraf', 'qaamuus': 'as_qaamuus'}
        
        setup_code = f"TusmoValue {temp_var}; {temp_var}.type = {type_enum_map.get(type_str, 'TUSMO_WAXBA')};"
        if type_str in union_member_map:
            setup_code += f" {temp_var}.value.{union_member_map[type_str]} = {element_c_code};"
            
        return f"({{ {setup_code} tusmo_tix_mixed_remove({array_c_name}, {temp_var}); }})"
