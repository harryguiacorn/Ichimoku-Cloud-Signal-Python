from pathlib import Path

import pandas as pd


def write_latest_row(data: pd.DataFrame, path: str) -> None:
    source_path = Path(path)
    latest_path = source_path.with_name(
        f"{source_path.stem}_latest{source_path.suffix}"
    )
    data.tail(1).to_csv(latest_path, index=False)


def latest_csv_path(path: str) -> Path:
    source_path = Path(path)
    latest_path = source_path.with_name(
        f"{source_path.stem}_latest{source_path.suffix}"
    )
    return latest_path if latest_path.exists() else source_path
