<#
.SYNOPSIS
Crea un ZIP nuevo fuera del origen sin seguir enlaces ni sobrescribir copias.
.EXAMPLE
.\script.ps1 -Origen C:\Datos -Destino D:\Copias\datos.zip
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Origen,
    [Parameter(Mandatory = $true)][string]$Destino
)
$ErrorActionPreference = 'Stop'
$stream = $null
$archive = $null
$created = $false
try {
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $source = Get-Item -LiteralPath $Origen -Force
    if (-not $source.PSIsContainer) { throw 'El origen debe ser una carpeta.' }
    # Evita tambien origenes que pasan por enlaces o junctions.
    $ancestor = $source
    while ($null -ne $ancestor) {
        if ($ancestor.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw 'El origen no puede pasar por enlaces o junctions.'
        }
        $ancestor = $ancestor.Parent
    }
    $base = $source.FullName.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
    $target = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destino)
    if ([IO.Path]::GetExtension($target) -ne '.zip') { throw 'El destino debe ser .zip.' }
    $parent = Get-Item -LiteralPath ([IO.Path]::GetDirectoryName($target)) -Force
    $ancestor = $parent
    while ($null -ne $ancestor) {
        if ($ancestor.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw 'El destino no puede pasar por enlaces o junctions.'
        }
        $ancestor = $ancestor.Parent
    }
    if ($target.StartsWith($base, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'El ZIP debe guardarse fuera de la carpeta de origen.'
    }
    $stream = [IO.File]::Open($target, [IO.FileMode]::CreateNew)
    $created = $true
    $archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Create)
    $pending = [Collections.Generic.Stack[IO.DirectoryInfo]]::new()
    $pending.Push($source)
    while ($pending.Count -gt 0) {
        $folder = $pending.Pop()
        foreach ($item in Get-ChildItem -LiteralPath $folder.FullName -Force) {
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
            $relative = $item.FullName.Substring($base.Length).Replace('\', '/')
            if ($item.PSIsContainer) {
                $null = $archive.CreateEntry($relative + '/')
                $pending.Push($item)
            } else {
                $null = [IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                    $archive, $item.FullName, $relative, [IO.Compression.CompressionLevel]::Optimal)
            }
        }
    }
    $archive.Dispose()
    $archive = $null
    $stream.Dispose()
    $stream = $null
    Write-Output "Copia creada: $target"
} catch {
    if ($null -ne $archive) { $archive.Dispose() }
    if ($null -ne $stream) { $stream.Dispose() }
    if ($created) { Remove-Item -LiteralPath $target -Force }
    Write-Error $_
    exit 1
}
