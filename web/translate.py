"""Burmese grapheme-to-phoneme inference helpers."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SYL_NORM = ROOT / "syl-normalizer" / "syl_normalizer.py"
SYL_DICT = ROOT / "syl-normalizer" / "filtered_dictionary.txt"
VOCAB_MY = ROOT / "data" / "vocab" / "vocab.my.yml"
VOCAB_PH = ROOT / "data" / "vocab" / "vocab.ph.yml"
MODELS_DIR = ROOT / "models"
MARIAN_DECODER = os.environ.get(
    "MARIAN_DECODER",
    shutil.which("marian-decoder") or "",
)

# checkpoints used in the experiment notebooks
MODEL_REGISTRY: list[dict[str, Any]] = [
    {
        "id": "baseline.seq2seq.myph",
        "label": "Seq2Seq · baseline · iter15000",
        "folder": "baseline.seq2seq.myph",
        "checkpoint": "model.iter15000.npz",
    },
    {
        "id": "change1.seq2seq.myph",
        "label": "Seq2Seq · change1 · iter8000",
        "folder": "change1.seq2seq.myph",
        "checkpoint": "model.iter8000.npz",
    },
    {
        "id": "change2.seq2seq.myph",
        "label": "Seq2Seq · change2 · ensemble iter7000+8000",
        "folder": "change1.seq2seq.myph",
        "ensemble": ["model.iter7000.npz", "model.iter8000.npz"],
        "weights": ["1", "1"],
    },
    {
        "id": "baseline.transformer.myph",
        "label": "Transformer · baseline · iter10000",
        "folder": "baseline.transformer.myph",
        "checkpoint": "model.iter10000.npz",
    },
    {
        "id": "change1.transformer.myph",
        "label": "Transformer · change1 · iter5000",
        "folder": "change1.transformer.myph",
        "checkpoint": "model.iter5000.npz",
    },
    {
        "id": "change2.transformer.myph",
        "label": "Transformer · change2 · ensemble iter4000+5000+6000",
        "folder": "change1.transformer.myph",
        "ensemble": ["model.iter4000.npz", "model.iter5000.npz", "model.iter6000.npz"],
        "weights": ["1", "1", "1"],
    }
]


def _checkpoint_paths(cfg: dict[str, Any]) -> list[Path]:
    folder = MODELS_DIR / cfg["folder"]
    if ensemble := cfg.get("ensemble"):
        return [folder / name for name in ensemble]
    return [folder / cfg["checkpoint"]]


def iter_required_checkpoints() -> list[Path]:
    """Unique checkpoint paths under MODELS_DIR referenced by MODEL_REGISTRY."""
    seen: set[Path] = set()
    ordered: list[Path] = []
    for cfg in MODEL_REGISTRY:
        for path in _checkpoint_paths(cfg):
            if path not in seen:
                seen.add(path)
                ordered.append(path)
    return ordered


def _get_model_config(model_id: str) -> dict[str, Any]:
    for cfg in MODEL_REGISTRY:
        if cfg["id"] == model_id:
            return cfg
    raise RuntimeError(f"unknown model: {model_id}")


def list_models() -> list[dict[str, str]]:
    """Return configured models whose checkpoint files exist on disk."""
    models: list[dict[str, str]] = []
    for cfg in MODEL_REGISTRY:
        paths = _checkpoint_paths(cfg)
        if not all(path.is_file() for path in paths):
            continue
        models.append(
            {
                "id": cfg["id"],
                "label": cfg["label"],
            }
        )
    return models


def normalize(text: str) -> str:
    """Run syllable normalizer on one line of Burmese input."""
    result = subprocess.run(
        [
            sys.executable,
            str(SYL_NORM),
            "--dictionary",
            str(SYL_DICT),
            "--frequency",
            "2",
            "--fuzzy-distance",
            "0",
        ],
        input=text.strip() + "\n",
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "normalization failed").strip()
        raise RuntimeError(err.splitlines()[-1] if err else "normalization failed")
    return result.stdout.strip()


def decode(normalized: str, model_id: str) -> str:
    """Decode normalized Burmese syllables to phonemes with marian-decoder."""
    if not MARIAN_DECODER:
        raise RuntimeError(
            "marian-decoder not found. Install Marian NMT or set MARIAN_DECODER."
        )

    cfg = _get_model_config(model_id)
    paths = _checkpoint_paths(cfg)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"model not found: {', '.join(missing)}")

    cmd = [
        MARIAN_DECODER,
        "-v",
        str(VOCAB_MY),
        str(VOCAB_PH),
        "--devices",
        "0",
        "--quiet-translation",
    ]

    if cfg.get("ensemble"):
        cmd.extend(["--models", *[str(path) for path in paths]])
        cmd.extend(["--weights", *cfg["weights"]])
    else:
        cmd.extend(["-m", str(paths[0])])

    result = subprocess.run(
        cmd,
        input=normalized + "\n",
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "decoding failed").strip()
        raise RuntimeError(err.splitlines()[-1] if err else "decoding failed")
    return result.stdout.strip()


def translate(text: str, model_id: str) -> dict[str, str]:
    """Normalize Burmese input and return phoneme translation."""
    normalized = normalize(text)
    phonemes = decode(normalized, model_id)
    return {
        "input": text.strip(),
        "normalized": normalized,
        "phonemes": phonemes,
    }
