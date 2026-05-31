# compiler/midend/lifetime_tracker.py

class LifetimeTracker:
    def __init__(self, symbol_table=None):
        # scope_stack: list of dicts {var_name: info}
        # info has keys: 'type', 'node', 'initialized', 'borrowed', 'moved', 'cleared'
        self.scopes = []
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
            if (self.is_heap_type(info['type']) and 
                info.get('moved') is None and 
                not info.get('cleared', False) and
                not info.get('borrowed', False)):
                
                cleanup_list.append({
                    'name': var_name,
                    'type': info['type'],
                    'node': info['node'],
                    'free_fn': self.get_free_function(info['type'])
                })
                info['cleared'] = True
        return cleanup_list

    def record_definition(self, var_name, var_type, node, is_initialized=False, borrowed=False):
        if self.scopes:
            self.scopes[-1][var_name] = {
                'type': var_type,
                'node': node,
                'initialized': is_initialized,
                'borrowed': borrowed,
                'moved': None,
                'cleared': False
            }

    def mark_initialized(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                scope[var_name]['initialized'] = True
                return

    def is_initialized(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name].get('initialized', False)
        return True # Default to True for globals/built-ins

    def get_all_active_heap_vars(self):
        cleanup_list = []
        # Iterate through scopes but skip the global scope (index 0)
        for scope_vars in reversed(self.scopes[1:]):
            for var_name, info in scope_vars.items():
                if (self.is_heap_type(info['type']) and 
                    info.get('moved') is None and 
                    not info.get('cleared', False) and
                    not info.get('borrowed', False)):
                    cleanup_list.append({
                        'name': var_name,
                        'type': info['type'],
                        'node': info['node'],
                        'free_fn': self.get_free_function(info['type'])
                    })
                    info['cleared'] = True # Mark as cleared since we are emitting a free
        return cleanup_list

    def get_active_heap_vars_for_loop(self):
        cleanup_list = []
        if not self.scopes: return cleanup_list
        scope_vars = self.scopes[-1]
        for var_name, info in scope_vars.items():
            if (self.is_heap_type(info['type']) and 
                info.get('moved') is None and 
                not info.get('cleared', False) and
                not info.get('borrowed', False)):
                cleanup_list.append({
                    'name': var_name,
                    'type': info['type'],
                    'node': info['node'],
                    'free_fn': self.get_free_function(info['type'])
                })
        return cleanup_list

    def record_move(self, var_name, move_node):
        for scope in reversed(self.scopes):
            if var_name in scope:
                scope[var_name]['moved'] = move_node
                return

    def record_usage(self, var_name, node):
        pass

    def record_borrow(self, var_name, borrow_node):
        pass

    def revive(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                scope[var_name]['moved'] = None
                scope[var_name]['cleared'] = False
                return

    def is_moved(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name].get('moved') is not None
        return False

    def get_move_node(self, var_name):
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name].get('moved')
        return None