# hel_grammer_rule.py (La cusboonaysiiyay)
from compiler.frontend.parser.ast_nodes import HelNode

def p_hel_statement(p):
    '''hel : HEL LPAREN IDENTIFIER RPAREN SEMICOLON
            | HEL IDENTIFIER SEMICOLON
            | HEL LPAREN STRING COMMA IDENTIFIER RPAREN SEMICOLON
            | HEL STRING IDENTIFIER SEMICOLON'''
    line = p.lineno(1)
    filename = p.lexer.filename
    
    # hel x; (len = 4)
    if len(p) == 4:
        var_name = p[2]
        prompt = None
    # hel(x); (len = 6)
    elif len(p) == 6:
        var_name = p[3]
        prompt = None
    # hel "prompt" var; (len = 5)
    elif len(p) == 5:
        var_name = p[3]
        prompt = p[2]
    # hel("prompt", var); (len = 8)
    else:
        prompt = p[3]
        var_name = p[5]
    
    p[0] = HelNode(line, var_name, filename, prompt)