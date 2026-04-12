# keen_grammer_rule.py 
from compiler.frontend.parser.ast_nodes import KeenNode, IsticmaalNode

def p_keen_import(p):
    '''keen_import : KEEN STRING SEMICOLON'''
    line = p.lineno(1)
    filename_to_import = p[2].strip('"\'')
    source_filename = p.lexer.filename
    p[0] = KeenNode(line, filename_to_import, source_filename)

def p_isticmaal_import(p):
    '''isticmaal_import : ISTICMAAL LBRACE import_name_list RBRACE KUJIRA STRING SEMICOLON'''
    line = p.lineno(1)
    names_to_import = p[3] or []
    filename_to_import = p[6].strip('"\'')
    source_filename = p.lexer.filename
    p[0] = IsticmaalNode(line, names_to_import, filename_to_import, source_filename)

def p_import_name_list(p):
    '''import_name_list : import_name_list COMMA IDENTIFIER
                        | IDENTIFIER
                        | empty'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []
