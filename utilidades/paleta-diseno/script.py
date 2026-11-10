"""Exporta una paleta SVG editable, sin sobrescribir diseños."""
import argparse
from pathlib import Path
import re

def export(destination, colors):
    if not 2 <= len(colors) <= 12 or any(not re.fullmatch(r'#[0-9a-fA-F]{6}', c) for c in colors):
        raise ValueError('Usa entre 2 y 12 colores #RRGGBB.')
    if Path(destination).suffix.lower() != '.svg':
        raise ValueError('El destino debe terminar en .svg.')
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{160 * len(colors)}" height="220" viewBox="0 0 {160 * len(colors)} 220">']
    for index, color in enumerate(colors):
        x = index * 160
        parts.append(f'<rect x="{x}" width="160" height="220" fill="white"/><rect x="{x}" width="160" height="170" fill="{color}"/><text x="{x + 16}" y="202" fill="black" font-family="sans-serif" font-size="18">{color.upper()}</text>')
    parts.append('</svg>')
    with Path(destination).open('x', encoding='utf-8') as stream:
        stream.write('\n'.join(parts))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destino')
    parser.add_argument('colores', nargs='+', help='Colores #RRGGBB entre comillas')
    args = parser.parse_args()
    try:
        export(args.destino, args.colores)
        print(args.destino)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
