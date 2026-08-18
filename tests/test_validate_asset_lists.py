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
        "nan.L,Bad Symbol\n"
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
    assert all(not symbol.lower().startswith("nan") for symbol in symbols)

    ohlc = model.readLocalCsvData(symbols, model.csvPath)
    assert set(ohlc.keys()) == {"AAPL", "MSFT", "GOOG"}


def test_wiki_symbol_reader_drops_blank_last_row():
    import pandas as pd
    from src.mvc.controllers.GetSymbolFTSE250 import Model

    model = Model("https://example.com", "asset_list/FTSE250.csv", "Company")
    model.df_list = pd.DataFrame(
        {
            "Company": ["Alpha", "Beta", ""],
            "Ticker": ["AAPL", "MSFT", ""],
        }
    )

    model.cleanData()

    assert list(model.df["symbol"]) == ["AAPL.L", "MSFT.L"]
    assert list(model.df["name"]) == ["Alpha", "Beta"]


def test_dow_jones_reader_does_not_depend_on_wikipedia_table_caption(
    monkeypatch,
):
    import pandas as pd
    from src.mvc.controllers.GetSymbolDowJones30 import Model

    class Response:
        text = "<html></html>"

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        "src.mvc.controllers.GetSymbolDowJones30.requests.get",
        lambda url, headers: Response(),
    )
    monkeypatch.setattr(
        "src.mvc.controllers.GetSymbolDowJones30.pd.read_html",
        lambda html: [
            pd.DataFrame({"Other": ["unrelated"], "Value": [1]}),
            pd.DataFrame({"Company": ["Alpha"], "Symbol": ["BRK.B"]}),
        ],
    )

    model = Model("https://example.com", "asset_list/DowJones30.csv")

    model.readHtml()
    model.cleanData()

    assert list(model.df["symbol"]) == ["BRK-B"]
    assert list(model.df["name"]) == ["Alpha"]
