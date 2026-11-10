"""Pruebas funcionales con archivos desechables, sin tocar datos del usuario."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def load(folder):
    spec = importlib.util.spec_from_file_location(folder, ROOT / folder / "script.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


backup = load("copia-seguridad")
cleanup = load("limpieza-temporales")


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "origen con espacios"
        self.source.mkdir()
        (self.source / "vacía").mkdir()
        (self.source / "datos.txt").write_text("datos de prueba", encoding="utf-8")
        (self.source / ".oculto").write_bytes(b"oculto")
        self.target = self.root / "copia.zip"

    def test_archive_content_and_empty_directory(self):
        backup.backup(self.source, self.target)
        with zipfile.ZipFile(self.target) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.read("datos.txt"), b"datos de prueba")
            self.assertEqual(archive.read(".oculto"), b"oculto")
            self.assertIn("vacía/", archive.namelist())

    def test_existing_backup_is_preserved(self):
        self.target.write_bytes(b"no sobrescribir")
        with self.assertRaises(FileExistsError):
            backup.backup(self.source, self.target)
        self.assertEqual(self.target.read_bytes(), b"no sobrescribir")

    def test_destination_inside_source_is_rejected(self):
        with self.assertRaises(ValueError):
            backup.backup(self.source, self.source / "copia.zip")
        self.assertFalse((self.source / "copia.zip").exists())

    def test_incomplete_archive_is_removed(self):
        from unittest.mock import patch
        with patch.object(zipfile.ZipFile, "write", side_effect=OSError("lectura fallida")):
            with self.assertRaises(OSError):
                backup.backup(self.source, self.target)
        self.assertFalse(self.target.exists())

    def test_links_are_not_archived(self):
        external = self.root / "externo.txt"
        external.write_bytes(b"fuera del origen")
        try:
            (self.source / "enlace").symlink_to(external)
        except OSError:
            self.skipTest("No se permite crear enlaces en este equipo")
        backup.backup(self.source, self.target)
        with zipfile.ZipFile(self.target) as archive:
            self.assertNotIn("enlace", archive.namelist())

    def test_unreadable_directory_fails_and_removes_partial_zip(self):
        from unittest.mock import patch

        def failed_walk(*args, **kwargs):
            kwargs["onerror"](PermissionError("carpeta inaccesible"))
            return iter(())

        with patch.object(backup.os, "walk", side_effect=failed_walk):
            with self.assertRaises(PermissionError):
                backup.backup(self.source, self.target)
        self.assertFalse(self.target.exists())


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.old = self.root / "antiguo.tmp"
        self.old.write_bytes(b"antiguo")
        self.new = self.root / "reciente.tmp"
        self.new.write_bytes(b"reciente")
        old_time = time.time() - 10 * 86400
        os.utime(self.old, (old_time, old_time))

    def clean(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return cleanup.clean(self.root, **kwargs)

    def test_preview_preserves_files(self):
        result = self.clean()
        self.assertEqual(result["seleccionados"], 1)
        self.assertEqual(result["eliminados"], 0)
        self.assertTrue(self.old.exists())
        self.assertTrue(self.new.exists())

    def test_apply_only_removes_old_files(self):
        result = self.clean(apply=True)
        self.assertEqual(result["eliminados"], 1)
        self.assertFalse(self.old.exists())
        self.assertTrue(self.new.exists())

    def test_zero_days_is_rejected(self):
        with self.assertRaises(ValueError):
            self.clean(days=0, apply=True)
        self.assertTrue(self.old.exists())

    def test_directory_links_do_not_escape_root(self):
        with tempfile.TemporaryDirectory() as external:
            protected = Path(external) / "importante.txt"
            protected.write_bytes(b"no borrar")
            old_time = time.time() - 10 * 86400
            os.utime(protected, (old_time, old_time))
            try:
                (self.root / "enlace").symlink_to(external, target_is_directory=True)
            except OSError:
                self.skipTest("No se permite crear enlaces en este equipo")
            self.clean(apply=True)
            self.assertTrue(protected.exists())


class CommandLineTests(unittest.TestCase):
    def test_all_help_commands(self):
        for name in ("informacion-sistema", "diagnostico-red", "copia-seguridad", "limpieza-temporales"):
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(ROOT / name / "script.py"), "--help"],
                                        capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_tcp_diagnostic_on_local_listener(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            result = subprocess.run([
                sys.executable, str(ROOT / "diagnostico-red" / "script.py"),
                "127.0.0.1", "--puerto", str(listener.getsockname()[1]),
            ], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"tcp": true', result.stdout)

    def test_invalid_port_fails(self):
        result = subprocess.run([
            sys.executable, str(ROOT / "diagnostico-red" / "script.py"),
            "localhost", "--puerto", "0",
        ], capture_output=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
