from compiler.frontend.parser.ast_nodes import Xidid

def p_tusmo_xidid(p):
    '''statement_return : TUSMO_XIDID STRING SEMICOLON'''
    xidid = p[2]
    if len(p) == 4:
        p[0] = Xidid(xidid)
