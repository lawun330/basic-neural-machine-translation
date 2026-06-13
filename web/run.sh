#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/web"

export MARIAN_DECODER="${MARIAN_DECODER:-$(command -v marian-decoder || true)}"
export DEFAULT_MODEL="${DEFAULT_MODEL:-baseline.transformer.myph}"
export PORT="${PORT:-7860}"

if [[ -z "$MARIAN_DECODER" ]]; then
  echo "marian-decoder not found. Set MARIAN_DECODER or add it to PATH." >&2
  exit 1
fi

echo "Starting Burmese Grapheme to Phoneme UI at http://127.0.0.1:${PORT}"
exec python3 app.py