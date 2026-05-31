import argparse
import logging
import re
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from lsprotocol.types import (
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    Hover,
    HoverParams,
    MarkupContent,
    MarkupKind,
    CompletionParams,
    CompletionList,
    CompletionItem,
    CompletionItemKind,
    Location,
    Position,
    Range,
    DefinitionParams,
    DocumentSymbolParams,
    DocumentSymbol,
    SymbolKind,
    Diagnostic,
    DiagnosticSeverity,
)
from pygls.lsp.server import LanguageServer

from compiler.midend.docstring_index import (
    DocEntry,
    DocstringIndex,
    build_doc_index,
    build_doc_index_with_imports,
)

LOGGER = logging.getLogger("tusmo.hover")

TEXT_DOCUMENT_DID_OPEN = "textDocument/didOpen"
TEXT_DOCUMENT_DID_CHANGE = "textDocument/didChange"
TEXT_DOCUMENT_DID_CLOSE = "textDocument/didClose"
HOVER = "textDocument/hover"
TEXT_DOCUMENT_COMPLETION = "textDocument/completion"
TEXT_DOCUMENT_DEFINITION = "textDocument/definition"
TEXT_DOCUMENT_DOCUMENT_SYMBOL = "textDocument/documentSymbol"

KEYWORDS = [
    ("keyd", "keyd : ku dhawaaq dooriye/variable", CompletionItemKind.Keyword),
    ("hawl", "hawl : qeex shaqo/function ama hab-socod/method", CompletionItemKind.Keyword),
    ("soo_celi", "soo_celi : soo celi qiimo", CompletionItemKind.Keyword),
    ("haddii", "haddii : haddii xaaladi run tahay", CompletionItemKind.Keyword),
    ("ama_haddii", "ama_haddii : haddii kale haddii xaalad kale run tahay", CompletionItemKind.Keyword),
    ("haddii_kale", "haddii_kale : haddii kale", CompletionItemKind.Keyword),
    ("inta", "inta : ku celcelin ilaa xaaladi been ka noqoto", CompletionItemKind.Keyword),
    ("samay", "samay : samee hawl loop dhexdiisa", CompletionItemKind.Keyword),
    ("soco", "soco : u gudub wareegga xiga ee loop-ka", CompletionItemKind.Keyword),
    ("joog", "joog : ka bax loop-ka gabi ahaanba", CompletionItemKind.Keyword),
    ("kasta", "kasta : for-each loop si loogu dul maro tix", CompletionItemKind.Keyword),
    ("helo", "helo : ka helo walxaha tixda", CompletionItemKind.Keyword),
    ("laga", "laga : bilowga tirada loop-ka kasta", CompletionItemKind.Keyword),
    ("bilaabo", "bilaabo : bilaabida tirada loop-ka", CompletionItemKind.Keyword),
    ("ay", "ay : ku xidhidda loop-ka", CompletionItemKind.Keyword),
    ("kasoco", "kasoco : sii soco wareegga loop-ka", CompletionItemKind.Keyword),
    ("dhaxlaya", "dhaxlaya : koox dhaxlaysa koox kale", CompletionItemKind.Keyword),
    ("waalid", "waalid : u wacida dhisaha/habka kooxda waalidka", CompletionItemKind.Keyword),
    ("kan", "kan : tilmaamaha shayga hadda taagan (self/this)", CompletionItemKind.Keyword),
    ("koox", "koox : qeexida koox (class)", CompletionItemKind.Keyword),
    ("qaab", "qaab : qeexida qaabdhismeed (struct)", CompletionItemKind.Keyword),
    ("qeex", "qeex : qeexida joogto (constant)", CompletionItemKind.Keyword),
    ("cusub", "cusub : abuurista shay cusub oo koox ah", CompletionItemKind.Keyword),
    ("isticmaal", "isticmaal : soo dhoofsasho qayb ka mid ah fayl", CompletionItemKind.Keyword),
    ("keen", "keen : soo dhoofsasho buuxda oo fayl", CompletionItemKind.Keyword),
    ("ee", "ee : loo isticmaalo loop-yada ama qaabab kale", CompletionItemKind.Keyword),
    ("run", "run : qiimaha runta (boolean true)", CompletionItemKind.Constant),
    ("been", "been : qiimaha been (boolean false)", CompletionItemKind.Constant),
    ("haa", "haa : qiimaha haa (boolean true)", CompletionItemKind.Constant),
    ("maya", "maya : qiimaha maya (boolean false)", CompletionItemKind.Constant),
    ("tiro", "tiro : nooca xogta ee int (integer)", CompletionItemKind.TypeParameter),
    ("eray", "eray : nooca xogta ee string", CompletionItemKind.TypeParameter),
    ("jajab", "jajab : nooca xogta ee float", CompletionItemKind.TypeParameter),
    ("miyaa", "miyaa : nooca xogta ee bool (boolean)", CompletionItemKind.TypeParameter),
    ("xaraf", "xaraf : nooca xogta ee char", CompletionItemKind.TypeParameter),
    ("tix", "tix : nooca xogta ee list (array)", CompletionItemKind.TypeParameter),
    ("qaamuus", "qaamuus : nooca xogta ee dictionary (map)", CompletionItemKind.TypeParameter),
    ("walbo", "walbo : nooca xogta ee dynamic/wildcard", CompletionItemKind.TypeParameter),
    ("waxbo", "waxbo : nooca xogta ee void (empty)", CompletionItemKind.TypeParameter),
]

BUILTINS = [
    ("qor", "hawl qor(...) : daabac macluumaad", CompletionItemKind.Function, "qor(*arguments) : Waxay ku daabacdaa shaashada qiyam kasta."),
    ("gali", "hawl gali(tix, qiimo) : ku dar walax tixda", CompletionItemKind.Function, "gali(tix, qiimo) : Waxay ku dartaa qiimo dhamaadka tixda."),
    ("kasaar", "hawl kasaar(tix, index) : ka saar walax tixda", CompletionItemKind.Function, "kasaar(tix, index) : Waxay ka saartaa walax tixda iyadoo la adeegsanayo index-ka."),
    ("dherer", "hawl dherer(x) : soo celi dhererka", CompletionItemKind.Function, "dherer(x) : Waxay soo celisaa dhererka tixda ama erayga."),
    ("nooc", "hawl nooc(x) : soo celi nooca dooriyaha", CompletionItemKind.Function, "nooc(x) : Waxay soo celisaa magaca nooca dooriyaha ee eray ahaan."),
]


class TusmoLanguageServer(LanguageServer):
    """A minimal hover-focused language server for Tusmo sources."""

    def __init__(self) -> None:
        super().__init__("tusmo-hover-server", "0.1.0")
        self.doc_indices: dict[str, DocstringIndex] = {}


server = TusmoLanguageServer()


@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: TusmoLanguageServer, params: DidOpenTextDocumentParams) -> None:
    _refresh_index(ls, params.text_document.uri)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: TusmoLanguageServer, params: DidChangeTextDocumentParams) -> None:
    _refresh_index(ls, params.text_document.uri)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls: TusmoLanguageServer, params: DidCloseTextDocumentParams) -> None:
    ls.doc_indices.pop(params.text_document.uri, None)


@server.feature(HOVER)
def hover(ls: TusmoLanguageServer, params: HoverParams) -> Optional[Hover]:
    document = ls.workspace.get_text_document(params.text_document.uri)
    if not document:
        return None

    line = _get_line(document.source, params.position.line)
    if line is None:
        return None

    symbol, qualified_symbol = _extract_symbol(line, params.position.character)
    if not symbol:
        return None

    doc_index = ls.doc_indices.get(params.text_document.uri)
    if not doc_index:
        return None

    entries: list[DocEntry] = []
    if qualified_symbol:
        entries = doc_index.lookup(qualified_symbol)
    if not entries:
        entries = doc_index.lookup(symbol)
    if not entries:
        return None

    markdown = _format_entries(entries)
    return Hover(contents=MarkupContent(kind=MarkupKind.Markdown, value=markdown))


@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(ls: TusmoLanguageServer, params: CompletionParams) -> Optional[CompletionList]:
    items = []

    # 1. Add static keywords
    for kw, desc, kind in KEYWORDS:
        items.append(
            CompletionItem(
                label=kw,
                kind=kind,
                detail=desc,
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**Erayga Furaha:** `{kw}`\n\n{desc}"
                )
            )
        )

    # 2. Add static built-ins
    for name, signature, kind, doc in BUILTINS:
        items.append(
            CompletionItem(
                label=name,
                kind=kind,
                detail=signature,
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**Hawsha Dhex-dhisan:** `{name}`\n\n{doc}"
                )
            )
        )

    # 3. Add dynamic parsed symbols from index
    doc_index = ls.doc_indices.get(params.text_document.uri)
    if doc_index:
        for symbol_name, entries in doc_index.items():
            if not entries:
                continue
            entry = entries[0] 
            
            kind = CompletionItemKind.Function
            if entry.kind == "class" or entry.kind == "qaab":
                kind = CompletionItemKind.Class
            elif entry.kind == "method":
                kind = CompletionItemKind.Method
            elif entry.kind == "variable":
                kind = CompletionItemKind.Variable
            elif entry.kind == "constant":
                kind = CompletionItemKind.Constant
            elif entry.kind == "property":
                kind = CompletionItemKind.Property
                
            item = CompletionItem(
                label=symbol_name,
                kind=kind,
                detail=entry.signature if entry.signature else entry.kind,
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown, 
                    value=_render_docstring(entry.docstring)
                )
            )
            items.append(item)
        
    return CompletionList(is_incomplete=False, items=items)


@server.feature(TEXT_DOCUMENT_DEFINITION)
def definition(ls: TusmoLanguageServer, params: DefinitionParams) -> Optional[list[Location]]:
    document = ls.workspace.get_text_document(params.text_document.uri)
    if not document:
        return None

    line = _get_line(document.source, params.position.line)
    if line is None:
        return None

    symbol, qualified_symbol = _extract_symbol(line, params.position.character)
    if not symbol:
        return None

    doc_index = ls.doc_indices.get(params.text_document.uri)
    if not doc_index:
        return None

    entries: list[DocEntry] = []
    if qualified_symbol:
        entries = doc_index.lookup(qualified_symbol)
    if not entries:
        entries = doc_index.lookup(symbol)
    if not entries:
        return None

    locations = []
    for entry in entries:
        if entry.filename and entry.line is not None:
            line_idx = max(0, entry.line - 1)
            try:
                uri = Path(entry.filename).resolve().as_uri()
            except Exception:
                uri = f"file://{entry.filename}"
            
            loc = Location(
                uri=uri,
                range=Range(
                    start=Position(line=line_idx, character=0),
                    end=Position(line=line_idx, character=999)
                )
            )
            locations.append(loc)

    return locations if locations else None


@server.feature(TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def document_symbols(ls: TusmoLanguageServer, params: DocumentSymbolParams) -> Optional[list[DocumentSymbol]]:
    doc_index = ls.doc_indices.get(params.text_document.uri)
    if not doc_index:
        return None

    symbols = []
    document = ls.workspace.get_text_document(params.text_document.uri)
    if not document:
        return None

    doc_path = _to_path(document.path or params.text_document.uri)
    if not doc_path:
        return None

    for symbol_name, entries in doc_index.items():
        if not entries:
            continue
        entry = entries[0]
        
        # Only show symbols defined in the current file to prevent outline pollution
        entry_path = _to_path(entry.filename) if entry.filename else None
        if not entry_path or doc_path.resolve() != entry_path.resolve():
            continue

        # Avoid showing qualified names (e.g. show `add` instead of `Calculator.add`)
        if "." in symbol_name:
            continue

        kind = SymbolKind.Function
        if entry.kind == "class" or entry.kind == "qaab":
            kind = SymbolKind.Class
        elif entry.kind == "method":
            kind = SymbolKind.Method
        elif entry.kind == "variable":
            kind = SymbolKind.Variable
        elif entry.kind == "constant":
            kind = SymbolKind.Constant
        elif entry.kind == "property":
            kind = SymbolKind.Property

        line_idx = max(0, (entry.line - 1) if entry.line is not None else 0)
        sym_range = Range(
            start=Position(line=line_idx, character=0),
            end=Position(line=line_idx, character=999)
        )
        
        symbol_obj = DocumentSymbol(
            name=symbol_name,
            kind=kind,
            range=sym_range,
            selection_range=sym_range,
            detail=entry.signature if entry.signature else entry.kind
        )
        symbols.append(symbol_obj)

    return symbols if symbols else None


def _refresh_index(ls: TusmoLanguageServer, uri: str) -> None:
    document = ls.workspace.get_text_document(uri)
    if not document:
        return

    filename = document.path or uri
    file_path = _to_path(filename)
    search_roots = _determine_search_roots(ls, file_path)
    try:
        if file_path:
            index = build_doc_index_with_imports(
                document.source,
                str(file_path),
                extra_search_roots=search_roots,
            )
        else:
            index = build_doc_index(document.source, filename)
    except Exception:  # pragma: no cover - defensive
        LOGGER.exception("Failed to build docstring index for %s", filename)
        return

    # 1. Publish Diagnostics (real-time error reporting)
    diagnostics = []
    if index.error_message:
        line_num = 0
        match = re.search(r'(?:Saddarka:|line|Line)\s*(\d+)', index.error_message)
        if match:
            line_num = max(0, int(match.group(1)) - 1)
            
        diag = Diagnostic(
            range=Range(
                start=Position(line=line_num, character=0),
                end=Position(line=line_num, character=999)
            ),
            message=index.error_message,
            source="Tusmo",
            severity=DiagnosticSeverity.Error
        )
        diagnostics.append(diag)
        
    ls.publish_diagnostics(uri, diagnostics)

    # 2. Update doc index or early-return to keep old index if new index is empty
    if not list(index.items()) and uri in ls.doc_indices:
        return

    ls.doc_indices[uri] = index


def _get_line(source: str, line_number: int) -> Optional[str]:
    lines = source.splitlines()
    if line_number < 0 or line_number >= len(lines):
        return None
    return lines[line_number]


def _is_identifier_char(ch: str) -> bool:
    return ch == "_" or ch.isalnum()


def _extract_symbol(line: str, character: int) -> tuple[Optional[str], Optional[str]]:
    if not line:
        return None, None

    if character >= len(line):
        character = len(line) - 1
    if character < 0:
        return None, None

    if not _is_identifier_char(line[character]) and character > 0 and _is_identifier_char(line[character - 1]):
        character -= 1

    start = character
    while start > 0 and _is_identifier_char(line[start - 1]):
        start -= 1

    end = character
    while end < len(line) and _is_identifier_char(line[end]):
        end += 1

    symbol = line[start:end]
    if not symbol:
        return None, None

    qualifier = None
    dot_index = start - 1
    if dot_index >= 0 and line[dot_index] == ".":
        q_end = dot_index
        q_start = q_end - 1
        while q_start >= 0 and _is_identifier_char(line[q_start]):
            q_start -= 1
        qualifier = line[q_start + 1 : q_end] if q_start < q_end - 1 else None

    if qualifier:
        return symbol, f"{qualifier}.{symbol}"
    return symbol, None


def _format_entries(entries: list[DocEntry]) -> str:
    chunks = []
    for entry in entries:
        header = f"**{entry.display_name}** ({entry.kind})"
        signature_block = (
            f"```tusmo\n{entry.signature}\n```" if entry.signature else ""
        )
        doc_text = _render_docstring(entry.docstring)
        chunk_parts = [header]
        if signature_block:
            chunk_parts.append(signature_block)
        chunk_parts.append(doc_text)
        chunks.append("\n\n".join(chunk_parts))
    return "\n\n---\n\n".join(chunks)


def _render_docstring(docstring: str | None) -> str:
    if not docstring:
        return "_Docstring not provided._"

    text = docstring.strip()
    if not text:
        return "_Docstring not provided._"

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace(r"\\n", "\n")
    text = text.replace(r"\n", "\n")
    text = re.sub(r"#([^#\n]+)#", lambda m: f"**{m.group(1).strip()}**", text)
    # Removing the hard line break to fix markdown formatting
    return text


def _to_path(filename: str | None) -> Optional[Path]:
    if not filename:
        return None
    path_str = filename
    if filename.startswith("file://"):
        path_str = urlparse(filename).path
    try:
        path = Path(path_str)
    except (OSError, ValueError):
        return None
    if not path.is_absolute():
        try:
            path = path.resolve()
        except OSError:
            return None
    return path


def _determine_search_roots(
    ls: TusmoLanguageServer, file_path: Optional[Path]
) -> list[Path]:
    candidates: list[Path] = []

    def add_sets(base: Path) -> None:
        for name in ("lib", "stdlib", ".lib"):
            candidates.append(base / name)

    workspace_root = getattr(ls.workspace, "root_path", None)
    if workspace_root:
        root_path = Path(workspace_root)
        add_sets(root_path)

    add_sets(Path.cwd())

    if file_path:
        repo_root = file_path.parent
        add_sets(repo_root)

    # Global fallback to ~/.tusmo/stdlib
    tusmo_home = os.environ.get("TUSMO_HOME")
    if not tusmo_home:
        tusmo_home = os.path.expanduser("~/.tusmo")
    global_stdlib = Path(tusmo_home) / "stdlib"
    if global_stdlib.exists():
        candidates.append(global_stdlib)

    uniq: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            resolved = str(candidate.resolve())
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        path_obj = Path(resolved)
        if path_obj.exists() or path_obj == global_stdlib: # Safe inclusion
            uniq.append(path_obj)

    return uniq


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tusmo hover server (docstrings on hover).",
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run in stdio mode (this is the default if --tcp is not provided).",
    )
    parser.add_argument(
        "--tcp",
        action="store_true",
        help="Run the server over TCP instead of stdio.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind when using --tcp (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=2087,
        help="Port to bind when using --tcp (default: 2087).",
    )
    parser.add_argument(
        "--log-file",
        help="Optional path to write debug logs for the language server.",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging verbosity (default: WARNING).",
    )
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_file,
        level=getattr(logging, args.log_level.upper(), logging.WARNING),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.tcp:
        LOGGER.info("Starting Tusmo hover server on tcp://%s:%s", args.host, args.port)
        server.start_tcp(args.host, args.port)
    else:
        LOGGER.info("Starting Tusmo hover server (stdio mode)")
        server.start_io()


if __name__ == "__main__":
    main()
