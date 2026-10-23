from types import SimpleNamespace

import pandas as pd

from cloud_signal.runners import runMajorETFs


def test_timeframe_runner_loads_market_data_once_before_processing_symbols(
    tmp_path, monkeypatch
):
    symbols = ["ONE", "TWO"]
    raw_data = pd.DataFrame({"Close": [1.0]})
    ichimoku_data = pd.DataFrame({"Close": [1.0], "tenkan_sen": [1.0]})
    load_calls = []
    processed = []
    signals = []

    class FakeMarketDataControl:
        def __init__(self, model, view):
            self.model = SimpleNamespace(
                getDataOHLC=lambda: (
                    load_calls.append("loaded")
                    or {symbol: raw_data for symbol in symbols}
                )
            )

        def getAssetList(self):
            return symbols

        def process_data(self, symbol, data):
            processed.append((symbol, data))
            return ichimoku_data

    class FakeSignalControl:
        def __init__(self, model, view):
            pass

        def process_dataframe(self, symbol, data):
            signals.append((symbol, data))

    class FakeAggregatorControl:
        def __init__(self, model, view):
            pass

        def main(self):
            pass

    monkeypatch.setattr(
        runMajorETFs, "MarketDataControl", FakeMarketDataControl
    )
    monkeypatch.setattr(
        runMajorETFs, "CloudSignalControl", FakeSignalControl
    )
    monkeypatch.setattr(
        runMajorETFs, "TKxSignalControl", FakeSignalControl
    )
    monkeypatch.setattr(
        runMajorETFs, "ChikouSignalControl", FakeSignalControl
    )
    monkeypatch.setattr(
        runMajorETFs, "CloudAggregatorControl", FakeAggregatorControl
    )
    monkeypatch.setattr(
        runMajorETFs, "TKxAggregatorControl", FakeAggregatorControl
    )
    monkeypatch.setattr(
        runMajorETFs, "ChikouAggregatorControl", FakeAggregatorControl
    )
    monkeypatch.setattr(
        runMajorETFs, "ASSET_LIST", str(tmp_path / "assets.csv")
    )

    runMajorETFs._run_timeframe(
        "D", "d", "1d", "max", "1D", False
    )

    assert load_calls == ["loaded"]
    assert [symbol for symbol, _ in processed] == symbols
    assert len(signals) == len(symbols) * 3


def test_major_etfs_selects_timeframes_and_rejects_unknown_values():
    selected = runMajorETFs._select_timeframes(["D", "1h"])

    assert [timeframe[0] for timeframe in selected] == ["1H", "D"]
    try:
        runMajorETFs._select_timeframes(["quarterly"])
    except ValueError as error:
        assert "quarterly" in str(error)
    else:
        raise AssertionError("Unknown timeframe should be rejected")


def test_partial_major_etfs_run_skips_multitimeframe_merges(monkeypatch):
    processed = []
    merged = []
    monkeypatch.setattr(
        runMajorETFs,
        "_run_timeframe",
        lambda *timeframe: processed.append(timeframe[0]),
    )
    monkeypatch.setattr(
        runMajorETFs, "_merge_cloud_and_tkx", lambda: merged.append("cloud")
    )
    monkeypatch.setattr(
        runMajorETFs, "_merge_chikou", lambda: merged.append("chikou")
    )

    runMajorETFs.main(["1h", "d"])

    assert processed == ["1H", "D"]
    assert merged == []


def test_chikou_final_merge_is_written_to_sum_directory(monkeypatch):
    captured = {}

    class FakeMergerModel:
        def __init__(
            self,
            input_paths,
            output_path,
            direction_count_names,
            score_names,
            title,
        ):
            captured["input_paths"] = input_paths
            captured["output_path"] = output_path
            captured["title"] = title

    class FakeMergerControl:
        def __init__(self, model, view):
            captured["model"] = model

        def main(self):
            pass

    monkeypatch.setattr(
        runMajorETFs, "ChikouMergerModel", FakeMergerModel
    )
    monkeypatch.setattr(
        runMajorETFs, "ChikouMergerControl", FakeMergerControl
    )

    runMajorETFs._merge_chikou()

    assert (
        captured["output_path"]
        == "output/sum/MajorETFs-chikou-merged.csv"
    )
    assert all(
        path.startswith("output/chikou/")
        for path in captured["input_paths"]
    )
