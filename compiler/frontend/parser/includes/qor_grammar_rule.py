from compiler.frontend.parser.ast_nodes import QorNode

def p_qor_statement(p):
    '''qor_statement : QOR LPAREN argument_list_opt RPAREN SEMICOLON'''    
    line = p.lineno(1)
    filename = p.lexer.filename 
    p[0] = QorNode(line, p[3], filename)