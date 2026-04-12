# compiler/frontend/parser/includes/class_grammer_rule.py (Corrected)
from compiler.frontend.parser.ast_nodes import (
    ClassNode,
    KeydNode,
    FunctionNode,
    ClassInstantiationNode,
    MemberAccessNode,
    MethodCallNode,
    ThisNode,
    WaalidNode,
    StringNode,
)
from compiler.frontend.parser.includes.built_in_fn_grammer_rules import p_built_in_fn_names

def p_expression_waalid(p):
    '''expression : WAALID'''
    line = p.lineno(1)
    filename = p.lexer.filename
    p[0] = WaalidNode(line, filename)

def p_class_declaration(p):
    '''class_declaration : KOOX IDENTIFIER LBRACE class_body RBRACE
                         | KOOX IDENTIFIER DHAXLAYA IDENTIFIER LBRACE class_body RBRACE'''
    line = p.lineno(1)
    filename = p.lexer.filename
    if len(p) == 6:
        # No Dhaxlaya(inheritance)
        parent_name = None
        items = p[4] or []
        name = p[2]
    else:
        # with Dhaxlaya(Inheritance)
        parent_name = p[4]
        items = p[6] or []
        name = p[2]
    docstring_value = None
    if items and isinstance(items[0], StringNode):
        docstring_value = items[0].value
        items = items[1:]
    members = [item for item in items if isinstance(item, KeydNode)]
    methods = [item for item in items if isinstance(item, FunctionNode)]
    class_node = ClassNode(name, members, methods, line, filename, parent_name=parent_name)
    class_node.docstring = docstring_value
    p[0] = class_node

def p_class_body(p):
    '''class_body : docstring_opt class_member_list'''
    if p[1]:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = p[2]

def p_class_member_list(p):
    '''class_member_list : class_member_list class_member
                         | class_member
                         | empty'''
    if len(p) == 3: p[1].append(p[2]); p[0] = p[1]
    elif len(p) == 2 and p[1] is not None: p[0] = [p[1]]
    else: p[0] = []

def p_class_member(p):
    '''class_member : declaration
                    | function_declaration
                    | constructor_declaration'''
    p[0] = p[1]

def p_docstring_opt(p):
    '''docstring_opt : STRING
                     | empty'''
    if p[1]:
        p[0] = StringNode(p[1], line=p.lineno(1), filename=p.lexer.filename)
    else:
        p[0] = None

def p_constructor_declaration(p):
    '''constructor_declaration : DHIS LPAREN parameter_list RPAREN COLON WAXBO body_statements'''
    line = p.lineno(1)
    filename = p.lexer.filename
    p[0] = FunctionNode(
        return_type='waxbo',
        name='dhis',
        params=p[3],
        body=p[7],
        line=line,
        filename=filename
    )

def p_expression_instantiation(p):
    '''expression : IDENTIFIER LPAREN argument_list_opt RPAREN CUSUB'''
    line = p.lineno(1)
    filename = p.lexer.filename
    p[0] = ClassInstantiationNode(p[1], p[3], line, filename)

def p_expression_member_access(p):
    '''expression : expression DOT IDENTIFIER'''
    line = p.lineno(2)
    filename = p.lexer.filename
    p[0] = MemberAccessNode(p[1], p[3], line, filename)

def p_expression_method_call(p):
    '''expression : expression DOT IDENTIFIER LPAREN argument_list_opt RPAREN
                  | expression DOT DHIS LPAREN argument_list_opt RPAREN
                  | expression DOT fn_name LPAREN argument_list_opt RPAREN'''
    line = p.lineno(2)
    filename = p.lexer.filename
    p[0] = MethodCallNode(line, p[1], p[3], p[5], filename)
