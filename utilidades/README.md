# Utilidades para Windows

Orientadas a Windows 10/11; consulta los requisitos de cada utilidad.
Las herramientas de archivos también funcionan con Python en otros sistemas.
No requieren permisos de administrador ni paquetes externos. No cambian la
activación de Windows. Los scripts de activación originales siguen separados.

Cada carpeta contiene dos implementaciones independientes y un lanzador:

| Archivo | Requisitos |
| --- | --- |
| `script.ps1` | Windows PowerShell 5.1 o PowerShell 7 |
| `script.py` | Python 3.9 o posterior |
| `ejecutar.cmd` | Abre la versión PowerShell y transmite sus argumentos y código de salida |

Ejecuta los ejemplos desde la carpeta de la utilidad. Las rutas con espacios
deben ir entre comillas. Python también puede iniciarse con `python` si `py` no
está instalado. Consulta la ayuda con `py script.py --help` o
`Get-Help .\script.ps1 -Detailed`.

| Carpeta | Uso |
| --- | --- |
| `informacion-sistema` | Informe de Windows, procesador, memoria y discos en JSON |
| `diagnostico-red` | Resolución DNS y conexión TCP a un servidor y puerto |
| `copia-seguridad` | Copia ZIP nueva de una carpeta, sin sobrescribir archivos |
| `limpieza-temporales` | Vista previa o borrado de archivos temporales antiguos |
| `crear-proyecto` | Productividad: estructura de carpetas y lista de tareas |
| `buscar-duplicados` | Productividad: informe SHA-256 sin borrar archivos |
| `tema-windows` | Personalización: consultar o aplicar tema claro/oscuro |
| `paleta-diseno` | Diseño: exportar muestras de color a SVG editable |

El lanzador respeta la política de ejecución de PowerShell; no la modifica ni
la omite. Si tu organización bloquea scripts, utiliza la versión Python o
consulta a su administrador. No se descargan ni ejecutan programas externos.

## Comprobaciones

Las pruebas de Python usan únicamente la biblioteca estándar y carpetas
temporales: `py -m unittest discover -s utilidades/tests -v`, desde la raíz
del repositorio. Cubren la copia ZIP y las protecciones de limpieza.
Las versiones PowerShell y los informes específicos de Windows requieren
validación en Windows; una prueba en Linux no confirma su funcionamiento allí.

## Primeros pasos

1. Descarga o clona el repositorio.
2. Abre PowerShell en la carpeta de la herramienta elegida.
3. Consulta su README y ejecuta el ejemplo con tus rutas.

Las versiones Python y PowerShell tienen argumentos propios: no intercambies
`--opciones` de Python con `-Parametros` de PowerShell. CMD es un lanzador
de PowerShell, no una tercera implementación independiente. Para parámetros
de tipo lista, como `-Colores`, ejecuta el `.ps1` desde PowerShell.

Los informes pueden contener nombres del equipo, rutas o direcciones de red;
revísalos antes de compartirlos. La limpieza con aplicar elimina archivos sin
papelera. Las copias ZIP no sustituyen una copia consistente de bases de datos
o archivos que estén cambiando.
