"""Comprobaciones de resultados y protección de archivos existentes."""
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from test_utilidades import load

project = load('crear-proyecto')
duplicates = load('buscar-duplicados')
palette = load('paleta-diseno')

class NewToolsTests(unittest.TestCase):
    def test_project_preserves_existing_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'Proyecto con espacios'
            project.create(target)
            self.assertTrue((target / 'src').is_dir())
            (target / 'README.md').write_text('contenido personal')
            with self.assertRaises(FileExistsError):
                project.create(target)
            self.assertEqual((target / 'README.md').read_text(), 'contenido personal')

    def test_duplicates_compare_content_and_keep_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, data in [('a', b'igual'), ('b', b'igual'), ('c', b'otros')]:
                (root / name).write_bytes(data)
            result = duplicates.find_duplicates(root)
            self.assertEqual(len(result), 1)
            self.assertEqual({Path(p).name for p in result[0]['archivos']}, {'a', 'b'})
            self.assertEqual(len(list(root.iterdir())), 3)

    def test_svg_valid_and_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'colores.svg'
            palette.export(target, ['#abcdef', '#000000'])
            svg = ET.parse(target).getroot()
            self.assertEqual(svg.attrib['width'], '320')
            original = target.read_bytes()
            with self.assertRaises(FileExistsError):
                palette.export(target, ['#ffffff', '#000000'])
            self.assertEqual(target.read_bytes(), original)
            with self.assertRaises(ValueError):
                palette.export(Path(tmp) / 'invalido.svg', ['<script>', '#000000'])
            self.assertFalse((Path(tmp) / 'invalido.svg').exists())

if __name__ == '__main__':
    unittest.main()
