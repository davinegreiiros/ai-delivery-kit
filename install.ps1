# ai-delivery-kit — instalador para Windows PowerShell 5.1+ e PowerShell 7+.
#
# Uso local (a partir de um clone):
#   .\install.ps1 [-Client all|claude|agents|codex|gemini|copilot|cursor] [-Project DIR] [-Uninstall] [-Update]
# Uso remoto (clona em ~\.ai-delivery-kit e instala para todos os clientes):
#   irm https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.ps1 | iex
#
# Destinos:
#   claude -> ~\.claude\skills  (Claude Code)
#   agents -> ~\.agents\skills  (Codex, Gemini CLI/Antigravity, GitHub Copilot, Cursor)
# Links globais usam junctions (não exigem administrador nem modo desenvolvedor).
[CmdletBinding()]
param(
    [ValidateSet('all', 'claude', 'agents', 'codex', 'gemini', 'antigravity', 'copilot', 'cursor')]
    [string]$Client = 'all',
    [string]$Project = '',
    [switch]$Uninstall,
    [switch]$Update
)

$ErrorActionPreference = 'Stop'
$RepoUrl = if ($env:AI_KIT_REPO) { $env:AI_KIT_REPO } else { 'https://github.com/davinegreiiros/ai-delivery-kit.git' }
$KitHome = if ($env:AI_KIT_HOME) { $env:AI_KIT_HOME } else { Join-Path $HOME '.ai-delivery-kit' }
$Marker = '.ai-delivery-kit'

function Resolve-KitRoot {
    if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot 'skills'))) {
        return $PSScriptRoot
    }
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'git é necessário para a instalação remota'
    }
    if (Test-Path (Join-Path $KitHome '.git')) {
        Write-Host "atualizando $KitHome"
        git -C $KitHome pull --ff-only --quiet
    } elseif (Test-Path $KitHome) {
        throw "$KitHome existe e não é um clone do kit; defina AI_KIT_HOME para outro local"
    } else {
        Write-Host "clonando $RepoUrl em $KitHome"
        git clone --depth 1 --quiet $RepoUrl $KitHome
    }
    if ($LASTEXITCODE -ne 0) { throw 'falha ao obter o kit com git' }
    return $KitHome
}

function Get-LinkTarget([string]$Path) {
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $item -or -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { return $null }
    $target = $item.Target
    if ($target -is [array]) { $target = $target[0] }
    return [string]$target
}

function Same-Path([string]$A, [string]$B) {
    if (-not $A -or -not $B) { return $false }
    $norm = { param($p) ($p -replace '^\\\\\?\\', '').TrimEnd('\', '/').ToLowerInvariant() }
    return (& $norm $A) -eq (& $norm $B)
}

function Install-Links([string]$KitRoot, [string]$Target) {
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    foreach ($skill in Get-ChildItem -Directory (Join-Path $KitRoot 'skills')) {
        $link = Join-Path $Target $skill.Name
        $current = Get-LinkTarget $link
        if ($Uninstall) {
            if (Same-Path $current $skill.FullName) {
                (Get-Item -LiteralPath $link -Force).Delete()
                Write-Host "removido: $link"
            }
            continue
        }
        if ($current) {
            if (-not (Same-Path $current $skill.FullName)) {
                Write-Warning "ignorado: $link aponta para $current (remova manualmente para trocar)"
            }
            continue
        }
        if (Test-Path -LiteralPath $link) {
            Write-Warning "ignorado: $link já existe e não é um link deste kit"
            continue
        }
        New-Item -ItemType Junction -Path $link -Target $skill.FullName | Out-Null
        Write-Host "vinculado: $link"
    }
}

function Copy-ToProject([string]$KitRoot, [string]$ProjectDir) {
    if (-not (Test-Path -LiteralPath $ProjectDir -PathType Container)) {
        throw "diretório do projeto não encontrado: $ProjectDir"
    }
    foreach ($base in @((Join-Path $ProjectDir '.claude\skills'), (Join-Path $ProjectDir '.agents\skills'))) {
        New-Item -ItemType Directory -Force -Path $base | Out-Null
        foreach ($skill in Get-ChildItem -Directory (Join-Path $KitRoot 'skills')) {
            $dest = Join-Path $base $skill.Name
            if ((Test-Path -LiteralPath $dest) -and -not (Test-Path -LiteralPath (Join-Path $dest $Marker))) {
                Write-Warning "ignorado: $dest já existe e não foi criado pelo kit"
                continue
            }
            if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Recurse -Force }
            if ($Uninstall) { Write-Host "removido: $dest"; continue }
            Copy-Item -LiteralPath $skill.FullName -Destination $dest -Recurse
            Set-Content -LiteralPath (Join-Path $dest $Marker) -Value 'Copiado do ai-delivery-kit. Atualize com install.ps1 -Project.' -Encoding UTF8
            Write-Host "copiado: $dest"
        }
    }
}

$KitRoot = Resolve-KitRoot
if ($Update -and (Test-Path (Join-Path $KitRoot '.git'))) {
    git -C $KitRoot pull --ff-only --quiet
    Write-Host "kit atualizado em $KitRoot"
}

if ($Project) {
    Copy-ToProject $KitRoot $Project
} else {
    $targets = switch ($Client) {
        'all' { @((Join-Path $HOME '.claude\skills'), (Join-Path $HOME '.agents\skills')) }
        'claude' { @((Join-Path $HOME '.claude\skills')) }
        default { @((Join-Path $HOME '.agents\skills')) }
    }
    foreach ($t in $targets) { Install-Links $KitRoot $t }
}

if (-not $Uninstall) {
    Write-Host ''
    Write-Host 'Pronto. Abra um projeto no seu agente e peça:'
    Write-Host '  "Prepare este repositório para o ai-delivery-kit. Não faça commit."'
}
