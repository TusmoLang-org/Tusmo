# function_grammer_rule.py (Updated)
from compiler.frontend.parser.ast_nodes import FunctionNode, FunctionCallNode, ParameterNode, LambdaNode

def p_function_declaration(p):
    '''function_declaration : HAWL IDENTIFIER LPAREN parameter_list RPAREN COLON type_specifier body_statements
                           | SHAQO IDENTIFIER LPAREN parameter_list RPAREN COLON type_specifier body_statements
                           | HAWL IDENTIFIER LPAREN parameter_list RPAREN ARROW type_specifier body_statements
                           | SHAQO IDENTIFIER LPAREN parameter_list RPAREN ARROW type_specifier body_statements
                           | HAWL IDENTIFIER LPAREN parameter_list RPAREN COLON WAXBO body_statements
                           | SHAQO IDENTIFIER LPAREN parameter_list RPAREN COLON WAXBO body_statements
                           | HAWL IDENTIFIER LPAREN parameter_list RPAREN ARROW WAXBO body_statements
                           | SHAQO IDENTIFIER LPAREN parameter_list RPAREN ARROW WAXBO body_statements
                           | HAWL fn_name LPAREN parameter_list RPAREN COLON type_specifier body_statements
                           | SHAQO fn_name LPAREN parameter_list RPAREN COLON type_specifier body_statements
                           | HAWL fn_name LPAREN parameter_list RPAREN ARROW type_specifier body_statements
                           | SHAQO fn_name LPAREN parameter_list RPAREN ARROW type_specifier body_statements
                           | HAWL fn_name LPAREN parameter_list RPAREN COLON WAXBO body_statements
                           | SHAQO fn_name LPAREN parameter_list RPAREN COLON WAXBO body_statements
                           | HAWL fn_name LPAREN parameter_list RPAREN ARROW WAXBO body_statements
                           | SHAQO fn_name LPAREN parameter_list RPAREN ARROW WAXBO body_statements'''
    line = p.lineno(1)
    filename = p.lexer.filename
    if p[6] == ':' or p[6] == '=>':
         p[0] = FunctionNode(return_type=p[7], name=p[2], params=p[4], body=p[8], line=line, filename=filename)

def p_anonymous_function(p):
    '''anonymous_function : HAWL LPAREN parameter_list RPAREN ARROW expression
                          | HAWL LPAREN parameter_list RPAREN COLON type_specifier body_statements'''
    line = p.lineno(1)
    filename = p.lexer.filename
    if p[5] == '=>':
        # Concise one-liner: hawl(params) => expression
        p[0] = LambdaNode(params=p[3], return_type=None, body=p[6], is_concise=True, line=line, filename=filename)
    else:
        # Full block: hawl(params): type { body }
        p[0] = LambdaNode(params=p[3], return_type=p[6], body=p[7], is_concise=False, line=line, filename=filename)

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter
                      | empty'''
    if len(p) == 4: p[1].append(p[3]); p[0] = p[1]
    elif len(p) == 2 and p[1] is not None: p[0] = [p[1]]
    else: p[0] = []

def p_parameter(p):
    '''parameter : IDENTIFIER COLON type_specifier
                 | IDENTIFIER COLON type_specifier EQUALS expression'''
    if len(p) == 4:
        p[0] = ParameterNode(name=p[1], param_type=p[3], line=p.lineno(1), filename=p.lexer.filename)
    else:
        p[0] = ParameterNode(name=p[1], param_type=p[3], default_value=p[5], line=p.lineno(1), filename=p.lexer.filename)

def p_expression_function_call(p):
    # USE 'argument_list_opt' TO AVOID CONFLICTS
    '''function_call : IDENTIFIER LPAREN argument_list_opt RPAREN
                     | fn_name LPAREN argument_list_opt RPAREN'''
    line = p.lineno(1)
    filename = p.lexer.filename
    p[0] = FunctionCallNode(p[1], p[3], line, filename)

def p_argument_list(p):
    # FIX CONFLICT: An argument list has one or more items
    '''argument_list : argument_list COMMA argument
                     | argument'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_argument_list_opt(p):
    #ADDED: This handles both empty and non-empty lists for function calls
    '''argument_list_opt : argument_list
                         | empty'''
    p[0] = p[1] if p[1] else []

def p_argument_named(p):
    '''argument : IDENTIFIER EQUALS expression'''
    from compiler.frontend.parser.ast_nodes import NamedArgument
    p[0] = NamedArgument(name=p[1], value=p[3], line=p.lineno(1), filename=p.lexer.filename)

def p_argument_positional(p):
    '''argument : expression'''
    p[0] = p[1]
