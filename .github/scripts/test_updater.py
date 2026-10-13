#!/usr/bin/env python3
"""Regression tests for updater subprocess handling in frozen Tusmo builds."""

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

import tusmo


class UpdaterEnvironmentTests(unittest.TestCase):
    def test_linux_restores_original_library_path(self):
        env = {
            "LD_LIBRARY_PATH": "/opt/tusmo/bin/_internal",
            "LD_LIBRARY_PATH_ORIG": "/usr/lib/custom",
        }
        with mock.patch.dict(os.environ, env, clear=True), \
             mock.patch.object(sys, "platform", "linux"), \
             mock.patch.object(sys, "frozen", True, create=True):
            result = tusmo._update_subprocess_environment()

        self.assertEqual(result["LD_LIBRARY_PATH"], "/usr/lib/custom")

    def test_linux_removes_bundled_path_when_no_original_existed(self):
        with mock.patch.dict(os.environ, {"LD_LIBRARY_PATH": "/opt/tusmo/bin/_internal"}, clear=True), \
             mock.patch.object(sys, "platform", "linux"), \
             mock.patch.object(sys, "frozen", True, create=True):
            result = tusmo._update_subprocess_environment()

        self.assertNotIn("LD_LIBRARY_PATH", result)

    def test_macos_removes_only_paths_inside_bundle(self):
        with tempfile.TemporaryDirectory() as bundle_dir:
            bundle_lib = os.path.join(bundle_dir, "_internal")
            env = {"DYLD_LIBRARY_PATH": os.pathsep.join((bundle_lib, "/usr/local/lib"))}
            with mock.patch.dict(os.environ, env, clear=True), \
                 mock.patch.object(sys, "platform", "darwin"), \
                 mock.patch.object(sys, "frozen", True, create=True), \
                 mock.patch.object(sys, "_MEIPASS", bundle_dir, create=True):
                result = tusmo._update_subprocess_environment()

        self.assertEqual(result["DYLD_LIBRARY_PATH"], "/usr/local/lib")

    def test_windows_resets_pyinstaller_dll_search_directory(self):
        kernel = mock.Mock()
        kernel.SetDllDirectoryW.return_value = 1
        with mock.patch.dict(os.environ, {}, clear=True), \
             mock.patch.object(sys, "platform", "win32"), \
             mock.patch.object(sys, "frozen", True, create=True), \
             mock.patch("ctypes.WinDLL", return_value=kernel, create=True):
            tusmo._update_subprocess_environment()

        kernel.SetDllDirectoryW.assert_called_once_with(None)


class UpdaterExecutionTests(unittest.TestCase):
    def test_failed_installer_download_stops_before_running_bash(self):
        failure = subprocess.CalledProcessError(6, ["curl"])
        with mock.patch.object(tusmo.subprocess, "run", side_effect=failure) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                tusmo._run_unix_update({"PATH": os.environ.get("PATH", "")})

        run.assert_called_once()
        self.assertEqual(run.call_args.kwargs["check"], True)

    def test_failed_update_is_not_reported_as_success(self):
        failure = subprocess.CalledProcessError(6, ["curl"])
        output = io.StringIO()
        with mock.patch.object(tusmo.platform, "system", return_value="Linux"), \
             mock.patch.object(tusmo, "_update_subprocess_environment", return_value={}), \
             mock.patch.object(tusmo, "_run_unix_update", side_effect=failure), \
             contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as raised:
                tusmo.update_tusmo("update")

        self.assertEqual(raised.exception.code, 6)
        self.assertIn("way fashilantay", output.getvalue())
        self.assertNotIn("waa la cusboonaysiiyay", output.getvalue())

    def test_windows_handoff_waits_for_running_app_to_exit(self):
        with mock.patch.object(tusmo.subprocess, "Popen") as popen:
            tusmo._start_windows_update({"PATH": "system-path"})

        args, kwargs = popen.call_args
        self.assertIn("powershell.exe", args[0][0])
        self.assertIn("Invoke-WebRequest", args[0][-1])
        self.assertEqual(kwargs["env"]["TUSMO_UPDATE_WAIT_PID"], str(os.getpid()))
        self.assertEqual(kwargs["env"]["TUSMO_EXPECT_VERSION"], tusmo.LOCAL_VERSION)


if __name__ == "__main__":
    unittest.main(verbosity=2)
