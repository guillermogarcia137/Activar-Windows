<#
.SYNOPSIS
Genera una paleta SVG nueva con entre 2 y 12 colores hexadecimales.
.EXAMPLE
.\script.ps1 -Destino paleta.svg -Colores '#2563EB','#0F172A','#F8FAFC'
#>
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Destino,
      [Parameter(Mandatory=$true)][string[]]$Colores)
$ErrorActionPreference = 'Stop'
try {
    if ($Colores.Count -lt 2 -or $Colores.Count -gt 12) { throw 'Usa entre 2 y 12 colores.' }
    foreach ($color in $Colores) { if ($color -notmatch '^#[0-9a-fA-F]{6}$') { throw 'Usa colores #RRGGBB.' } }
    if ([IO.Path]::GetExtension($Destino) -ne '.svg') { throw 'El destino debe ser .svg.' }
    $width = 160 * $Colores.Count
    $parts = @("<svg xmlns=`"http://www.w3.org/2000/svg`" width=`"$width`" height=`"220`" viewBox=`"0 0 $width 220`">")
    for ($i = 0; $i -lt $Colores.Count; $i++) {
        $x = $i * 160; $tx = $x + 16; $color = $Colores[$i].ToUpperInvariant()
        $parts += "<rect x=`"$x`" width=`"160`" height=`"220`" fill=`"white`"/><rect x=`"$x`" width=`"160`" height=`"170`" fill=`"$color`"/><text x=`"$tx`" y=`"202`" fill=`"black`" font-family=`"sans-serif`" font-size=`"18`">$color</text>"
    }
    $parts += '</svg>'
    $target = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destino)
    $stream = [IO.File]::Open($target, [IO.FileMode]::CreateNew)
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes(($parts -join "`n"))
        $stream.Write($bytes, 0, $bytes.Length)
    } finally { $stream.Dispose() }
    Write-Output $target
} catch { Write-Error $_; exit 1 }
