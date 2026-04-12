# ast_nodes.py

class ASTNode:
    """
    Kani waa bilowga tree-ga Dhamaan nodes-ka waxay ka farcami donaan tree-gan
    """
    def __init__(self, line=None, filename=None):
        self.line = line
        self.filename = filename

class ExpressionNode(ASTNode):
    """Fasalka aasaasiga ah ee dhammaan 'expressions'. sida : literals, identifiers, binary operations, function calls, iwm."""
    pass

class NumberNode(ExpressionNode):
    """Kani waxa uu matali donaa tiro(int)"""
    def __init__(self, value, line=None, filename=None):
        super().__init__(line, filename)
        self.value = value

class FloatNode(ExpressionNode):
    """Kani waxa uu matali donaa jajab(float)"""
    def __init__(self, value, line=None, filename=None):
        super().__init__(line, filename)
        self.value = value

class StringNode(ExpressionNode):
    """Kani waxa uu matali donaa eray(string)"""
    def __init__(self, value, line=None, filename=None):
        super().__init__(line, filename)
        self.value = value

class CharNode(ExpressionNode):
    """Kani waxa uu matali donaa xaraf(char)"""
    def __init__(self, value, line=None, filename=None):
        super().__init__(line, filename)
        self.value = value

class IdentifierNode(ExpressionNode):
    """Kani waxa uu matali donaa magaca(Identifier) loo bixiyo : variable, function, class, iwm."""   
    def __init__(self, name, line=None, filename=None):
        super().__init__(line, filename)
        self.name = name

class TernaryOpNode(ExpressionNode):
    """Kani waxa uu matali donaa hawlgalka ternary, tusaale ahaan: xalada ? haddii_run_noqoto : haddii_been_noqoto"""
    def __init__(self, condition, if_true, if_false, line=None, filename=None):
        super().__init__(line, filename)
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

class BooleanNode(ExpressionNode):
    """Kani waxa uu matali donaa qiimaha boolean (run ama been)"""
    def __init__(self, value, line=None, filename=None):
        super().__init__(line, filename)
        self.value = value

class BinaryOpNode(ExpressionNode):
    """Kani waxa uu matali donaa hawlgalka binary(sida ku darta, ka jarta iwm), tusaale ahaan: x + y, x * y, iwm."""
    def __init__(self, left, op, right, line=None, filename=None):
        super().__init__(line, filename)
        self.left = left
        self.op = op
        self.right = right
        self.type = "binary_op"

class FStringNode(ExpressionNode):
    """Kani waxa uu matali donaa f-string, oo ah isku darka erayo iyo expressions, tusaale ahaan: f"Magacaygu waa {magac}." """
    def __init__(self, parts, line=None, filename=None):
        super().__init__(line, filename)
        self.parts = parts
        self.type = "fstring"

class TypeLiteralNode(ExpressionNode):
    """Kani waxa uu matali donaa nooc la isticmaalay sida literal, tusaale ahaan: tiro, eray, ama magaca class."""
    def __init__(self, type_name, line=None, filename=None):
        super().__init__(line, filename)
        self.type_name = type_name

class KeydNode(ASTNode):
    """Kani waxa uu matali donaa  keydinta, tusaale ahaan: keyd x: tiro = 5"""
    def __init__(self, var_name, var_type, value, line, filename):
        super().__init__(line, filename)
        self.var_name = var_name
        self.var_type = var_type
        self.value = value

class AssignmentNode(ASTNode):
    """Kani waxa uu matali donaa  qoondeynta, tusaale ahaan: x = 5, ama x += 1"""
    def __init__(self, identifier, op, expression, line, filename):
        super().__init__(line, filename)
        self.identifier = identifier
        self.op = op
        self.expression = expression

class ReturnStatementNode(ASTNode):
    """Kani waxa uu matali donaa  soo celinta, tusaale ahaan: soo celi x + y"""
    def __init__(self, expression, line=None, filename=None):
        super().__init__(line, filename)
        self.expression = expression

class BreakNode(ASTNode):
    """Kani waxa uu matali donaa  'joog' (break)."""
    def __init__(self, line=None, filename=None):
        super().__init__(line, filename)

class ContinueNode(ASTNode):
    """Kani waxa uu matali donaa  'kasoco' (continue)."""
    def __init__(self, line=None, filename=None):
        super().__init__(line, filename)

class EmbeddedCNode(ASTNode):
    """Kani waxa uu matali donaa   ___c__code_  kaas oo xambaar C code"""
    def __init__(self, code, line=None, filename=None):
        super().__init__(line, filename)
        self.code = code

class QorNode(ASTNode):
    """Kani waxa uu matali donaa  'Qor' , tusaale ahaan: qor(x + y)"""
    def __init__(self, line, expressions, filename):
        super().__init__(line, filename)
        self.expressions = expressions

class HelNode(ASTNode):
    """Kani waxa uu matali donaa  'Hel' , tusaale ahaan: hel(x)"""
    def __init__(self, line, identifier, filename, prompt=None):
        super().__init__(line, filename)
        self.identifier = identifier
        self.prompt = prompt

class IfNode(ASTNode):
    """Kani waxa uu matali donaa  'Haddii' , tusaale ahaan: haddii x > 0: qor("x waa positive")"""
    def __init__(self, cases, else_case=None, line=None, filename=None):
        super().__init__(line, filename)
        self.cases = cases
        self.else_case = else_case

class ArrayTypeNode(ASTNode):
    """Kani waxa uu matali donaa nooca array, tusaale ahaan: tix:tiro, ama tix:eray, iwm."""
    def __init__(self, line, element_type=None, filename=None):
        super().__init__(line, filename)
        self.element_type = element_type 

    def __eq__(self, other):
        return (isinstance(other, ArrayTypeNode) and
                self.element_type == other.element_type)

    def __str__(self):
        if isinstance(self.element_type, ArrayTypeNode):
            return f"tix:{str(self.element_type)}"
        elif self.element_type:
            return f"tix:{self.element_type}"
        else:
            return "tix"

    def get_base_type(self):
        if isinstance(self.element_type, ArrayTypeNode):
            return self.element_type.get_base_type()
        return self.element_type

    def get_array_depth(self):
        if isinstance(self.element_type, ArrayTypeNode):
            return 1 + self.element_type.get_array_depth()
        elif self.element_type:
            return 1
        return 0

class FunctionTypeNode(ASTNode):
    """Kani waxa uu matali donaa nooca hawlgalka, tusaale ahaan: hawl(x:tiro, y:eray):eray"""
    def __init__(self, line, param_types, return_type, filename=None):
        super().__init__(line, filename)
        self.param_types = param_types
        self.return_type = return_type

    def __eq__(self, other):
        return (isinstance(other, FunctionTypeNode) and
                self.param_types == other.param_types and
                self.return_type == other.return_type)

    def __str__(self):
        param_str = ', '.join(map(str, self.param_types))
        return f"hawl({param_str}):{self.return_type}"

class ArrayInitializationNode(ExpressionNode):
    """Kani waxa uu matali donaa array bilow ah taas oo leh elements, tusaale ahaan: keyd:tix:tiro = [1, 2, 3]"""
    def __init__(self, line, elements, filename):
        super().__init__(line, filename)
        self.elements = elements

class ArrayAccessNode(ExpressionNode):
    """Kani waxa uu matali donaa helitaanka element ka mid ah array, tusaale ahaan: arr[0]"""
    def __init__(self, line, array_name_node, index_expression, filename):
        super().__init__(line, filename)
        self.array_name_node = array_name_node
        self.index_expression = index_expression

class ArrayTypeQueryNode(ExpressionNode):
    """Kani waxa uu matali donaa nooca gaarka ah ee tix si loo weydiiyo nooca element ee array. tusaale ahaan: nooc(arr[0])"""
    def __init__(self, line, identifier, filename):
        super().__init__(line, filename)
        self.identifier = identifier

class ArrayAssignmentNode(ASTNode):
    """Kani waxa uu matali donaa qoondeynta element ka mid ah array, tusaale ahaan: arr[0] = 10"""
    def __init__(self, line, array_access_node, value_expression, filename):
        super().__init__(line, filename)
        self.array_access_node = array_access_node
        self.value_expression = value_expression

class FunctionNode(ASTNode):
    """Kani waxa uu matali donaa  'Hawl' , tusaale ahaan: hawl isku_dar(x:tiro, y:tiro):tiro { soo celi x + y }"""
    def __init__(self, return_type, name, params, body, line, filename):
        super().__init__(line, filename)
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body
        self.docstring = None

class ParameterNode(ASTNode):
    """Kani waxa uu matali donaa hal parameter ee hawl, tusaale ahaan: x:tiro, ama y:eray = "default" """
    def __init__(self, name, param_type, default_value=None, line=None, filename=None):
        super().__init__(line, filename)
        self.name = name
        self.param_type = param_type
        self.default_value = default_value

class NamedArgument(ASTNode):
    """Kani waxa uu matali donaa hal argument oo magac leh ee loo gudbiyo hawl, tusaale ahaan: x=5, ama y="hello" """
    def __init__(self, name, value, line=None, filename=None):
        super().__init__(line, filename)
        self.name = name
        self.value = value

class FunctionCallNode(ExpressionNode):
    """Kani waxa uu matali donaa wicitaanka hawl, tusaale ahaan: isku_dar(5, 10), ama isku_dar(x=5, y=10)"""
    def __init__(self, name, params, line, filename):
        super().__init__(line, filename)
        self.name = name
        self.params = params
        self.ordered_args = None

class WhileNode(ASTNode):
    """Kani waxa uu matali donaa  'inta ay' , tusaale ahaan: inta ay x < 10 { qor(x); x += 1 }"""
    def __init__(self, line, condition, body, filename):
        super().__init__(line, filename)
        self.condition = condition
        self.body = body

class DoWhileNode(ASTNode):
    """Kani waxa uu matali donaa  'samee...inta ay' , tusaale ahaan: samee { qor(x); x += 1 } inta ay x < 10"""
    def __init__(self, line, body, condition, filename):
        super().__init__(line, filename)
        self.body = body
        self.condition = condition

class ForRangeNode(ASTNode):
    """Kani waxa uu matali donaa  'soco identifier laga bilaawo' oo leh xadka, tusaale ahaan: soco i laga bilaabo 0..10 { qor(i) }"""
    def __init__(self, line, iterator_var_name, start_expr, end_expr, body, filename):
        super().__init__(line, filename)
        self.iterator_var_name = iterator_var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body

class ForEachNode(ASTNode):
    """Kani waxa uu matali donaa  'soco identifier kasta laga helo' oo leh array, tusaale ahaan: soco item kasta laga helo arr { qor(item) }"""
    def __init__(self, line, iterator_var_name, array_expr, body, filename):
        super().__init__(line, filename)
        self.iterator_var_name = iterator_var_name
        self.array_expr = array_expr
        self.body = body

class MethodCallNode(ExpressionNode):
    """Kani waxa uu matali donaa wicitaanka method ee object, tusaale ahaan: qof1.magac(), ama qof1.magac(x=5)"""
    def __init__(self, line, object_node, method_name, args_list, filename):
        super().__init__(line, filename)
        self.object_node = object_node
        self.method_name = method_name
        self.args_list = args_list
        self.ordered_args = None

class KeenNode(ASTNode):
    """Kani waxa uu matali donaa keenista module kale oo dhameystiran, tusaale ahaan: keen math"""
    def __init__(self, line, filename_to_import, source_filename):
        super().__init__(line, source_filename)
        self.filename = filename_to_import

    def __str__(self):
        return f"keen: {self.filename}"

class IsticmaalNode(ASTNode):
    """Kani waxa uu matali donaa keenista module qeybo ka mid ah, tusaale ahaan: isticmaal {iskudar, kalajar} kujira math"""
    def __init__(self, line, names_to_import, filename_to_import, source_filename):
        super().__init__(line, source_filename)
        self.names = names_to_import
        self.module = filename_to_import

    def __str__(self):
        return f"isticmaal: {self.names} kujira {self.module}"

class ClassNode(ASTNode):
    """Kani waxa uu matali donaa  'Koox' , tusaale ahaan: Koox Qof {  }"""
    def __init__(self, name, members, methods, line, filename, parent_name=None):
        super().__init__(line, filename)
        self.name = name
        self.members = members
        self.methods = methods
        self.docstring = None
        self.parent_name = parent_name

class ClassInstantiationNode(ExpressionNode):
    """Kani waxa uu matali donaa abuurista object cusub oo ka mid ah class, tusaale ahaan: keyd:Qof qof1 = Qof() cusub;"""
    def __init__(self, class_name, constructor_args, line, filename):
        super().__init__(line, filename)
        self.class_name = class_name
        self.constructor_args = constructor_args
        self.ordered_args = None

class MemberAccessNode(ExpressionNode):
    """Kani waxa uu matali donaa helitaanka member ka mid ah object, tusaale ahaan: qof1.magac, ama qof1.magac = "Ali" """
    def __init__(self, object_node, member_name, line, filename):
        super().__init__(line, filename)
        self.object_node = object_node
        self.member_name = member_name

class ThisNode(ExpressionNode):
    """Kani waxa uu matali donaa  keyword-ka 'kan'  ee laga isticmaalo gudaha class si loo sameeyo tixraacyo """
    def __init__(self, line, filename):
        super().__init__(line, filename)

class WaalidNode(ExpressionNode):
    """Kani waxa uu matali donaa  keyword-ka 'waalid'  ee laga isticmaalo gudaha class si loo sameeyo tixraaca lagu dhaxlayo class kale"""
    def __init__(self, line, filename):
        super().__init__(line, filename)

class CCallNode(ExpressionNode):
    """Kani waxa uu matali donaa wicitaanka hawlaha ku qoran luuqada C, tusaale ahaan: __c__code__ printf("Hello, World!"); """
    def __init__(self, c_function_name, args, line, filename):
        super().__init__(line, filename)
        self.c_function_name = c_function_name
        self.args = args

    def __repr__(self):
        return f"CCallNode({self.c_function_name}, {self.args})"

class DictionaryInitializationNode(ExpressionNode):
    """Kani waxa uu matali donaa dictionary(qaamuus), tusaale ahaan: {"magac": "Ali", "da": 25}."""
    def __init__(self, line, pairs, filename):
        super().__init__(line, filename)
        self.pairs = pairs

class DictionaryAccessNode(ExpressionNode):
    """Kani waxa uu matali donaa helitaanka dictionary, tusaale ahaan: my_dict["key"]."""
    def __init__(self, line, dictionary_node, key_node, filename):
        super().__init__(line, filename)
        self.dictionary_node = dictionary_node
        self.key_node = key_node

class DictionaryAssignmentNode(ASTNode):
    """Kani waxa uu matali donaa qoondeynta dictionary, tusaale ahaan: my_dict["key"] = value."""
    def __init__(self, line, dictionary_access_node, value_node, filename):
        super().__init__(line, filename)
        self.dictionary_access_node = dictionary_access_node
        self.value_node = value_node
