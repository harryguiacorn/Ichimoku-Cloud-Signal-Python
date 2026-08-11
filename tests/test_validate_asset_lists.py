from pathlib import Path
from scripts.validate_asset_lists import validate_asset_list


def test_validate_asset_list_valid(tmp_path: Path):
    p = tmp_path / "asset_list.csv"
    p.write_text("symbol,name\nABC.L,Alpha\nDEF.L,Delta\n")
    invalids = validate_asset_list(p)
    assert invalids == []


def test_validate_asset_list_invalid_empty(tmp_path: Path):
    p = tmp_path / "asset_list.csv"
    p.write_text("symbol,name\n,NoSymbol\nGHI.L,Gamma\n")
    invalids = validate_asset_list(p)
    assert len(invalids) == 1


def test_validate_asset_list_invalid_nan(tmp_path: Path):
    p = tmp_path / "asset_list.csv"
    p.write_text("symbol,name\nnan.L,\n")
    invalids = validate_asset_list(p)
    assert len(invalids) == 1
