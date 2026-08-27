#!/usr/bin/env python3
"""Validate asset_list CSV files for malformed or empty symbols.

Exit code 0 on success, 1 if any invalid rows found.
"""

import csv
from pathlib import Path


def validate_asset_list(path: Path):
    invalid_rows = []
    if not path.exists():
        return [(str(path), "file_not_found")]

    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if "symbol" not in reader.fieldnames:
            return [(str(path), "missing_symbol_column")]

        for i, row in enumerate(reader, start=2):
            sym = row.get("symbol")
            if sym is None:
                invalid_rows.append((i, row))
                continue
            sym_text = str(sym).strip()
            # treat empty, whitespace-only, or nan-like symbols as invalid
            if sym_text == "" or sym_text.lower().startswith("nan"):
                invalid_rows.append((i, row))

    return invalid_rows


def main():
    base = Path("asset_list")
    if not base.exists():
        print("No asset_list directory found; skipping validation.")
        return 0

    any_invalid = False
    for csv_path in sorted(base.glob("*.csv")):
        invalids = validate_asset_list(csv_path)
        if invalids:
            any_invalid = True
            print(f"Invalid rows in {csv_path}:")
            for entry in invalids:
                print(f"  {entry}")

    if any_invalid:
        print("Asset list validation failed.")
        return 1

    print("Asset list validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
