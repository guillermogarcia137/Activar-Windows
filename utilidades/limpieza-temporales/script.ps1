<#
.SYNOPSIS
Previsualiza temporales antiguos. -Aplicar permite eliminarlos definitivamente.
.EXAMPLE
.\script.ps1 -Dias 7
.EXAMPLE
.\script.ps1 -Dias 7 -Aplicar
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateRange(1, 36500)][int]$Dias = 7,
    [switch]$Aplicar
)
$ErrorActionPreference = 'Stop'
$failures = 0
try {
    $root = Get-Item -LiteralPath ([IO.Path]::GetTempPath()) -Force
    if (-not $root.PSIsContainer -or $root.Parent -eq $null -or
        $root.FullName.TrimEnd('\') -eq $HOME.TrimEnd('\')) {
        throw 'Carpeta temporal no valida.'
    }
    $ancestor = $root
    while ($null -ne $ancestor) {
        if ($ancestor.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw 'La carpeta temporal no puede pasar por enlaces o junctions.'
        }
        $ancestor = $ancestor.Parent
    }
    Write-Output "Carpeta temporal: $($root.FullName)"
    $cutoff = [DateTime]::UtcNow.AddDays(-$Dias)
    $selected = 0
    $removed = 0
    $bytes = [long]0
    $pending = [Collections.Generic.Stack[IO.DirectoryInfo]]::new()
    $pending.Push($root)
    while ($pending.Count -gt 0) {
        $folder = $pending.Pop()
        try {
            $items = @(Get-ChildItem -LiteralPath $folder.FullName -Force)
        } catch {
            Write-Warning $_
            $failures++
            continue
        }
        foreach ($item in $items) {
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
            if ($item.PSIsContainer) { $pending.Push($item); continue }
            if ($item.LastWriteTimeUtc -ge $cutoff) { continue }
            $selected++
            $bytes += $item.Length
            if (-not $Aplicar) {
                Write-Output "Vista previa: $($item.FullName)"
            } elseif ($PSCmdlet.ShouldProcess($item.FullName, 'Eliminar temporal definitivamente')) {
                try {
                    Remove-Item -LiteralPath $item.FullName
                    $removed++
                } catch {
                    Write-Warning $_
                    $failures++
                }
            }
        }
    }
    Write-Output "Seleccionados: $selected; eliminados: $removed; bytes seleccionados: $bytes; errores: $failures"
    if ($failures -gt 0) { exit 1 }
} catch {
    Write-Error $_
    exit 1
}
