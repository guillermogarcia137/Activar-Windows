<#
.SYNOPSIS
Comprueba DNS y una conexion TCP, sin modificar la red.
.EXAMPLE
.\script.ps1 -Servidor example.com -Puerto 443
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Servidor,
    [ValidateRange(1, 65535)][int]$Puerto = 443,
    [ValidateRange(1, 60)][int]$Espera = 5
)
$ErrorActionPreference = 'Stop'
$client = $null
try {
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $addresses = @([Net.Dns]::GetHostAddresses($Servidor) |
        ForEach-Object { $_.IPAddressToString })
    $client = [Net.Sockets.TcpClient]::new()
    $task = $client.ConnectAsync($Servidor, $Puerto)
    if (-not $task.Wait($Espera * 1000)) { throw 'Tiempo de conexion agotado.' }
    $task.GetAwaiter().GetResult()
    [ordered]@{
        servidor = $Servidor
        direcciones = $addresses
        puerto = $Puerto
        tcp = $client.Connected
        duracion_ms = $timer.ElapsedMilliseconds
    } | ConvertTo-Json
} catch {
    Write-Error $_
    exit 1
} finally {
    if ($null -ne $client) { $client.Dispose() }
}
