from pathlib import Path

import pandas as pd

from cloud_signal.cache import get_cached_dataframe, save_cached_dataframe

SIGNAL_CACHE_VERSION = "signal-v1"


def _identity(signal: str, symbol: str) -> str:
    return f"{symbol.strip().upper()}::{signal}"


def get_cached_signal(
    signal: str, output_dir: str, symbol: str, source: pd.DataFrame
) -> pd.DataFrame | None:
    return get_cached_dataframe(
        f"signal_{signal}",
        _identity(signal, symbol),
        source,
        SIGNAL_CACHE_VERSION,
    )


def save_cached_signal(
    signal: str,
    output_dir: str,
    symbol: str,
    source: pd.DataFrame,
    result: pd.DataFrame,
    columns: list[str],
) -> None:
    save_cached_dataframe(
        f"signal_{signal}",
        _identity(signal, symbol),
        source,
        result[columns],
        SIGNAL_CACHE_VERSION,
    )


def signal_outputs_exist(
    output_dir: str, symbol: str, suffix: str
) -> bool:
    output_path = Path(output_dir) / f"{symbol}{suffix}"
    latest_path = output_path.with_name(
        f"{output_path.stem}_latest{output_path.suffix}"
    )
    return output_path.is_file() and latest_path.is_file()
