<#
.SYNOPSIS
Muestra un informe de Windows en JSON sin modificar el sistema.
.EXAMPLE
.\script.ps1
#>
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
try {
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
} catch {
    Write-Error $_
    exit 1
}
