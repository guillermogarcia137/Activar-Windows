"""Informe de Windows en JSON, sin modificar la configuración."""
import argparse
import json
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if sys.platform != "win32":
        parser.error("Esta utilidad requiere Windows y Windows PowerShell.")
    # CIM obtiene los mismos datos independientemente del idioma de Windows.
    command = r"""+$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor
$disks = @(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' |
    Select-Object DeviceID, Size, FreeSpace)
[ordered]@{
    Equipo = $env:COMPUTERNAME
    Sistema = $os.Caption
    Version = $os.Version
    Arquitectura = $os.OSArchitecture
    Procesador = @($cpu | ForEach-Object { $_.Name })
    MemoriaTotalBytes = [long]$os.TotalVisibleMemorySize * 1024
    MemoriaLibreBytes = [long]$os.FreePhysicalMemory * 1024
    Discos = $disks
} | ConvertTo-Json -Depth 4
"""
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive",
             "-Command", command], capture_output=True, check=True,
            encoding="utf-8", errors="replace", timeout=60,
        )
        print(json.dumps(json.loads(result.stdout), ensure_ascii=True, indent=2))
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"No se pudo obtener el informe: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
