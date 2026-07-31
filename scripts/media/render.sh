#!/usr/bin/env bash
# render.sh — render a starter tape against the real released binary in a
# staged copy of this repo's flows. Sibling of the engine's
# render-tape.sh · same honesty contract. Usage:
#   bash scripts/media/render.sh [tape-name]   (default: check-and-inspect)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
NAME="${1:-check-and-inspect}"
TAPE="$ROOT/scripts/media/$NAME.tape"
[ -f "$TAPE" ] || { echo "no tape at $TAPE" >&2; exit 1; }
command -v vhs >/dev/null || { echo "vhs not installed (brew install vhs)" >&2; exit 1; }
command -v nika >/dev/null || { echo "nika not on PATH" >&2; exit 1; }

rm -rf /tmp/starter-demo
mkdir -p /tmp/starter-demo
cp -R "$ROOT/flows" /tmp/starter-demo/flows
nika check /tmp/starter-demo/flows/daily-brief.nika.yaml >/dev/null || {
  echo "the shipped flow must check clean before it is shown" >&2
  exit 1
}

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK" /tmp/starter-demo' EXIT
cp "$TAPE" "$WORK/$NAME.tape"
(cd "$WORK" && vhs "$NAME.tape")

mkdir -p "$ROOT/media"
OUT="$ROOT/media/$NAME.gif"
if command -v gifsicle >/dev/null; then
  gifsicle -O3 --lossy=40 "$WORK/$NAME.gif" -o "$OUT"
else
  cp "$WORK/$NAME.gif" "$OUT"
fi
SIZE_MB=$(du -m "$OUT" | cut -f1)
[ "$SIZE_MB" -le 8 ] || { echo "✖ $OUT is ${SIZE_MB}MB (budget 8MB)" >&2; exit 1; }
echo "→ $OUT (${SIZE_MB}MB · budget 8MB)"
