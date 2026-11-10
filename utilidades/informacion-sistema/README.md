# Información del sistema

Muestra equipo, versión de Windows, arquitectura, procesadores, memoria y
espacio total/libre de los discos locales. No incluye claves de producto.
La versión Python consulta CIM mediante Windows PowerShell incluido en Windows.

```powershell
.\ejecutar.cmd
.\script.ps1
py script.py
```

Para guardar el informe desde PowerShell:
`py script.py | Out-File informe.json -Encoding utf8`.
El informe contiene el nombre del equipo; revísalo antes de compartirlo.
