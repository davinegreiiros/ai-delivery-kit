#!/usr/bin/env bash
# ai-delivery-kit — instalador para macOS/Linux (bash 3.2+).
#
# Uso local (a partir de um clone):
#   ./install.sh [--client all|claude|agents|codex|gemini|copilot|cursor] [--project DIR] [--uninstall]
# Uso remoto (clona em ~/.ai-delivery-kit e instala):
#   curl -fsSL https://raw.githubusercontent.com/davinegreiiros/ai-delivery-kit/main/install.sh | bash
#   curl -fsSL .../install.sh | bash -s -- --client claude
#
# Destinos:
#   claude  -> ~/.claude/skills   (Claude Code)
#   agents  -> ~/.agents/skills   (Codex, Gemini CLI/Antigravity, GitHub Copilot, Cursor)
#   --project DIR copia as skills para DIR/.claude/skills e DIR/.agents/skills (para versionar no projeto).
set -euo pipefail

REPO_URL="${AI_KIT_REPO:-https://github.com/davinegreiiros/ai-delivery-kit.git}"
KIT_HOME="${AI_KIT_HOME:-$HOME/.ai-delivery-kit}"
MARKER=".ai-delivery-kit"
CLIENT="all"
PROJECT=""
UNINSTALL=0
UPDATE=0

usage() { sed -n 2,15p "$0" 2>/dev/null | sed 's/^# \{0,1\}//'; }
log() { printf '%s\n' "$*"; }
warn() { printf 'aviso: %s\n' "$*" >&2; }
die() { printf 'erro: %s\n' "$*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --client) CLIENT="${2:-}"; [ -n "$CLIENT" ] || die "informe o cliente"; shift 2 ;;
    --project) PROJECT="${2:-}"; [ -n "$PROJECT" ] || die "informe o diretório"; shift 2 ;;
    --uninstall) UNINSTALL=1; shift ;;
    --update) UPDATE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "opção desconhecida: $1 (use --help)" ;;
  esac
done

# 1. Localizar a raiz do kit: clone atual ou cópia gerenciada em KIT_HOME.
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi
if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/skills" ]; then
  KIT_ROOT="$SCRIPT_DIR"
else
  command -v git >/dev/null 2>&1 || die "git é necessário para a instalação remota"
  if [ -d "$KIT_HOME/.git" ]; then
    log "atualizando $KIT_HOME"
    git -C "$KIT_HOME" pull --ff-only --quiet
  elif [ -e "$KIT_HOME" ]; then
    die "$KIT_HOME existe e não é um clone do kit; defina AI_KIT_HOME para outro local"
  else
    log "clonando $REPO_URL em $KIT_HOME"
    git clone --depth 1 --quiet "$REPO_URL" "$KIT_HOME"
  fi
  KIT_ROOT="$KIT_HOME"
fi
if [ "$UPDATE" -eq 1 ] && [ -d "$KIT_ROOT/.git" ]; then
  git -C "$KIT_ROOT" pull --ff-only --quiet && log "kit atualizado em $KIT_ROOT"
fi

# 2. Resolver destinos.
case "$CLIENT" in
  all) targets=("$HOME/.claude/skills" "$HOME/.agents/skills") ;;
  claude) targets=("$HOME/.claude/skills") ;;
  agents|codex|gemini|antigravity|copilot|cursor) targets=("$HOME/.agents/skills") ;;
  *) die "cliente inválido: $CLIENT" ;;
esac

# 3. Instalar/remover links globais (o kit continua sendo a fonte única).
link_skills() {
  target="$1"
  mkdir -p "$target"
  for skill_dir in "$KIT_ROOT"/skills/*/; do
    src="${skill_dir%/}"
    link="$target/$(basename "$src")"
    if [ "$UNINSTALL" -eq 1 ]; then
      if [ -L "$link" ] && [ "$(readlink "$link")" = "$src" ]; then
        rm "$link" && log "removido: $link"
      fi
      continue
    fi
    if [ -L "$link" ]; then
      current="$(readlink "$link")"
      if [ "$current" != "$src" ]; then
        warn "ignorado: $link aponta para $current (remova manualmente para trocar)"
        continue
      fi
    elif [ -e "$link" ]; then
      warn "ignorado: $link já existe e não é um link deste kit"
      continue
    fi
    ln -sfn "$src" "$link"
    log "vinculado: $link"
  done
}

# 4. Copiar para um projeto (para versionar junto com o código e compartilhar com o time).
copy_skills() {
  project="$1"
  [ -d "$project" ] || die "diretório do projeto não encontrado: $project"
  for base in "$project/.claude/skills" "$project/.agents/skills"; do
    mkdir -p "$base"
    for skill_dir in "$KIT_ROOT"/skills/*/; do
      src="${skill_dir%/}"
      dest="$base/$(basename "$src")"
      if [ -e "$dest" ] && [ ! -f "$dest/$MARKER" ]; then
        warn "ignorado: $dest já existe e não foi criado pelo kit"
        continue
      fi
      rm -rf "$dest"
      if [ "$UNINSTALL" -eq 1 ]; then
        log "removido: $dest"
        continue
      fi
      cp -R "$src" "$dest"
      printf 'Copiado do ai-delivery-kit. Atualize com install.sh --project.\n' > "$dest/$MARKER"
      log "copiado: $dest"
    done
  done
}

if [ -n "$PROJECT" ]; then
  copy_skills "$PROJECT"
else
  for t in "${targets[@]}"; do link_skills "$t"; done
fi

if [ "$UNINSTALL" -eq 0 ]; then
  log ""
  log "Pronto. Abra um projeto no seu agente e peça:"
  log "  \"Prepare este repositório para o ai-delivery-kit. Não faça commit.\""
fi
