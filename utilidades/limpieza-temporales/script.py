"""Previsualiza temporales antiguos; solo borra con --aplicar."""
import argparse
import os
from pathlib import Path
import stat
import sys
import tempfile
import time


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & 0x400)


def clean(root, days=7, apply=False):
    if days < 1:
        raise ValueError("La antigüedad mínima es de un día.")
    root = Path(root)
    if is_link(root):
        raise ValueError("La carpeta temporal no puede ser un enlace.")
    root = root.resolve(strict=True)
    if not root.is_dir() or root == Path(root.anchor) or root == Path.home().resolve():
        raise ValueError("Carpeta temporal no válida.")
    cutoff = time.time() - days * 86400
    selected = removed = errors = total = 0

    def walk_error(exc):
        nonlocal errors
        errors += 1
        print(f"No se pudo inspeccionar: {exc}", file=sys.stderr)

    for folder, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        safe_dirs = []
        for name in dirs:
            try:
                if not is_link(Path(folder) / name):
                    safe_dirs.append(name)
            except OSError as exc:
                walk_error(exc)
        dirs[:] = safe_dirs
        for name in files:
            path = Path(folder) / name
            try:
                if is_link(path):
                    continue
                info = path.stat()
                if not stat.S_ISREG(info.st_mode) or info.st_mtime >= cutoff:
                    continue
                selected += 1
                total += info.st_size
                print(f"{'Borrar' if apply else 'Vista previa'}: {path}")
                if apply:
                    path.unlink()
                    removed += 1
            except OSError as exc:
                walk_error(exc)
    return {"seleccionados": selected, "eliminados": removed,
            "bytes_seleccionados": total, "errores": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dias", type=int, default=7)
    parser.add_argument("--aplicar", action="store_true", help="Elimina sin pasar por la papelera")
    args = parser.parse_args()
    try:
        root = tempfile.gettempdir()
        print(f"Carpeta temporal: {root}")
        summary = clean(root, args.dias, args.aplicar)
        print(summary)
        return 1 if summary["errores"] else 0
    except (OSError, ValueError) as exc:
        print(f"No se pudo limpiar: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
