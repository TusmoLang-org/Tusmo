import ply.yacc as yacc
import sys
from compiler.frontend.lexer.lexer import tokens, lexer
from compiler.frontend.parser.grammar_rules import *



def p_error(p):
    if p:
        filename = getattr(p.lexer, 'filename', '<fayl aan la aqoon>')
        print(f"\n\033[1;31m[!] KHALAD NAXWE:\033[0m Erayga \033[1;31m'{p.value}'\033[0m lama aqoonsana halkan!")
        print(f"\033[90m" + ("-" * 45) + "\033[0m")
        print(f"\033[94mFaylka:\033[0m   {filename}")
        print(f"\033[94mSaddarka:\033[0m {p.lineno}")
        print(f"\033[1;35m// Naxwahaaga dib u eeg! '{p.value}' booskan ma qabanayo.\033[0m\n")
        sys.exit(1)
    else:
        filename = getattr(lexer, 'filename', '<fayl aan la aqoon>')
        print(f"\n\033[1;31m[!] KHALAD NAXWE:\033[0m Waxaa laga helay dhammaadka faylka \033[1;31m'{filename}'\033[0m meel aan laga filayn!")
        print(f"\033[90m" + ("-" * 45) + "\033[0m")
        print(f"\033[1;35m// Ma koodkaad kala bartay ka tagtay? Soo dhammaystir koodkaaga.\033[0m\n")
        sys.exit(1)

parser = yacc.yacc(debug=True)