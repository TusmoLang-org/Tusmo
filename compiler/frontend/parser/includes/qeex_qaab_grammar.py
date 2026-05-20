# compiler/frontend/parser/includes/qeex_qaab_grammar.py
from compiler.frontend.parser.ast_nodes import QeexNode, QaabNode

def p_qeex_declaration(p):
    '''qeex_declaration : QEEX IDENTIFIER EQUALS expression SEMICOLON
                        | QEEX IDENTIFIER EQUALS IDENTIFIER SEMICOLON'''
    from compiler.frontend.parser.ast_nodes import QeexNode, IdentifierNode
    if len(p) == 6:
        if isinstance(p[4], str): # Case 2: Identifier
             # We create a synthetic IdentifierNode for the C macro
             val_node = IdentifierNode(p[4], p.lineno(4), p.lexer.filename)
             p[0] = QeexNode(p[2], val_node, p.lineno(1), p.lexer.filename)
        else:
             p[0] = QeexNode(p[2], p[4], p.lineno(1), p.lexer.filename)

def p_struct_literal(p):
    '''expression : LPAREN IDENTIFIER RPAREN LBRACE argument_list_opt RBRACE'''
    from compiler.frontend.parser.ast_nodes import QaabQiimeNode
    p[0] = QaabQiimeNode(p[2], p[5], p.lineno(1), p.lexer.filename)

def p_qaab_declaration(p):
    '''qaab_declaration : QAAB IDENTIFIER LBRACE struct_member_list RBRACE SEMICOLON'''
    p[0] = QaabNode(p[2], p[4], p.lineno(1), p.lexer.filename)

def p_struct_member_list(p):
    '''struct_member_list : struct_member_list struct_member
                          | struct_member
                          | empty'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_struct_member(p):
    '''struct_member : KEYD COLON type_specifier IDENTIFIER SEMICOLON'''
    from compiler.frontend.parser.ast_nodes import KeydNode
    p[0] = KeydNode(p[4], p[3], None, p.lineno(1), p.lexer.filename)
