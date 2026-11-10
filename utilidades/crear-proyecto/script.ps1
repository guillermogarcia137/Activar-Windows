<#
.SYNOPSIS
Crea una carpeta de proyecto nueva con documentos, recursos, src y exportaciones.
.EXAMPLE
.\script.ps1 -Destino "C:\Proyectos\Mi proyecto"
#>
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Destino)
$ErrorActionPreference = 'Stop'
try {
    # New-Item sin Force rechaza un destino existente.
    $target = New-Item -ItemType Directory -Path $Destino
    foreach ($folder in 'documentos','recursos','src','exportaciones') {
        $null = New-Item -ItemType Directory -Path (Join-Path $target.FullName $folder)
    }
    Set-Content -LiteralPath (Join-Path $target.FullName 'README.md') -Encoding UTF8 -Value "# Proyecto`n`nObjetivo:`n`nTareas:`n- [ ] Definir alcance"
    Write-Output $target.FullName
} catch { Write-Error $_; exit 1 }
