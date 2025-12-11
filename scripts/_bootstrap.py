"""Helper for runner scripts.

Provides:
- ensure_repo_root(): make repo root importable so `from src...` works when running
  scripts directly.
- setup_runner_logging(module_name, runner_class=None, log_dir='output/logs'):
  configures root logger to log to console and to a file named after the runner.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Optional


def ensure_repo_root() -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(here, ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    return repo_root


def setup_runner_logging(
    module_name: Optional[str] = None,
    runner_class: Optional[object] = None,
    log_dir: str = "output/logs",
) -> str:
    """Configure logging to console and file for a runner.

    - module_name: full module name (e.g. 'scripts.runDJ30'). If omitted, will
      attempt to infer from __name__ of the caller.
    - runner_class: optional class or class-name to associate with the log filename.
    Returns the path to the log file.
    """
    if module_name:
        short = module_name.split(".")[-1]
    else:
        short = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    class_suffix = ""
    if runner_class:
        if isinstance(runner_class, type):
            class_suffix = f"_{runner_class.__name__}"
        else:
            class_suffix = f"_{str(runner_class)}"

    os.makedirs(log_dir, exist_ok=True)
    filename = os.path.join(log_dir, f"{short}{class_suffix}.txt")

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # remove existing handlers to avoid duplicate logs when re-imported
    for h in list(root.handlers):
        root.removeHandler(h)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    # open the log file in write mode so each run overwrites previous logs
    fh = logging.FileHandler(filename, mode="w", encoding="utf-8")
    fh.setFormatter(fmt)

    root.addHandler(sh)
    root.addHandler(fh)

    return filename
