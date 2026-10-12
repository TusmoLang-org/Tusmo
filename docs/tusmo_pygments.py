"""Pygments lexer for Tusmo examples in the documentation."""

from pygments.lexer import RegexLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text


class TusmoLexer(RegexLexer):
    name = "Tusmo"
    aliases = ["tusmo", "tus"]
    filenames = ["*.tus"]

    tokens = {
        "root": [
            (r"\s+", Text),
            (r"//.*?$|#.*?$", Comment.Single),
            (r"/\*[\s\S]*?\*/", Comment.Multiline),
            (r'"""[\s\S]*?"""', String.Doc),
            (r"'''[\s\S]*?'''", String.Doc),
            (r'f"(?:[^"\\]|\\.|\{[^}]*\})*"', String.Interpol),
            (r'"(?:[^"\\]|\\.)*"', String.Double),
            (r"'(?:[^'\\]|\\.)*'", String.Single),
            (
                r"\b(?:ama_haddii|haddii_kale|tix_cayiman|isticmaal|kujira|dhaxlaya|"
                r"bilaabo|kasoco|burbur|haddii|hawl|shaqo|inta|samay|soco|laga|kasta|"
                r"helo|joog|ahayn|lamid|koox|cusub|dhis|gali|keen|qeex|qaab|waalid|"
                r"miyaa|iyo|ama|ee|ay|kan)\b",
                Keyword,
            ),
            (
                r"\b(?:keyd|tiro|eray|xaraf|jajab|tix|qaamuus|waxbo)\b",
                Keyword.Type,
            ),
            (r"\b(?:run|haa|been|maya)\b", Keyword.Constant),
            (
                r"\b(?:qor|hel|soo_celi|kuBadal|kaReeb|Bkareeb|Mkareeb|XarafWeyn|"
                r"XarafYar|sooRaadi|lagaHelay|qaybi)\b",
                Name.Builtin,
            ),
            (r"\b[A-Z_][A-Z0-9_]*\b", Name.Constant),
            (r"\b\d+(?:\.\d+)?\b", Number),
            (r"[A-Za-z_]\w*(?=\s*\()", Name.Function),
            (r"[A-Za-z_]\w*", Name),
            (r"===|==|!=|>=|<=|=>|->|\+=|-=|\*=|/=|&&|\|\||[+*/%=<>!&|?-]", Operator),
            (r"[{}()\[\];,:.]", Punctuation),
            (r".", Text),
        ]
    }


__all__ = ["TusmoLexer"]
