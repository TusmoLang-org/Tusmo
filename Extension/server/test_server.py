import sys
import types
import unittest
from pathlib import Path

# --- Masterclass LSP/Pygls Mocking ---
# This interceptor dynamically injects mock lsprotocol/pygls modules
# into sys.modules so the LSP server can be tested offline without pip installs.

class DummyObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    def __repr__(self):
        return f"DummyObject({self.__dict__})"

lsprotocol_types = types.ModuleType("lsprotocol.types")
sys.modules["lsprotocol.types"] = lsprotocol_types

lsprotocol_types.DidChangeTextDocumentParams = DummyObject
lsprotocol_types.DidCloseTextDocumentParams = DummyObject
lsprotocol_types.DidOpenTextDocumentParams = DummyObject
lsprotocol_types.Hover = DummyObject
lsprotocol_types.HoverParams = DummyObject
lsprotocol_types.MarkupContent = DummyObject

class MockMarkupKind:
    Markdown = "markdown"
    Plaintext = "plaintext"

lsprotocol_types.MarkupKind = MockMarkupKind
lsprotocol_types.CompletionParams = DummyObject
lsprotocol_types.CompletionList = DummyObject
lsprotocol_types.CompletionItem = DummyObject

class MockCompletionItemKind:
    Keyword = "Keyword"
    Constant = "Constant"
    TypeParameter = "TypeParameter"
    Function = "Function"
    Class = "Class"
    Method = "Method"
    Variable = "Variable"
    Property = "Property"

lsprotocol_types.CompletionItemKind = MockCompletionItemKind
lsprotocol_types.Location = DummyObject
lsprotocol_types.Position = DummyObject
lsprotocol_types.Range = DummyObject
lsprotocol_types.DefinitionParams = DummyObject
lsprotocol_types.DocumentSymbolParams = DummyObject
lsprotocol_types.DocumentSymbol = DummyObject

class MockSymbolKind:
    Class = "Class"
    Method = "Method"
    Function = "Function"
    Variable = "Variable"
    Constant = "Constant"
    Property = "Property"

lsprotocol_types.SymbolKind = MockSymbolKind
lsprotocol_types.Diagnostic = DummyObject

class MockDiagnosticSeverity:
    Error = "Error"

lsprotocol_types.DiagnosticSeverity = MockDiagnosticSeverity

# Mock pygls.lsp.server
pygls_lsp_server = types.ModuleType("pygls.lsp.server")
sys.modules["pygls.lsp.server"] = pygls_lsp_server

class MockLanguageServerBase:
    def __init__(self, name=None, version=None):
        self.name = name
        self.version = version
        self.features = {}

    def feature(self, name):
        def decorator(func):
            # Track registered feature handlers
            self.features[name] = func
            return func
        return decorator

pygls_lsp_server.LanguageServer = MockLanguageServerBase

# Add root folder to sys.path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from compiler.midend.docstring_index import (
    build_doc_index,
    build_doc_index_with_imports,
    DocEntry,
    IMPORT_CACHE
)
from Extension.server.tusmo_hover_server import (
    TusmoLanguageServer,
    completions,
    definition,
    document_symbols,
    _refresh_index
)

class MockWorkspace:
    def __init__(self):
        self._docs = {}

    def get_text_document(self, uri):
        return self._docs.get(uri)

    def put_text_document(self, uri, doc):
        self._docs[uri] = doc

class MockTextDocument:
    def __init__(self, uri, source):
        self.uri = uri
        self.source = source
        self.path = uri.replace("file://", "")

class MockLanguageServer(TusmoLanguageServer):
    def __init__(self):
        super().__init__()
        self.workspace = MockWorkspace()
        self.published_diagnostics = {}

    def publish_diagnostics(self, uri, diagnostics):
        self.published_diagnostics[uri] = diagnostics


class TestTusmoLsp(unittest.TestCase):

    def test_doc_entry_coordinates(self):
        """Verify that parsed AST nodes save coordinates into DocEntry."""
        source = """
koox Xisaab {
    "Kani waa kooxda xisaabta."
    
    hawl dar(e: tiro, b: tiro): tiro {
        "Waxay isku darta e iyo b."
        soo_celi e + b;
    }
}
"""
        index = build_doc_index(source, "tijaabo.tus")
        
        # Verify koox coordinate
        xisaab_entries = index.lookup("Xisaab")
        self.assertTrue(len(xisaab_entries) > 0)
        self.assertEqual(xisaab_entries[0].filename, "tijaabo.tus")
        self.assertEqual(xisaab_entries[0].line, 2)
        
        # Verify method coordinate
        dar_entries = index.lookup("Xisaab.dar")
        self.assertTrue(len(dar_entries) > 0)
        self.assertEqual(dar_entries[0].filename, "tijaabo.tus")
        self.assertEqual(dar_entries[0].line, 5)

    def test_import_caching(self):
        """Verify mtime-based import caching mechanism."""
        IMPORT_CACHE.clear()
        
        dummy_file = Path("tijaabo_cache.tus")
        dummy_file.write_text("""
hawl salaam(): waxbo {
    "Waxay tiraahdaa salaam."
    qor("Salaam dunida!");
}
""", encoding="utf-8")
        
        try:
            source = f'keen "{dummy_file.name}";'
            # Build first time (will parse and cache)
            index1 = build_doc_index_with_imports(source, str(Path("main.tus").resolve()))
            
            # Retrieve cached entry
            resolved_str = str(dummy_file.resolve())
            self.assertIn(resolved_str, IMPORT_CACHE)
            
            # Build second time (must load from cache)
            index2 = build_doc_index_with_imports(source, str(Path("main.tus").resolve()))
            
            # Check cached entries match
            self.assertEqual(len(index1.lookup("salaam")), len(index2.lookup("salaam")))
        finally:
            if dummy_file.exists():
                dummy_file.unlink()

    def test_lsp_completion(self):
        """Verify LSP completion returns static keywords/builtins + dynamic symbols."""
        ls = MockLanguageServer()
        uri = "file:///mock.tus"
        source = """
hawl tijaabo(): waxbo {
    "Tijaabo."
}
"""
        doc = MockTextDocument(uri, source)
        ls.workspace.put_text_document(uri, doc)
        
        _refresh_index(ls, uri)
        
        params = DummyObject(
            text_document=DummyObject(uri=uri),
            position=DummyObject(line=0, character=0)
        )
        res = completions(ls, params)
        self.assertIsNotNone(res)
        
        labels = [item.label for item in res.items]
        # Must contain keyword 'hawl'
        self.assertIn("hawl", labels)
        # Must contain builtin 'qor'
        self.assertIn("qor", labels)
        # Must contain parsed function 'tijaabo'
        self.assertIn("tijaabo", labels)

    def test_lsp_definition(self):
        """Verify LSP definition returns correct Location coordinates."""
        ls = MockLanguageServer()
        uri = "file:///mock_def.tus"
        source = """
hawl target_func(): waxbo {
    "Hawsha la raadinayo."
}

target_func();
"""
        doc = MockTextDocument(uri, source)
        ls.workspace.put_text_document(uri, doc)
        
        _refresh_index(ls, uri)
        
        # Call definition at line 5 (0-indexed line 5, which contains target_func call)
        params = DummyObject(
            text_document=DummyObject(uri=uri),
            position=DummyObject(line=5, character=5)
        )
        res = definition(ls, params)
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].range.start.line, 1) # target_func defined at line 2 (0-indexed line 1)

    def test_lsp_document_symbols(self):
        """Verify LSP document symbols return outline entries for current file."""
        ls = MockLanguageServer()
        uri = "file:///mock_symbols.tus"
        source = """
koox X {
    "Koox."
}
"""
        doc = MockTextDocument(uri, source)
        ls.workspace.put_text_document(uri, doc)
        
        _refresh_index(ls, uri)
        
        params = DummyObject(
            text_document=DummyObject(uri=uri)
        )
        res = document_symbols(ls, params)
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name, "X")

    def test_lsp_diagnostics(self):
        """Verify real-time diagnostics on syntax errors."""
        ls = MockLanguageServer()
        uri = "file:///mock_err.tus"
        # Invalid syntax: missing bracket
        source = """
hawl khaldan( : tiro {
    soo_celi 5;
}
"""
        doc = MockTextDocument(uri, source)
        ls.workspace.put_text_document(uri, doc)
        
        _refresh_index(ls, uri)
        
        diags = ls.published_diagnostics.get(uri)
        self.assertIsNotNone(diags)
        self.assertTrue(len(diags) > 0)
        self.assertIn("KHALAD", diags[0].message.upper() or "ERROR")


if __name__ == "__main__":
    unittest.main()
