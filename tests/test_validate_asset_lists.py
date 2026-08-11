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


def test_read_asset_list_normalizes_symbols_and_skips_invalid(tmp_path: Path):
    from pathlib import Path
    from src.mvc.core.DataTKxSignalMVC import Model
    import os

    asset_file = tmp_path / "asset_list.csv"
    asset_file.write_text(
        "symbol,name\n"
        "AAPL,Apple Inc.\n"
        " MSFT ,Microsoft Corp.\n"
        " /GOOG,Google LLC\n"
        ",Missing\n"
        "nan,Null\n"
    )

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "AAPL.csv").write_text(
        "Date,Open,High,Low,Close\n2026-08-11,100,101,99,100"
    )
    (data_dir / "MSFT.csv").write_text(
        "Date,Open,High,Low,Close\n2026-08-11,200,201,199,200"
    )
    (data_dir / "GOOG.csv").write_text(
        "Date,Open,High,Low,Close\n2026-08-11,300,301,299,300"
    )

    model = Model(str(data_dir) + os.sep, str(asset_file))
    symbols = model.readAssetList(model.assetListPath)

    assert symbols == ["AAPL", "MSFT", "GOOG"]
    assert all(isinstance(symbol, str) for symbol in symbols)

    ohlc = model.readLocalCsvData(symbols, model.csvPath)
    assert set(ohlc.keys()) == {"AAPL", "MSFT", "GOOG"}
