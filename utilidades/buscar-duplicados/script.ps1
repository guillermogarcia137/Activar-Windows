<#
.SYNOPSIS
Lista duplicados SHA-256 sin borrar archivos ni recorrer enlaces.
.EXAMPLE
.\script.ps1 -Origen C:\Datos
#>
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Origen)
$ErrorActionPreference = 'Stop'
try {
    $source = Get-Item -LiteralPath $Origen -Force
    if (-not $source.PSIsContainer -or ($source.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'El origen debe ser una carpeta sin enlace.' }
    $pending = [Collections.Generic.Stack[string]]::new()
    $pending.Push($source.FullName)
    $groups = @{}
    while ($pending.Count -gt 0) {
        foreach ($item in Get-ChildItem -LiteralPath $pending.Pop() -Force) {
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
            if ($item.PSIsContainer) { $pending.Push($item.FullName); continue }
            $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            if (-not $groups.ContainsKey($hash)) { $groups[$hash] = @() }
            $groups[$hash] += $item.FullName
        }
    }
    $result = @(foreach ($hash in ($groups.Keys | Sort-Object)) {
        if ($groups[$hash].Count -gt 1) { [pscustomobject]@{sha256=$hash; archivos=@($groups[$hash] | Sort-Object)} }
    })
    ConvertTo-Json -InputObject $result -Depth 4
} catch { Write-Error $_; exit 1 }
