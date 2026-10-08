#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$ROOT/.." && pwd)"
OUTPUT="$PROJECT_ROOT/releases/Instalar-Apex-Combate-Windows.exe"
GO_BINARY="${GO_BINARY:-go}"
RSRC_VERSION="v0.10.2"

for command in "$GO_BINARY" awk sha256sum; do
  if ! command -v "$command" >/dev/null 2>&1; then
    printf 'Comando obrigatório ausente: %s\n' "$command" >&2
    exit 1
  fi
done

cd "$ROOT"
"$GO_BINARY" run "github.com/akavel/rsrc@$RSRC_VERSION" \
  -ico apex.ico \
  -manifest apex.manifest \
  -arch amd64 \
  -o rsrc_windows_amd64.syso

mkdir -p "$PROJECT_ROOT/releases"
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 "$GO_BINARY" build \
  -buildvcs=false \
  -trimpath \
  -ldflags='-H windowsgui -s -w' \
  -o "$OUTPUT" \
  .

CHECKSUM="$(sha256sum "$OUTPUT" | awk '{print $1}')"
printf '%s  %s\n' "$CHECKSUM" "$(basename "$OUTPUT")" | tee "$OUTPUT.sha256"
printf '\nInstalador Windows gerado: %s\n' "$OUTPUT"
