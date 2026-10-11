"""
tusmo_lexer.py – Custom Pygments lexer for the Tusmo programming language.
Place this file in the root of the Tusmo repo and reference it in mkdocs.yml.
"""
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import (
    Text, Comment, Operator, Keyword, Name, String,
    Number, Punctuation, Literal
)


class TusmoLexer(RegexLexer):
    name = "Tusmo"
    aliases = ["tusmo", "tus"]
    filenames = ["*.tus"]

    KEYWORDS_CONTROL = (
        "haddii", "ama_haddii", "haddii_kale",
        "inta", "samay", "soco", "joog", "kasoco",
        "kasta", "laga", "bilaabo", "ay", "helo", "ee",
        "soo_celi",
    )
    KEYWORDS_DECL = (
        "keyd", "hawl", "shaqo", "koox", "qaab", "qeex",
        "dhis", "burbur", "cusub", "dhaxlaya", "waalid", "kan",
    )
    KEYWORDS_IMPORT = ("keen", "isticmaal", "kujira")

    TYPES = (
        "tiro", "jajab", "eray", "xaraf", "miyaa",
        "waxbo", "walbo", "tix", "qaamuus", "tix_cayiman",
    )
    BUILTINS = (
        "hel", "qor", "show", "gali", "nooc", "dherer",
        "tix_cayiman", "majiraa", "tir", "XarafWeyn", "XarafYar",
        "kaReeb", "Bkareeb", "Mkareeb", "kuBadal", "sooRaadi",
        "lagaHelay", "qaybi", "nasiib_tiro", "nasiib_jajab",
        "bilaaw_nasiib", "iguYar", "uguWeyn", "qaado", "jooji",
        "saacadda", "sug",
    )
    BOOLEANS = ("run", "haa", "been", "maya")
    OPERATORS_WORD = (
        "lamid_maaha", "lamid", "weyn_lamid", "yar_lamid",
        "weyn", "yar", "iyo", "ama", "ahayn",
    )

    tokens = {
        "root": [
            # Comments
            (r"//.*?$", Comment.Single),
            (r"/\*", Comment.Multiline, "comment"),

            # Triple-quoted strings
            (r'"""', String, "triple_string"),

            # F-strings
            (r'\$"', String.Interpol, "fstring"),

            # Regular strings
            (r'"', String.Double, "string_double"),
            (r"'", String.Char, "string_single"),

            # Numbers
            (r"\b0[xX][0-9a-fA-F]+\b", Number.Hex),
            (r"\b\d+\.\d+\b", Number.Float),
            (r"\b\d+\b", Number.Integer),

            # Keywords
            (words(KEYWORDS_CONTROL, prefix=r"\b", suffix=r"\b"), Keyword.Reserved),
            (words(KEYWORDS_DECL,    prefix=r"\b", suffix=r"\b"), Keyword.Declaration),
            (words(KEYWORDS_IMPORT,  prefix=r"\b", suffix=r"\b"), Keyword.Namespace),

            # Types
            (words(TYPES,     prefix=r"\b", suffix=r"\b"), Keyword.Type),

            # Booleans
            (words(BOOLEANS,  prefix=r"\b", suffix=r"\b"), Keyword.Constant),

            # Word operators
            (words(OPERATORS_WORD, prefix=r"\b", suffix=r"\b"), Operator.Word),

            # Built-in functions
            (words(BUILTINS,  prefix=r"\b", suffix=r"\b"), Name.Builtin),

            # Function definitions: hawl name(
            (r"(?<=\bhawl\s)([a-zA-Z_]\w*)", Name.Function),

            # Class / struct names
            (r"(?<=\bkoox\s)([A-Z][a-zA-Z0-9_]*)", Name.Class),
            (r"(?<=\bqaab\s)([A-Z][a-zA-Z0-9_]*)", Name.Class),

            # Generic function calls
            (r"\b([a-zA-Z_]\w*)(?=\s*\()", Name.Function),

            # Symbols & operators
            (r"=>",      Operator),
            (r"\.\.",    Operator),
            (r"==|!=|>=|<=|>|<", Operator),
            (r"[+\-*/%]", Operator),
            (r"=",       Operator),
            (r"[(){}\[\],;:.]", Punctuation),

            # Identifiers
            (r"[a-zA-Z_]\w*", Name),

            # Whitespace
            (r"\s+", Text),
        ],

        "comment": [
            (r"[^*/]+", Comment.Multiline),
            (r"\*/",    Comment.Multiline, "#pop"),
            (r"[*/]",   Comment.Multiline),
        ],

        "triple_string": [
            (r'"""',    String, "#pop"),
            (r"\\.",    String.Escape),
            (r'[^"\\]+', String),
            (r'"',      String),
        ],

        "fstring": [
            (r'"',      String.Interpol, "#pop"),
            (r"\{",     Punctuation, "fstring_interp"),
            (r"\\.",    String.Escape),
            (r'[^"\\{]+', String.Interpol),
        ],

        "fstring_interp": [
            (r"\}",     Punctuation, "#pop"),
            (r"[^}]+",  Name),
        ],

        "string_double": [
            (r'"',      String.Double, "#pop"),
            (r"\\.",    String.Escape),
            (r'[^"\\]+', String.Double),
        ],

        "string_single": [
            (r"'",      String.Char, "#pop"),
            (r"\\.",    String.Escape),
            (r"[^'\\]+", String.Char),
        ],
    }
