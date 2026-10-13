#!/usr/bin/env python3
"""Regression tests for selective imports retaining module-level C support."""

from pathlib import Path
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from compiler.frontend.parser.ast_nodes import EmbeddedCNode
from compiler.processer import parse_code_to_ast, process_imports


RAYLIB_SELECTIVE_IMPORTS = '''
isticmaal {Midab, Boos2D, AfarGees} kujira "raylib/types";
isticmaal {bilowDaaqada, xaddidFps, daaqadaMaXirantahay, bilowSawirka,
           dhameeySawirka, xirDaaqada} kujira "raylib/window";
isticmaal {nadiifiShaashada, sawirGoob} kujira "raylib/graphics";
isticmaal {kuqor, helFar} kujira "raylib/text";
'''


class SelectiveImportMetadataTests(unittest.TestCase):
    def test_raylib_selective_imports_keep_header_and_wrapper_code(self):
        source_path = REPO_ROOT / "selective-raylib-regression.tus"
        initial_ast = parse_code_to_ast(RAYLIB_SELECTIVE_IMPORTS, str(source_path))
        resolved_ast = process_imports(
            initial_ast,
            str(REPO_ROOT),
            stdlib_path=str(REPO_ROOT / "stdlib"),
        )
        embedded_c = "\n".join(
            node.code for node in resolved_ast if isinstance(node, EmbeddedCNode)
        )

        self.assertIn('#include "stdlib/raylib/raylib.h"', embedded_c)
        self.assertIn("void Tusmo_ClearBackground(Midab color)", embedded_c)
        self.assertIn("void Tusmo_DrawCircle(", embedded_c)
        self.assertIn("TusmoValue Tusmo_LoadFont(", embedded_c)
        self.assertIn("void Tusmo_DrawTextEx(", embedded_c)


if __name__ == "__main__":
    unittest.main(verbosity=2)
