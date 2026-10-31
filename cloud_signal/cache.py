from __future__ import annotations

import hashlib
import json
import logging
import os
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

import pandas as pd

from cloud_signal.paths import PROJECT_ROOT

logger = logging.getLogger(__name__)

_METRICS: Counter[str] = Counter()
_METRICS_LOCK = Lock()


def cache_root() -> Path:
    configured = os.environ.get("CLOUD_SIGNAL_CACHE_DIR")
    root = Path(configured) if configured else PROJECT_ROOT / ".cache" / "cloud_signal"
    if not root.is_absolute():
        root = PROJECT_ROOT / root
    return root


def frame_fingerprint(data: pd.DataFrame) -> str:
    digest = hashlib.sha256()
    digest.update(repr(tuple(data.columns)).encode("utf-8"))
    digest.update(repr(tuple(str(dtype) for dtype in data.dtypes)).encode("utf-8"))
    digest.update(pd.util.hash_pandas_object(data, index=True).values.tobytes())
    return digest.hexdigest()


def _identity_directory(namespace: str, identity: str) -> Path:
    identity_hash = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return cache_root() / namespace / identity_hash


def _prune_versions(directory: Path, version: str, keep: str) -> None:
    for path in directory.glob(f"{version}-*.csv"):
        if path.name != keep:
            path.unlink(missing_ok=True)


def _write_frame(path: Path, data: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".tmp", dir=path.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        data.to_csv(temporary_path, index=True, float_format="%.17g")
        os.replace(temporary_path, path)
        _record("cache.bytes_written", path.stat().st_size)
    finally:
        temporary_path.unlink(missing_ok=True)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".tmp", dir=path.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
        json.dump(payload, temporary, sort_keys=True)
    try:
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _read_frame(path: Path, index: pd.Index | None = None) -> pd.DataFrame | None:
    try:
        data = pd.read_csv(path, index_col=0)
    except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError):
        logger.warning("Ignoring unreadable cache entry %s", path, exc_info=True)
        return None
    _record("cache.bytes_read", path.stat().st_size)
    if index is not None:
        if len(data) != len(index):
            logger.warning("Ignoring cache entry with mismatched rows: %s", path)
            return None
        data.index = index
    return data


def _restore_dtypes(data: pd.DataFrame, metadata: dict[str, Any]) -> None:
    dtypes = metadata.get("dtypes")
    if not isinstance(dtypes, list) or len(dtypes) != len(data.columns):
        return
    for column, dtype in zip(data.columns, dtypes):
        try:
            data[column] = data[column].astype(dtype)
        except (TypeError, ValueError):
            logger.warning(
                "Unable to restore cached dtype %s for column %s",
                dtype,
                column,
            )


def _record(name: str, amount: int = 1) -> None:
    with _METRICS_LOCK:
        _METRICS[name] += amount


def record_metric(name: str, amount: int = 1) -> None:
    _record(name, amount)


def get_cached_dataframe(
    namespace: str,
    identity: str,
    source: pd.DataFrame,
    version: str,
) -> pd.DataFrame | None:
    fingerprint = frame_fingerprint(source)
    path = (
        _identity_directory(namespace, identity)
        / f"{version}-{fingerprint}.csv"
    )
    if not path.is_file():
        _record(f"{namespace}.miss")
        return None
    cached = _read_frame(path, source.index)
    if cached is None:
        _record(f"{namespace}.miss")
        return None
    metadata_path = path.parent / "latest.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.warning(
            "Ignoring cache entry without readable metadata: %s",
            metadata_path,
            exc_info=True,
        )
        _record(f"{namespace}.miss")
        return None
    if (
        metadata.get("version") != version
        or metadata.get("file") != path.name
    ):
        _record(f"{namespace}.miss")
        return None
    _restore_dtypes(cached, metadata)
    _record(f"{namespace}.hit")
    return cached


def get_latest_dataframe(
    namespace: str, identity: str, version: str
) -> tuple[pd.DataFrame, dict[str, Any]] | None:
    directory = _identity_directory(namespace, identity)
    metadata_path = directory / "latest.json"
    if not metadata_path.is_file():
        return None
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.warning("Ignoring unreadable cache metadata %s", metadata_path, exc_info=True)
        return None
    if metadata.get("version") != version:
        return None
    filename = metadata.get("file")
    if (
        not isinstance(filename, str)
        or Path(filename).name != filename
        or not filename.startswith(f"{version}-")
    ):
        logger.warning("Ignoring invalid cache filename in %s", metadata_path)
        return None
    data_path = directory / filename
    if not data_path.is_file():
        return None
    data = _read_frame(data_path)
    if data is None:
        return None
    _restore_dtypes(data, metadata)
    if metadata.get("index_type") == "DatetimeIndex":
        data.index = pd.to_datetime(data.index, utc=True, errors="coerce")
    if metadata.get("index_name"):
        data.index.name = metadata["index_name"]
    return data, metadata


def save_cached_dataframe(
    namespace: str,
    identity: str,
    source: pd.DataFrame,
    result: pd.DataFrame,
    version: str,
) -> None:
    fingerprint = frame_fingerprint(source)
    directory = _identity_directory(namespace, identity)
    filename = f"{version}-{fingerprint}.csv"
    data_path = directory / filename
    if not data_path.is_file():
        _write_frame(data_path, result)
        _record(f"{namespace}.write")
    _write_json(
        directory / "latest.json",
        {
            "version": version,
            "source_fingerprint": fingerprint,
            "file": filename,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "index_type": type(result.index).__name__,
            "index_name": result.index.name,
            "dtypes": [str(dtype) for dtype in result.dtypes],
        },
    )
    _prune_versions(directory, version, filename)


def save_latest_dataframe(
    namespace: str,
    identity: str,
    data: pd.DataFrame,
    version: str,
    *,
    fetched_at: datetime | None = None,
) -> None:
    directory = _identity_directory(namespace, identity)
    fingerprint = frame_fingerprint(data)
    filename = f"{version}-{fingerprint}.csv"
    data_path = directory / filename
    if not data_path.is_file():
        _write_frame(data_path, data)
        _record(f"{namespace}.write")
    _write_json(
        directory / "latest.json",
        {
            "version": version,
            "source_fingerprint": fingerprint,
            "file": filename,
            "fetched_at": (fetched_at or datetime.now(timezone.utc)).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "index_type": type(data.index).__name__,
            "index_name": data.index.name,
            "dtypes": [str(dtype) for dtype in data.dtypes],
        },
    )
    _prune_versions(directory, version, filename)


def log_cache_metrics() -> None:
    with _METRICS_LOCK:
        metrics = sorted(_METRICS.items())
        _METRICS.clear()
    if not metrics:
        return
    logger = logging.getLogger("cloud_signal.cache")
    logger.info(
        "Cache and workload metrics: %s",
        ", ".join(f"{name}={value}" for name, value in metrics),
    )
