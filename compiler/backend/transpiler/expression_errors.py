# expression_errors.py

class Cilad(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return (
            f"\033[1;31m[!] CILAD GENERATOR:\033[0m {self.message}\n"
            f"\033[90m" + ("-" * 45) + "\033[0m\n"
            f"\033[1;33mTalo:\033[0m Haddii aad aragto ciladan, fadlan hubi habka aad u qortay koodka.\n"
        )

def ERR_NOT_AST_NODE(node_type):
    return f"generate_expression waxay heshay '{node_type}' halkii laga rabay AST node."

def ERR_NO_GEN_LOGIC(node_type):
    return f"Ma jiro hab loo bedelo (C code) expression-ka noociisu yahay '{node_type}'."

def ERR_UNKNOWN_OP(op):
    return f"Hawl-wadeen (operator) aan la aqoon: '{op}'."

def ERR_FSTRING_TYPE():
    return f"""F-string expressions waa inay noqdaan 'eray', 'xaraf', 'tiro', 'jajab', ama 'miyaa'.
                    
        \033[1;31m keyd:tix t = []; qor(\"{{t}}\"); \033[1;35m // tix (array) laguma ridi karo f-string
        \033[1;32m qor(\"Magacu waa: {{magac}}\"); \033[1;35m // sidani waa sax"""

def ERR_CAST_ARG_COUNT(name, actual):
    return f"""Hawsha '{name}' waxay filaysaa 1 parameter, laakiin waxaa lasiiyay {actual}.
                    
        \033[1;31m {name}(x, y); \033[1;35m // parameter badan
        \033[1;32m {name}(x); \033[1;35m // sidani waa sax"""

def ERR_DHERER_ARG_COUNT(actual):
    return f"""Hawsha 'dherer' waxay filaysaa 1 parameter, laakiin waxaa lasiiyay {actual}.
                    
        \033[1;31m dherer(x, y); \033[1;35m // parameter badan
        \033[1;32m dherer(x); \033[1;35m // sidani waa sax"""

def ERR_DHERER_TYPE(actual_type):
    return f"""Hawsha 'dherer' ma taageerto nooca '{actual_type}'.
                    
        \033[1;31m dherer(10); \033[1;35m // 'tiro' ma laha dherer
        \033[1;32m dherer("Tusmo"); \033[1;35m // sidani waa sax (eray ama tix)"""

def ERR_NOOC_ARG_COUNT():
    return f"Hawsha 'nooc' waxay u baahan tahay hal (1) parameter oo sax ah."

def ERR_NOOC_TIX_QUERY():
    return f"nooc(arr[]) waxay u baahan tahay keydiye tix (array variable) ah."

def ERR_TIX_CAYIMAN_USAGE():
    return f"""'tix_cayiman' waxaa loo isticmaali karaa oo kaliya marka keydiye cusub la samaynayo.
                    
        \033[1;31m qor(tix_cayiman()); \033[1;35m // halkan laguma isticmaali karo
        \033[1;32m keyd:tix:eray t = tix_cayiman(); \033[1;35m // sidani waa sax"""

def ERR_FUNC_NOT_FOUND(name):
    return f"Hawsha '{name}' ma ahan mid jirta ama lama helin."

def ERR_MISSING_PARAM(param_name):
    return f"Waxaa maqan qiimaha halbeegga '{param_name}' oo aan lahayn qiimo caadi ah (default)."
