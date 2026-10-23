"""Helper for runner scripts.

Provides:
- ensure_repo_root(): make repo root importable so `from cloud_signal...` works when running
  scripts directly.
- setup_runner_logging(module_name, runner_class=None, log_dir='output/logs'):
  configures root logger to log to console and to a file named after the runner.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from functools import wraps
import logging
import os
import sys
from os import path as os_path
from time import perf_counter
from types import ModuleType
from typing import Callable, Iterable, Optional, TypeVar

from cloud_signal.paths import LOG_DIR, PROJECT_ROOT

_Result = TypeVar("_Result")


@contextmanager
def timed_stage(logger: logging.Logger, stage: str) -> Iterator[None]:
    started_at = perf_counter()
    try:
        yield
    finally:
        logger.info(
            "%s finished in %.2f seconds",
            stage,
            perf_counter() - started_at,
        )


def timed_callable(
    logger: logging.Logger,
    stage: str,
    function: Callable[..., _Result],
) -> Callable[..., _Result]:
    @wraps(function)
    def timed(*args, **kwargs):
        with timed_stage(logger, stage):
            return function(*args, **kwargs)

    return timed


def instrument_controller_mains(
    logger: logging.Logger,
    modules: Optional[Iterable[ModuleType]] = None,
) -> None:
    if modules is None:
        modules = sys.modules.values()

    for module in modules:
        module_name = getattr(module, "__name__", "")
        if not module_name.startswith("cloud_signal.mvc.controllers."):
            continue

        main = getattr(module, "main", None)
        if not callable(main) or getattr(main, "__timed_stage__", False):
            continue

        stage = f"Workflow stage {module_name}.main"
        wrapped = timed_callable(logger, stage, main)
        setattr(wrapped, "__timed_stage__", True)
        module.main = wrapped


def ensure_repo_root() -> str:
    repo_root = str(PROJECT_ROOT)
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    os.chdir(repo_root)
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
    if log_dir == "output/logs":
        log_dir = str(LOG_DIR)
    elif not os_path.isabs(log_dir):
        log_dir = str(PROJECT_ROOT / log_dir)

    if module_name:
        short = module_name.split(".")[-1]
    else:
        short = os_path.splitext(os_path.basename(sys.argv[0]))[0]

    class_suffix = ""
    if runner_class:
        if isinstance(runner_class, type):
            class_suffix = f"_{runner_class.__name__}"
        else:
            class_suffix = f"_{str(runner_class)}"

    os.makedirs(log_dir, exist_ok=True)
    filename = os_path.join(log_dir, f"{short}{class_suffix}.txt")

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Reduce noisy third-party INFO logs that clutter runner logs
    # e.g. numexpr prints a startup INFO line about thread defaults.
    logging.getLogger("numexpr").setLevel(logging.WARNING)

    instrument_controller_mains(root)

    # If logging is already configured (root has handlers), do not reconfigure.
    # This prevents individual runner modules (which call this at import time)
    # from overriding the top-level runner log file. Instead, return the
    # file path used by the existing FileHandler if present.
    if root.handlers:
        for h in root.handlers:
            if isinstance(h, logging.FileHandler):
                try:
                    return h.baseFilename
                except Exception:
                    return filename
        # Root-level shims may configure console logging before importing the
        # package runner. Add the runner file without replacing that handler.
        if any(
            type(handler) is logging.StreamHandler
            and handler.stream is sys.stderr
            for handler in root.handlers
        ):
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s: %(message)s"
            )
            file_handler = logging.FileHandler(
                filename, mode="w", encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            root.addHandler(file_handler)
            return filename
        return filename

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    # open the log file in write mode so each run overwrites previous logs
    fh = logging.FileHandler(filename, mode="w", encoding="utf-8")
    fh.setFormatter(fmt)

    root.addHandler(sh)
    root.addHandler(fh)

    return filename
