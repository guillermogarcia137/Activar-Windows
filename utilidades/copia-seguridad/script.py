"""Crea un ZIP nuevo sin modificar la carpeta de origen ni seguir enlaces."""
import argparse
import os
from pathlib import Path
import stat
import sys
import zipfile


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & 0x400)


def walk_error(error):
    # Una carpeta ilegible no debe producir una copia aparentemente completa.
    raise error


def backup(source, destination):
    source = Path(source).resolve(strict=True)
    destination = Path(destination).resolve()
    if not source.is_dir():
        raise ValueError("El origen debe ser una carpeta.")
    if destination == source or source in destination.parents:
        raise ValueError("El ZIP debe guardarse fuera de la carpeta de origen.")
    if destination.suffix.lower() != ".zip":
        raise ValueError("El destino debe tener extensión .zip.")
    # Modo exclusivo: una copia existente nunca se sobrescribe.
    with destination.open("xb") as output:
        try:
            with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
                for root, dirs, files in os.walk(source, followlinks=False, onerror=walk_error):
                    dirs[:] = sorted(d for d in dirs if not is_link(Path(root) / d))
                    folder = Path(root)
                    if folder != source:
                        archive.write(folder, folder.relative_to(source).as_posix() + "/")
                    for name in sorted(files):
                        path = folder / name
                        if not is_link(path) and path.is_file():
                            archive.write(path, path.relative_to(source))
        except BaseException:
            output.close()
            destination.unlink()
            raise
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origen")
    parser.add_argument("destino", help="Ruta de un ZIP nuevo; su carpeta debe existir")
    args = parser.parse_args()
    try:
        print(f"Copia creada: {backup(args.origen, args.destino)}")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"No se pudo crear la copia: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
