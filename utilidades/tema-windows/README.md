# Tema de Windows · Personalización

Consulta el estado por defecto. `claro` y `oscuro` cambian dos preferencias del
usuario actual en HKCU, para aplicaciones y sistema. Anota el estado antes de
cambiarlo; puedes volver a aplicar el modo anterior. No cambia fondos, contraste
alto ni aplicaciones con tema propio. Algunas necesitan reinicio o cerrar sesión.
Disponible en Windows 10/11 con interfaz de escritorio; no para Server Core.

```powershell
.\script.ps1 -Modo estado
.\script.ps1 -Modo oscuro -WhatIf
.\script.ps1 -Modo oscuro
py script.py claro
.\ejecutar.cmd -Modo claro
```
