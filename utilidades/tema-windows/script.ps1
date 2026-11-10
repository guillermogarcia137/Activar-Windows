<#
.SYNOPSIS
Consulta o cambia el tema claro/oscuro del usuario actual.
.EXAMPLE
.\script.ps1 -Modo oscuro
#>
[CmdletBinding(SupportsShouldProcess=$true)]
param([ValidateSet('estado','claro','oscuro')][string]$Modo='estado')
$ErrorActionPreference = 'Stop'
try {
    $key = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    if ($Modo -eq 'estado') {
        if (Test-Path -LiteralPath $key) { Get-ItemProperty -LiteralPath $key | Select-Object AppsUseLightTheme,SystemUsesLightTheme }
        else { Write-Output 'Tema predeterminado de Windows.' }
    } elseif ($PSCmdlet.ShouldProcess($key, "Aplicar tema $Modo")) {
        $null = New-Item -Path $key -Force
        $value = [int]($Modo -eq 'claro')
        foreach ($name in 'AppsUseLightTheme','SystemUsesLightTheme') {
            $null = New-ItemProperty -LiteralPath $key -Name $name -PropertyType DWord -Value $value -Force
        }
        Write-Output 'Tema guardado. Algunas aplicaciones necesitan reiniciarse o cerrar sesion.'
    }
} catch { Write-Error $_; exit 1 }
