"""Register the Tusmo Pygments lexer for fenced code blocks."""

from pygments.lexers import LEXERS

# Pygments loads lexer classes lazily. Import this module while MkDocs has the
# docs directory on sys.path so Pygments can resolve it later in the build.
import tusmo_pygments  # noqa: F401

LEXERS["TusmoLexer"] = (
    "tusmo_pygments",
    "Tusmo",
    ("tusmo", "tus"),
    ("Tusmo language",),
    ("*.tus",),
)
