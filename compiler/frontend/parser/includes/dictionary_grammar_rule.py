# compiler/frontend/parser/includes/dictionary_grammar_rule.py
# Dictionary initialization
from ..ast_nodes import (
    DictionaryInitializationNode,
)

# Dictionary access: identifier["string_key"]
# Only match literal string keys to avoid conflicts with array access
def p_dictionary_access_string(p):
    '''expression : IDENTIFIER LBRACKET STRING RBRACKET'''
    line = p.lineno(2)
    filename = p.lexer.filename
    from ..ast_nodes import IdentifierNode, StringNode, DictionaryAccessNode
    dict_node = IdentifierNode(p[1], line=line, filename=filename)
    key_node = StringNode(p[3], line=line, filename=filename)
    p[0] = DictionaryAccessNode(line, dict_node, key_node, filename)

# Dictionary assignment: identifier["key"] = value (with string literal key)
def p_dictionary_assignment_string(p):
    '''statement : IDENTIFIER LBRACKET STRING RBRACKET EQUALS expression SEMICOLON'''
    line = p.lineno(2)
    filename = p.lexer.filename
    from ..ast_nodes import IdentifierNode, StringNode, DictionaryAccessNode, DictionaryAssignmentNode
    dict_node = IdentifierNode(p[1], line=line, filename=filename)
    key_node = StringNode(p[3], line=line, filename=filename)
    value_node = p[6]
    dict_access = DictionaryAccessNode(line, dict_node, key_node, filename)
    p[0] = DictionaryAssignmentNode(line, dict_access, value_node, filename)
