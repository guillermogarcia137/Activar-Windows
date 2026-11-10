"""Crea una estructura de proyecto nueva, sin sobrescribir carpetas."""
import argparse
from pathlib import Path

def create(destination):
    target = Path(destination)
    target.mkdir()  # Exclusivo: falla si ya existe.
    for folder in ('documentos', 'recursos', 'src', 'exportaciones'):
        (target / folder).mkdir()
    (target / 'README.md').write_text('# Proyecto\n\nObjetivo:\n\nTareas:\n- [ ] Definir alcance\n', encoding='utf-8')
    return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destino')
    args = parser.parse_args()
    try:
        print(create(args.destino))
    except OSError as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
