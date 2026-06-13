#!/usr/bin/env bash
set -euo pipefail

cd /app/web

if [[ -n "${HF_MODEL_REPO:-}" ]]; then
  echo "Fetching Marian checkpoints from Hugging Face Hub: ${HF_MODEL_REPO}"
  python3 download_models.py
else
  echo "HF_MODEL_REPO not set; skipping Hub download (expect models/ mounted locally)."
fi

exec python3 app.py
