#!/usr/bin/env python3
"""Download Marian checkpoints from Hugging Face Hub into models/."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

from huggingface_hub import hf_hub_download
from huggingface_hub.utils import HfHubHTTPError

from translate import MODELS_DIR, iter_required_checkpoints

HUB_LAYOUTS = ("mirror", "flat")
ROOT = Path(__file__).resolve().parent.parent


def load_dotenv() -> None:
    """Load project .env into os.environ (does not override existing vars)."""
    env_file = ROOT / ".env"
    if not env_file.is_file():
        return
    try:
        from dotenv import load_dotenv as _load_dotenv
    except ImportError:
        print(
            "warning: python-dotenv not installed; .env will not be loaded. "
            "Run: pip install python-dotenv",
            file=sys.stderr,
        )
        return
    _load_dotenv(env_file, override=False)


def clean_env_value(value: str) -> str:
    """Strip whitespace and surrounding quotes from env/secret values."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


def folder_stem(folder: str) -> str:
    """Turn a local model folder name into the flat Hub name prefix."""
    if folder.endswith(".myph"):
        return folder[: -len(".myph")]
    return folder.replace("/", ".")


def hub_filename(local_path: Path, *, prefix: str = "", layout: str = "mirror") -> str:
    """Map a local models/ path to the filename on the Hub repo."""
    rel = local_path.relative_to(MODELS_DIR)
    folder = rel.parent.as_posix()
    checkpoint = rel.name

    if layout == "mirror":
        hub_rel = rel.as_posix()
    elif layout == "flat":
        stem = folder_stem(folder) if folder != "." else ""
        hub_rel = f"{stem}.{checkpoint}" if stem else checkpoint
    else:
        raise ValueError(f"unknown hub layout: {layout}")

    if prefix and not prefix.endswith("/"):
        prefix = prefix + "/"
    return f"{prefix}{hub_rel}"


def download_checkpoint(
    repo_id: str,
    local_path: Path,
    *,
    token: str | None = None,
    hub_prefix: str = "",
    hub_layout: str = "mirror",
    force: bool = False,
) -> Path:
    """Download one checkpoint if missing (or when force=True)."""
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if local_path.is_file() and not force:
        print(f"skip (exists): {local_path}")
        return local_path

    filename = hub_filename(local_path, prefix=hub_prefix, layout=hub_layout)
    print(f"downloading: {repo_id}/{filename} -> {local_path}")
    try:
        cached = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            token=token or None,
        )
    except HfHubHTTPError as exc:
        raise RuntimeError(
            f"failed to download {repo_id}/{filename}: {exc}"
        ) from exc

    shutil.copy2(cached, local_path)

    if not local_path.is_file():
        raise RuntimeError(f"download finished but file missing: {local_path}")
    return local_path


def download_all(
    repo_id: str,
    *,
    token: str | None = None,
    hub_prefix: str = "",
    hub_layout: str = "mirror",
    force: bool = False,
    only: list[str] | None = None,
) -> list[Path]:
    """Download all registry checkpoints (or a filtered subset)."""
    paths = iter_required_checkpoints()
    if only:
        wanted = set(only)
        paths = [p for p in paths if p.relative_to(MODELS_DIR).as_posix() in wanted]

    downloaded: list[Path] = []
    for local_path in paths:
        downloaded.append(
            download_checkpoint(
                repo_id,
                local_path,
                token=token,
                hub_prefix=hub_prefix,
                hub_layout=hub_layout,
                force=force,
            )
        )
    return downloaded


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Marian .npz checkpoints from Hugging Face Hub."
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("HF_MODEL_REPO", ""),
        help="Hub model repo id (e.g. username/repository). "
        "Defaults to HF_MODEL_REPO env var.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HF_TOKEN", ""),
        help="Hub read token for private repos. Defaults to HF_TOKEN env var.",
    )
    parser.add_argument(
        "--hub-prefix",
        default=os.environ.get("HF_MODEL_HUB_PREFIX", ""),
        help="Optional prefix inside the repo (e.g. checkpoints/). "
        "Defaults to HF_MODEL_HUB_PREFIX env var.",
    )
    parser.add_argument(
        "--hub-layout",
        default=os.environ.get("HF_MODEL_HUB_LAYOUT", "flat"),
        choices=HUB_LAYOUTS,
        help=(
            "How local paths map to Hub filenames. "
            "mirror: folder/checkpoint (baseline.transformer.myph/model.iter10000.npz). "
            "flat: folder_stem.checkpoint (baseline.transformer.model.iter10000.npz). "
            "Defaults to HF_MODEL_HUB_LAYOUT env var (flat)."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even when the local file already exists.",
    )
    parser.add_argument(
        "--only",
        action="append",
        metavar="REL_PATH",
        help=(
            "Download one relative path under models/ (repeatable). "
            "Example: baseline.transformer.myph/model.iter10000.npz"
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help=(
            "Show local path -> Hub filename mapping and exit. "
            "Local paths stay nested for Marian; Hub uses --hub-layout."
        ),
    )
    parser.add_argument(
        "--list-local",
        action="store_true",
        help="List local checkpoint paths only.",
    )
    return parser.parse_args()


def print_path_mapping(hub_prefix: str, hub_layout: str) -> None:
    print(f"# hub_layout={hub_layout}  hub_prefix={hub_prefix or '(none)'}")
    print("# local (models/) -> Hub filename")
    for path in iter_required_checkpoints():
        local_rel = path.relative_to(MODELS_DIR).as_posix()
        hub_rel = hub_filename(path, prefix=hub_prefix, layout=hub_layout)
        print(f"{local_rel}\t->\t{hub_rel}")


def main() -> int:
    load_dotenv()
    args = parse_args()
    args.repo = clean_env_value(args.repo)
    args.token = clean_env_value(args.token)
    args.hub_prefix = clean_env_value(args.hub_prefix)
    args.hub_layout = clean_env_value(args.hub_layout)

    if args.list:
        print_path_mapping(args.hub_prefix, args.hub_layout)
        return 0

    if args.list_local:
        for path in iter_required_checkpoints():
            print(path.relative_to(MODELS_DIR).as_posix())
        return 0

    if not args.repo:
        print(
            "error: set --repo or HF_MODEL_REPO (e.g. username/repository)",
            file=sys.stderr,
        )
        return 1

    token = args.token or None
    download_all(
        args.repo,
        token=token,
        hub_prefix=args.hub_prefix,
        hub_layout=args.hub_layout,
        force=args.force,
        only=args.only,
    )
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
