# Diagnóstico de red

Resuelve un nombre y comprueba una conexión TCP. No modifica DNS, cortafuegos
ni adaptadores. Una conexión TCP correcta no valida TLS ni el servicio HTTP.
El tiempo de espera afecta a TCP; DNS usa los tiempos del sistema. En Python
puede haber varios intentos si el servidor tiene varias direcciones.

```powershell
.\ejecutar.cmd -Servidor example.com -Puerto 443 -Espera 5
.\script.ps1 -Servidor example.com -Puerto 443
py script.py example.com --puerto 443 --espera 5
```

También acepta IP y puertos de servicios locales. Devuelve código 1 si falla.
