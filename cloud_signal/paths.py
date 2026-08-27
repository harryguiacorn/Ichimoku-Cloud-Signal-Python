"""Canonical project filesystem locations."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSET_LIST_DIR = PROJECT_ROOT / "asset_list"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = OUTPUT_DIR / "logs"


def project_path(*parts: str) -> Path:
    """Return a path rooted at the project directory."""
    return PROJECT_ROOT.joinpath(*parts)
