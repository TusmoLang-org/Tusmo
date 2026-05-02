# compiler/midend/lifetime_tracker.py

class LifetimeTracker:
    def __init__(self, symbol_table=None):
        # scope_stack: list of dicts {var_name: info}
        self.scopes = []
        # var_name -> node_where_it_was_moved (Global for the entire analysis)
        self.moved_variables = {}
        # Set of variables that have already been cleared (freed) in a child scope
        self.cleared_variables = set()
        self.symbol_table = symbol_table

    def is_heap_type(self, type_str):
        type_str = str(type_str)
        if "tix" in type_str or "qaamuus" in type_str or type_str == "eray":
            return True
            
        if self.symbol_table:
            info = self.symbol_table.get(type_str)
            if info and info[1] == 'struct_definition':
                return False
                
        if type_str and type_str[0].isupper(): # Class names
            return True
        return False

    def get_free_function(self, type_str):
        type_str = str(type_str)
        if type_str == "tix:tiro": return "tusmo_free_tix_tiro"
        if type_str == "tix:eray": return "tusmo_free_tix_eray"
        if type_str == "tix:jajab": return "tusmo_free_tix_jajab"
        if type_str == "tix:miyaa": return "tusmo_free_tix_miyaa"
        if type_str == "tix:xaraf": return "tusmo_free_tix_xaraf"
        if type_str == "tix:tix:tiro": return "tusmo_free_tix_tiro_nested"
        if type_str == "tix:tix:eray": return "tusmo_free_tix_eray_nested"
        if type_str == "eray": return "tusmo_free_eray"
        if type_str == "qaamuus": return "tusmo_free_qaamuus"
        if type_str and type_str[0].isupper(): return "free"
        return "free"

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if not self.scopes:
            return []
        
        current_scope_vars = self.scopes.pop()
        cleanup_list = []
        
        for var_name, info in current_scope_vars.items():
            # Only free if it's heap-allocated and hasn't been moved or cleared
            if (self.is_heap_type(info['type']) and 
                var_name not in self.moved_variables and 
                var_name not in self.cleared_variables):
                
                cleanup_list.append({
                    'name': var_name,
                    'type': info['type'],
                    'node': info['node'],
                    'free_fn': self.get_free_function(info['type'])
                })
                self.cleared_variables.add(var_name)
        return cleanup_list

    def record_definition(self, var_name, var_type, node, is_initialized=False):
        if self.scopes:
            self.scopes[-1][var_name] = {
                'type': var_type,
                'node': node,
                'initialized': is_initialized
            }
        # If it was previously moved, but now redefined, clear the move
        if var_name in self.moved_variables:
            del self.moved_variables[var_name]
        if var_name in self.cleared_variables:
            self.cleared_variables.remove(var_name)

    def mark_initialized(self, var_name):
        """U sheeg tracker-ka in variable-ka qiime la siiyay."""
        for scope in reversed(self.scopes):
            if var_name in scope:
                scope[var_name]['initialized'] = True
                return

    def is_initialized(self, var_name):
        """Hubi haddii variable-ka uu leeyahay qiime."""
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name].get('initialized', False)
        return True # Default to True for globals/built-ins for now

    def get_all_active_heap_vars(self):
        cleanup_list = []
        # Iterate through scopes but skip the global scope (index 0)
        # We don't want functions freeing global variables when they return!
        for scope_vars in reversed(self.scopes[1:]):
            for var_name, info in scope_vars.items():
                if (self.is_heap_type(info['type']) and 
                    var_name not in self.moved_variables and 
                    var_name not in self.cleared_variables):
                    cleanup_list.append({
                        'name': var_name,
                        'type': info['type'],
                        'node': info['node'],
                        'free_fn': self.get_free_function(info['type'])
                    })
        return cleanup_list

    def get_active_heap_vars_for_loop(self):
        # In Tusmo, the loop scope is typically the last scope pushed,
        # but we might be inside a nested block within the loop.
        # This simplified version just gets variables from the innermost scope
        # which represents the current loop body block.
        cleanup_list = []
        if not self.scopes: return cleanup_list
        scope_vars = self.scopes[-1]
        for var_name, info in scope_vars.items():
            if (self.is_heap_type(info['type']) and 
                var_name not in self.moved_variables and 
                var_name not in self.cleared_variables):
                cleanup_list.append({
                    'name': var_name,
                    'type': info['type'],
                    'node': info['node'],
                    'free_fn': self.get_free_function(info['type'])
                })
        return cleanup_list

    def record_move(self, var_name, move_node):
        self.moved_variables[var_name] = move_node

    def record_usage(self, var_name, node):
        """Used by semantic analyzer to track variable life."""
        pass

    def record_borrow(self, var_name, borrow_node):
        pass

    def revive(self, var_name):
        """Variable mar hore dhimaday dib u soo nooleey madaama qiime cusub la siiyay."""
        if var_name in self.moved_variables:
            del self.moved_variables[var_name]
        if var_name in self.cleared_variables:
            self.cleared_variables.remove(var_name)

    def is_moved(self, var_name):
        return var_name in self.moved_variables

    def get_move_node(self, var_name):
        return self.moved_variables.get(var_name)
