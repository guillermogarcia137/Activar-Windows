"""Agrupa archivos por SHA-256; no elimina nada ni recorre enlaces."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

def linked(path):
    info = path.lstat()
    return path.is_symlink() or bool(getattr(info, 'st_file_attributes', 0) & 0x400)

def find_duplicates(source):
    source = Path(source)
    if not source.is_dir() or linked(source):
        raise ValueError('El origen debe ser una carpeta sin enlace.')
    groups = {}
    def fail(error):
        raise error
    for base, dirs, files in os.walk(source, onerror=fail, followlinks=False):
        dirs[:] = sorted(n for n in dirs if not linked(Path(base) / n))
        for name in sorted(files):
            path = Path(base) / name
            if linked(path) or not stat.S_ISREG(path.stat().st_mode):
                continue
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(block)
            groups.setdefault(digest.hexdigest(), []).append(str(path))
    return [{'sha256': key, 'archivos': paths} for key, paths in sorted(groups.items()) if len(paths) > 1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('origen')
    args = parser.parse_args()
    try:
        print(json.dumps(find_duplicates(args.origen), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
