"""Consulta o cambia el tema del usuario actual; no requiere administrador."""
import argparse
import sys
KEY = r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
NAMES = ('AppsUseLightTheme', 'SystemUsesLightTheme')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('modo', choices=['estado', 'claro', 'oscuro'], nargs='?', default='estado')
    args = parser.parse_args()
    if sys.platform != 'win32':
        parser.exit(1, 'Esta utilidad requiere Windows.\n')
    import winreg
    try:
        if args.modo == 'estado':
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY) as key:
                for name in NAMES:
                    try:
                        print(f'{name}: {winreg.QueryValueEx(key, name)[0]}')
                    except FileNotFoundError:
                        print(f'{name}: predeterminado de Windows')
        else:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, KEY) as key:
                for name in NAMES:
                    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(args.modo == 'claro'))
            print('Tema guardado. Algunas aplicaciones necesitan reiniciarse o cerrar sesión.')
    except FileNotFoundError:
        print('Tema predeterminado de Windows (sin personalización registrada).')
    except OSError as exc:
        parser.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
