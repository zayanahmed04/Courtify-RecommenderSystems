"""Utility helpers for file operations."""

from pathlib import Path
import shutil


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_copy(src: str | Path, dst: str | Path) -> None:
    ensure_dir(Path(dst).parent)
    shutil.copy2(src, dst)


def list_files(directory: str | Path, pattern: str = "*") -> list[Path]:
    return sorted(Path(directory).glob(pattern))
