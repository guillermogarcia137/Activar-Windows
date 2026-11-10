# Limpieza de temporales

Inspecciona únicamente la carpeta temporal del usuario indicada por Windows
(Python utiliza la carpeta temporal detectada por su biblioteca estándar).
Revisa la ruta mostrada, especialmente si has personalizado `TEMP` o `TMP`.
Por defecto solo lista archivos sin modificar desde hace más de siete días.
No sigue enlaces ni junctions, no elimina carpetas y comunica los errores.

```powershell
# Vista previa: no borra nada.
.\ejecutar.cmd -Dias 7
py script.py --dias 7

# Borrado definitivo: revisa primero la vista previa y cierra las aplicaciones.
.\script.ps1 -Dias 7 -Aplicar
py script.py --dias 7 --aplicar

# Simular el borrado con el mecanismo nativo de PowerShell.
.\script.ps1 -Dias 7 -Aplicar -WhatIf
```

El borrado no usa la papelera. Un archivo antiguo puede seguir siendo necesario;
revisa la lista antes de aplicar. Los archivos bloqueados se omiten con aviso y
código de salida 1. Evita ejecutarlo mientras otros programas crean, mueven o
modifican archivos temporales.
