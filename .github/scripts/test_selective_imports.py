#!/usr/bin/env python3
"""Regression tests for selective imports retaining module-level C support."""

from pathlib import Path
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from compiler.frontend.parser.ast_nodes import EmbeddedCNode
from compiler.processer import parse_code_to_ast, process_imports
import tusmo


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

    def test_linker_metadata_resolves_bundled_library_from_stdlib_on_each_platform(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            install_stdlib = temp / "installed" / "stdlib"
            project = temp / "unrelated-project"
            raylib_dir = install_stdlib / "raylib"
            raylib_dir.mkdir(parents=True)
            project.mkdir()

            linux_library = raylib_dir / "libraylib.a"
            windows_library = raylib_dir / "libraylib.a.lib"
            linux_library.touch()
            windows_library.touch()

            original_metadata = tusmo.Xidid.dhamaan_xogta
            tusmo.Xidid.dhamaan_xogta = [
                "stdlib/raylib/libraylib.a",
                "-lm.maya",
                "-lGL.maya",
            ]
            try:
                with patch.dict(os.environ, {"TUSMO_HOME": str(install_stdlib.parent)}), \
                     patch.object(tusmo.platform, "system", return_value="Linux"), \
                     patch("tusmo.os.getcwd", return_value=str(project)):
                    linux_args = tusmo.get_static_lib(
                        stdlib_dir=str(install_stdlib),
                        project_root=str(temp / "compiler"),
                    )
                self.assertIn(f'"{linux_library}"', linux_args)
                self.assertTrue(linux_args.endswith("-lm -lGL"))
                self.assertNotIn("-lm.a", linux_args)

                with patch.dict(os.environ, {"TUSMO_HOME": str(install_stdlib.parent)}), \
                     patch.object(tusmo.platform, "system", return_value="Windows"), \
                     patch("tusmo.os.getcwd", return_value=str(project)):
                    windows_args = tusmo.get_static_lib(
                        stdlib_dir=str(install_stdlib),
                        project_root=str(temp / "compiler"),
                    )
                self.assertIn(f'"{windows_library}"', windows_args)
                self.assertTrue(windows_args.endswith("-lm -lGL"))
                self.assertNotIn("-lm.lib", windows_args)

                with patch.dict(os.environ, {"TUSMO_HOME": str(install_stdlib.parent)}), \
                     patch.object(tusmo.platform, "system", return_value="Darwin"), \
                     patch("tusmo.os.getcwd", return_value=str(project)):
                    mac_args = tusmo.get_static_lib(
                        stdlib_dir=str(install_stdlib),
                        project_root=str(temp / "compiler"),
                    )
                self.assertIn(f'"{linux_library}"', mac_args)
                self.assertTrue(mac_args.endswith("-lm -lGL"))
            finally:
                tusmo.Xidid.dhamaan_xogta = original_metadata


if __name__ == "__main__":
    unittest.main(verbosity=2)
