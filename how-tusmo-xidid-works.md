**TUSMO_XIDID**
Qaabka uu u shaqeynaayo waa fudeed kaliya waxaa loo passayaa pathka faylka tusaale .lib/libtusmo.[a or lib]

tusmo.py compiler driver-keena asiga ayaa ogaanaya nooca syatem ee la isticmaalaya ka dib ayuu goaansanayaa in uu raaciyo dhamaad ka .lib ama .a




# Sidaani waa qaabka dhismeedkeeda


**frontend**
```py
class Xidid(ASTNode):
    '''Xidid waa linker haddhoo ku xiriirin doono c static files-ka uu ugudbin doono gcc-ga'''
    dhamaan_xogta = []
    def __init__(self, aqoonsi):
        self.aqoonsi = aqoonsi
        Xidid.dhamaan_xogta.append(aqoonsi)
```


**Frontend**
```py
from compiler.frontend.parser.ast_nodes import Xidid

def p_tusmo_xidid(p):
    '''statement_return : TUSMO_XIDID STRING SEMICOLON'''
    xidid = p[2]
    if len(p) == 4:
        p[0] = Xidid(xidid)

```

**Backend**
```py
def _unhandled_node(self, node):
        if isinstance(node, ExpressionNode):
            expr_c = self.expr_generator.generate_expression(node)
            self.c_code += f"    {expr_c};\n"
        elif isinstance(node, Xidid):
            pass
```


**Compiler driver tusmo.py**
```py
def get_static_lib():
    flags = []
    for lib in Xidid.dhamaan_xogta:
        file_name = lib
        os_type = platform.system()
        os_name = _platform_key(os_type)

        # Waa inaad variable-ka dib u qeexdaa (re-assign)
        if os_name == "windows":
            if not file_name.endswith(".lib"):
                file_nadef _unhandled_node(self, node):
        if isinstance(node, ExpressionNode):
            expr_c = self.expr_generator.generate_expression(node)
            self.c_code += f"    {expr_c};\n"
        elif isinstance(node, Xidid):
            passme = file_name + ".lib"
        else: # linux ama macos
            if not file_name.endswith(".a"):
                file_name = file_name + ".a"
        
        # Hubi in faylku dhab ahaan u jiro ka hor intaanan ku darin flags
        if os.path.exists(file_name):
            flags.append(f'"{file_name}"')
        else:
            # Haddii uusan jirin waddada tooska ah, isku day inaad ka raadiso .lib/
            alt_path = os.path.join(".lib", file_name)
            if os.path.exists(alt_path):
                flags.append(f'"{alt_path}"')
            else:
                # Haddii wali la waayo, iska daa saas (GCC ayaa error soo saari doona)
                flags.append(f'"{file_name}"')
                
    return " ".join(flags)
```

**tijaaabin**
waxaan abuuray file salaam.c ahaa ka dib waxaan ku qoray 
```c
#include <stdio.h>
void salaam() {
    printf("Salaam  (Hello from Tusmo Lib)\n");
}
```


ka dib waxaan u badalay binary;
```bash
gcc -c salaam.c -o salaam.o
```

ka dib waxaan u badaly static
```bash
ar rcs libtusmo.a salaam.o
```


ka dib waxaan abuuraynaa file tusmo ah kaas oo isticmaalay function-kaaasi ku dhex jira static file ka ee salaam.o

```tus
___c__code_("""

// We tell the program that salaam() exists elsewhere
extern void salaam(); 

""");

___c__call_("salaam");


TUSMO_XIDID ".lib/libtusmo";

```
