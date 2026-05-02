import codecs
import re
from compiler.frontend.parser.ast_nodes import (
    ASTNode,
    ClassNode,
    FunctionNode,
    StringNode,
)

_DOCSTRING_PATTERN = re.compile(
    r'(^[ \t]*)(?<!\$)"""(.*?)(?<!\$)"""[ \t]*(?:\r?\n|$)',
    re.DOTALL | re.MULTILINE,
)


def preprocess_docstrings(source: str) -> str:
    """
    No-op: Docstrings are now handled directly by the parser.
    """
    return source


def attach_docstrings(ast):
    """
    Traverse the AST and attach docstring metadata to FunctionNode/ClassNode
    instances. Removes the synthetic StringNode from the body/members so it
    does not generate code. Also attaches preceding string literals to 
    variable declarations (KeydNode, QeexNode, QaabNode).
    """
    if isinstance(ast, list):
        i = 0
        while i < len(ast):
            # Check for a StringNode followed by a declarable node
            if i + 1 < len(ast) and isinstance(ast[i], StringNode):
                next_node = ast[i+1]
                target_types = ('KeydNode', 'QeexNode', 'QaabNode', 'FunctionNode', 'ClassNode')
                if next_node.__class__.__name__ in target_types:
                    next_node.docstring = _unescape_docstring(ast[i].value)
                    ast.pop(i) # Remove the string node from AST
                    continue
            _attach_docstrings(ast[i])
            i += 1
    elif isinstance(ast, ASTNode):
        _attach_docstrings(ast)
    return ast


def _attach_docstrings(node: ASTNode | None):
    if node is None:
        return

    if isinstance(node, FunctionNode):
        if isinstance(node.body, list) and node.body and isinstance(node.body[0], StringNode):
            node.docstring = _unescape_docstring(node.body[0].value)
            node.body = node.body[1:]

    if isinstance(node, ClassNode):
        if getattr(node, "docstring", None) is None:
            members = getattr(node, "members", None)
            if isinstance(members, list) and members and isinstance(members[0], StringNode):
                node.docstring = _unescape_docstring(members[0].value)
                node.members = members[1:]

    for attr_name in dir(node):
        if attr_name.startswith("__"):
            continue
        value = getattr(node, attr_name)
        if isinstance(value, list):
            # Pass the list back to the main function to handle lookaheads
            attach_docstrings(value)
        elif isinstance(value, ASTNode):
            _attach_docstrings(value)


def _unescape_docstring(text: str) -> str:
    try:
        return codecs.decode(text, "unicode_escape")
    except Exception:
        return text
