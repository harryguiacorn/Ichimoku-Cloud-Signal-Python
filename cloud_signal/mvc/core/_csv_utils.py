import atexit
import json
import logging
import sqlite3
from threading import RLock
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

_LATEST_SIGNAL_CONNECTIONS: dict[Path, sqlite3.Connection] = {}
_LATEST_SIGNAL_LOCK = RLock()
_SIGNAL_FILE_SUFFIXES = {
    "_cloudCount": "cloud",
    "_tkxCount": "tkx",
    "_chikouCount": "chikou",
}


def write_latest_row(data: pd.DataFrame, path: str) -> None:
    source_path = Path(path)
    latest_path = source_path.with_name(
        f"{source_path.stem}_latest{source_path.suffix}"
    )
    data.tail(1).to_csv(latest_path, index=False)
    update_latest_signal_store(data, source_path)


def _signal_type_and_symbol(path: Path) -> tuple[str, str] | None:
    for suffix, signal in _SIGNAL_FILE_SUFFIXES.items():
        if path.stem.endswith(suffix):
            return signal, path.stem[: -len(suffix)]
    return None


def _latest_signal_connection(path: Path) -> sqlite3.Connection:
    database_path = path.parent / ".latest_signals.sqlite3"
    with _LATEST_SIGNAL_LOCK:
        connection = _LATEST_SIGNAL_CONNECTIONS.get(database_path)
        if connection is None:
            database_path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(database_path, timeout=30)
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS latest_signals (
                    signal TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    PRIMARY KEY (signal, symbol)
                )
                """
            )
            connection.commit()
            _LATEST_SIGNAL_CONNECTIONS[database_path] = connection
        return connection


def update_latest_signal_store(data: pd.DataFrame, path: Path) -> None:
    identity = _signal_type_and_symbol(path)
    if identity is None or data.empty:
        return
    signal, symbol = identity
    latest = data.tail(1).copy()
    for column in latest.columns:
        if pd.api.types.is_datetime64_any_dtype(latest[column]):
            latest[column] = latest[column].astype(str)
    payload = latest.to_json(
        orient="records", date_format="iso", double_precision=15
    )
    connection = _latest_signal_connection(path)
    with _LATEST_SIGNAL_LOCK:
        connection.execute(
            """
            INSERT INTO latest_signals (signal, symbol, payload)
            VALUES (?, ?, ?)
            ON CONFLICT(signal, symbol) DO UPDATE SET payload = excluded.payload
            """,
            (signal, symbol, payload),
        )


def read_latest_signal_data(
    symbols: list[str], csv_path: str, suffix: str, signal: str
) -> dict[str, pd.DataFrame]:
    directory = Path(csv_path)
    database_path = directory / ".latest_signals.sqlite3"
    data_by_symbol: dict[str, pd.DataFrame] = {}
    if database_path.is_file():
        connection = _latest_signal_connection(
            directory / f".latest_signals{suffix}"
        )
        with _LATEST_SIGNAL_LOCK:
            connection.commit()
            rows = connection.execute(
                "SELECT symbol, payload FROM latest_signals WHERE signal = ?",
                (signal,),
            ).fetchall()
        stored = {symbol: payload for symbol, payload in rows}
        for symbol in symbols:
            payload = stored.get(str(symbol).strip())
            if payload is not None:
                try:
                    records = json.loads(payload)
                except json.JSONDecodeError:
                    logger.warning(
                        "Ignoring malformed latest signal row for %s",
                        symbol,
                        exc_info=True,
                    )
                    continue
                if records:
                    data_by_symbol[str(symbol).strip()] = pd.DataFrame(
                        records
                    )

    for symbol in symbols:
        symbol = str(symbol).strip()
        if not symbol or symbol.lower() == "nan" or symbol in data_by_symbol:
            continue
        source_path = directory / f"{symbol}{suffix}.csv"
        try:
            data = pd.read_csv(latest_csv_path(str(source_path)))
        except FileNotFoundError:
            logger.info("Latest signal file not found: %s", source_path)
            continue
        if data.empty:
            continue
        data_by_symbol[symbol] = data
        update_latest_signal_store(data, source_path)
    if database_path.is_file():
        connection = _latest_signal_connection(
            directory / f".latest_signals{suffix}"
        )
        with _LATEST_SIGNAL_LOCK:
            connection.commit()
    return data_by_symbol


def latest_csv_path(path: str) -> Path:
    source_path = Path(path)
    latest_path = source_path.with_name(
        f"{source_path.stem}_latest{source_path.suffix}"
    )
    return latest_path if latest_path.exists() else source_path


@atexit.register
def _close_latest_signal_connections() -> None:
    with _LATEST_SIGNAL_LOCK:
        for connection in _LATEST_SIGNAL_CONNECTIONS.values():
            connection.close()
        _LATEST_SIGNAL_CONNECTIONS.clear()
