# Copia de seguridad ZIP

Crea un archivo nuevo con archivos ocultos y carpetas vacías. El ZIP debe estar
fuera del origen y su carpeta debe existir. Si el destino existe, falla sin
sobrescribirlo. Omite enlaces simbólicos y junctions dentro del origen.
Si un archivo no puede leerse, falla y elimina el ZIP incompleto.

```powershell
.\ejecutar.cmd -Origen "C:\Users\Ana\Documents" -Destino "D:\Copias\documentos.zip"
.\script.ps1 -Origen "C:\Datos" -Destino "D:\Copias\datos.zip"
py script.py "C:\Datos" "D:\Copias\datos.zip"
```

No es una imagen del sistema: no conserva permisos NTFS, flujos alternativos
ni una instantánea coherente de archivos que estén cambiando. Cierra los
programas que escriban en el origen y comprueba el ZIP antes de depender de él.
Para restaurar, usa «Extraer todo» de Windows en una carpeta vacía.
