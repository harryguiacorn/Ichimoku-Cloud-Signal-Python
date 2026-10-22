import warnings

import pandas as pd

from cloud_signal.mvc.core.DataChikouSignalMVC import (
    Control as ChikouSignalControl,
    Model as ChikouSignalModel,
    View as ChikouSignalView,
)
from cloud_signal.mvc.core.DataCloudSignalMVC import (
    Control as CloudSignalControl,
    Model as CloudSignalModel,
    View as CloudSignalView,
)
from cloud_signal.mvc.core.DataPandasMVC import (
    Control as MarketDataControl,
    Model as MarketDataModel,
    View as MarketDataView,
)
from cloud_signal.mvc.core.DataTKxSignalMVC import (
    Control as TKxSignalControl,
    Model as TKxSignalModel,
    View as TKxSignalView,
)


def test_yahoo_download_refreshes_and_merges_local_cache(tmp_path, monkeypatch):
    dates = pd.date_range("2025-01-01", periods=3, freq="D")
    pd.DataFrame(
        {"Close": [10.0, 11.0, 12.0]}, index=dates
    ).to_csv(tmp_path / "TEST.csv")

    downloaded_dates = pd.date_range("2025-01-02", periods=3, freq="D")
    downloaded = pd.DataFrame(
        {"Close": [20.0, 21.0, 22.0]}, index=downloaded_dates
    )
    calls = []

    def fake_download(**kwargs):
        calls.append(kwargs)
        return downloaded

    monkeypatch.setattr(
        "cloud_signal.mvc.core.DataPandasMVC.yf.download", fake_download
    )
    model = MarketDataModel(str(tmp_path) + "/", "assets.csv", "1d", "max", True)

    result = model.getLatestDataFromYahooByYFinance(["TEST"], "max", "1d")

    assert calls[0]["start"] == "2024-12-20"
    assert "period" not in calls[0]
    assert len(result["TEST"]) == 4
    assert (
        result["TEST"]
        .loc[pd.Timestamp("2025-01-02", tz="UTC"), "Close"]
        == 20.0
    )


def test_yahoo_download_batches_symbols_and_saves_each_cache(
    tmp_path, monkeypatch
):
    dates = pd.date_range("2025-01-01", periods=2, freq="D")
    columns = pd.MultiIndex.from_product(
        [["TEST1", "TEST2"], ["Close", "Open"]]
    )
    downloaded = pd.DataFrame(
        [[10.0, 9.0, 20.0, 19.0], [11.0, 10.0, 21.0, 20.0]],
        index=dates,
        columns=columns,
    )
    calls = []

    def fake_download(**kwargs):
        calls.append(kwargs)
        return downloaded

    monkeypatch.setattr(
        "cloud_signal.mvc.core.DataPandasMVC.yf.download", fake_download
    )
    model = MarketDataModel(str(tmp_path), "assets.csv", "1d", "max", True)

    result = model.getLatestDataFromYahooByYFinance(
        ["TEST1", "TEST2"], "max", "1d"
    )

    assert len(calls) == 1
    assert calls[0]["tickers"] == ["TEST1", "TEST2"]
    assert set(result) == {"TEST1", "TEST2"}
    assert result["TEST1"]["Close"].tolist() == [10.0, 11.0]
    assert result["TEST2"]["Close"].tolist() == [20.0, 21.0]
    assert (tmp_path / "TEST1.csv").exists()
    assert (tmp_path / "TEST2.csv").exists()


def test_yahoo_batch_keeps_cached_data_when_ticker_missing(
    tmp_path, monkeypatch
):
    dates = pd.date_range("2025-01-01", periods=2, freq="D")
    pd.DataFrame({"Close": [10.0, 11.0]}, index=dates).to_csv(
        tmp_path / "TEST1.csv"
    )
    downloaded = pd.DataFrame(
        [[12.0]],
        index=pd.DatetimeIndex(["2025-01-03"]),
        columns=pd.MultiIndex.from_product([["TEST1"], ["Close"]]),
    )

    monkeypatch.setattr(
        "cloud_signal.mvc.core.DataPandasMVC.yf.download",
        lambda **kwargs: downloaded,
    )
    model = MarketDataModel(str(tmp_path), "assets.csv", "1d", "max", True)

    result = model.getLatestDataFromYahooByYFinance(
        ["TEST1", "TEST2"], "max", "1d"
    )

    assert result["TEST1"]["Close"].tolist() == [10.0, 11.0, 12.0]
    assert "TEST2" not in result


def test_market_data_controller_returns_calculated_and_saved_frame(
    tmp_path, monkeypatch
):
    model = MarketDataModel(str(tmp_path), "assets.csv")
    raw_data = pd.DataFrame({"Close": [1.0]})
    ichimoku_data = pd.DataFrame({"tenkan_sen": [1.0]})
    saved = []
    monkeypatch.setattr(
        model, "getSymbolData", lambda symbol: raw_data
    )
    monkeypatch.setattr(
        model, "calculateIchimokuData", lambda data: ichimoku_data
    )
    monkeypatch.setattr(
        model,
        "saveIchimokuData",
        lambda symbol, data: saved.append((symbol, data)),
    )
    controller = MarketDataControl(model, MarketDataView())

    result = controller.process_symbol("TEST")

    assert result is ichimoku_data
    assert saved == [("TEST", ichimoku_data)]


def test_market_data_controller_exposes_named_datetime_index_for_handoff(
    tmp_path, monkeypatch
):
    model = MarketDataModel(str(tmp_path), "assets.csv")
    raw_data = pd.DataFrame({"Close": [1.0]})
    ichimoku_data = pd.DataFrame(
        {
            "Close": [10.0],
            "senkou_span_a": [9.0],
            "senkou_span_b": [8.0],
        },
        index=pd.DatetimeIndex(["2025-01-01"], name="Datetime"),
    )
    monkeypatch.setattr(model, "getSymbolData", lambda symbol: raw_data)
    monkeypatch.setattr(
        model, "calculateIchimokuData", lambda data: ichimoku_data
    )
    monkeypatch.setattr(model, "saveIchimokuData", lambda symbol, data: None)
    controller = MarketDataControl(model, MarketDataView())

    result = controller.process_symbol("TEST")

    assert result is not ichimoku_data
    assert result["Datetime"].tolist() == [
        pd.Timestamp("2025-01-01")
    ]
    cloud_control = CloudSignalControl(
        CloudSignalModel(str(tmp_path) + "/", "assets.csv", True),
        CloudSignalView(),
    )
    cloud_control.process_dataframe("TEST", result)
    assert (tmp_path / "TEST_cloudCount.csv").exists()


def test_market_data_cache_reads_yfinance_multirow_headers(tmp_path):
    path = tmp_path / "TEST.csv"
    dates = pd.date_range("2025-01-01", periods=2, freq="D")
    data = pd.DataFrame(
        [[10.0, 11.0], [12.0, 13.0]],
        index=dates,
        columns=pd.MultiIndex.from_product(
            [["Close", "Open"], ["TEST"]]
        ),
    )
    data.to_csv(path)

    cached = MarketDataModel._read_market_data_cache(str(path), "TEST")

    assert cached.columns.tolist() == ["Close", "Open"]
    assert cached["Close"].tolist() == [10.0, 12.0]


def test_market_data_cache_normalizes_mixed_timezone_offsets(tmp_path):
    path = tmp_path / "TEST.csv"
    path.write_text(
        "Datetime,Close\n"
        "2025-11-02 01:30:00-04:00,10\n"
        "2025-11-02 01:30:00-05:00,11\n",
        encoding="utf-8",
    )

    cached = MarketDataModel._read_market_data_cache(str(path), "TEST")

    assert str(cached.index.tz) == "UTC"
    assert cached["Close"].tolist() == [10, 11]
    assert cached.index.is_monotonic_increasing


def test_market_data_cache_does_not_warn_for_mixed_datetime_formats(
    tmp_path,
):
    path = tmp_path / "TEST.csv"
    path.write_text(
        "Datetime,Close\n"
        "2025-01-01 00:00:00+00:00,10\n"
        "2025-01-02T00:00:00Z,11\n"
        "2025/01/03,12\n",
        encoding="utf-8",
    )

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        cached = MarketDataModel._read_market_data_cache(str(path), "TEST")

    assert not captured
    assert cached["Close"].tolist() == [10, 11, 12]
    assert cached.index.is_monotonic_increasing


def test_signal_vector_calculations_keep_expected_values(tmp_path):
    from cloud_signal.mvc.core.DataChikouSignalMVC import DataChikouSignal
    from cloud_signal.mvc.core.DataCloudSignalMVC import DataCloudSignal
    from cloud_signal.mvc.core.DataTKxSignalMVC import DataTKxSignal

    cloud = DataCloudSignal("TEST", str(tmp_path) + "/")
    tkx = DataTKxSignal("TEST", str(tmp_path) + "/")
    chikou = DataChikouSignal("TEST", str(tmp_path) + "/")

    assert cloud.getCloudDirection(
        pd.Series([12, 8, 10, 10]),
        pd.Series([10, 10, 10, float("nan")]),
        pd.Series([11, 9, 11, 11]),
    ) == [1, -1, 0, 0]
    assert tkx.getTKxDirection(
        pd.Series([float("nan"), 3, 3, 1, float("nan"), 2]),
        pd.Series([1, 2, 3, 2, 1, 2]),
    ) == [0, 1, 1, -1, 0, -1]
    assert chikou.getChikouSignal(
        pd.Series([10, 11, 12, 8]),
        pd.Series([9, 10, 11, 10]),
        pd.Series([7, 9, 9, 9]),
        kijun_period=2,
    ) == [0, 0, 1, -1]


def test_kijun_and_kicker_vector_calculations_keep_loop_semantics(tmp_path):
    import numpy as np

    from cloud_signal.mvc.core.DataKijunSignalMVC import DataKijunSignal
    from cloud_signal.mvc.core.DataKickerSignalMVC import DataKickerSignal

    kijun = DataKijunSignal("TEST", str(tmp_path) + "/")
    direction = kijun.getKijunDirection(
        pd.Series([1, 2, 2, 1, 1, 2], dtype=float),
        pd.Series([np.nan, 1, 2, 2, 1, np.nan], dtype=float),
    )
    assert np.isnan(direction[0])
    assert direction[1:5] == [1.0, 1.0, -1.0, -1.0]
    assert np.isnan(direction[5])

    kicker = DataKickerSignal("TEST", str(tmp_path) + "/")
    candles = pd.DataFrame(
        {
            "Open": [10, 11, 9, 8],
            "Close": [8, 13, 7, 9],
            "High": [11, 14, 10, 8],
            "Low": [7, 10, 6, 8],
        }
    )
    assert kicker.getKickerSignal(candles) == [0, 1, -1, 0]


def test_signal_writer_keeps_full_history_and_writes_latest_sidecar(
    tmp_path,
):
    from cloud_signal.mvc.core._csv_utils import latest_csv_path
    from cloud_signal.mvc.core.DataCloudSignalMVC import DataCloudSignal

    data = _sample_ichimoku_data()
    signal = DataCloudSignal("TEST", str(tmp_path) + "/")
    signal.process_dataframe(data)

    full_path = tmp_path / "TEST_cloudCount.csv"
    latest_path = latest_csv_path(str(full_path))
    full_history = pd.read_csv(full_path)
    latest = pd.read_csv(latest_path)

    assert len(full_history) == len(data)
    assert len(latest) == 1
    assert latest.iloc[0]["Date"] == full_history.iloc[-1]["Date"]


def _sample_ichimoku_data():
    return pd.DataFrame(
        {
            "Date": pd.date_range("2025-01-01", periods=3, freq="D"),
            "Close": [12.0, 8.0, 10.0],
            "High": [13.0, 9.0, 11.0],
            "Low": [11.0, 7.0, 9.0],
            "senkou_span_a": [10.0, 9.0, 10.0],
            "senkou_span_b": [11.0, 10.0, 11.0],
            "tenkan_sen": [3.0, 1.0, 2.0],
            "kijun_sen": [2.0, 2.0, 2.0],
            "chikou_span": [None, None, None],
        }
    )


def _signal_controllers(data_path, asset_list_path):
    return (
        CloudSignalControl(
            CloudSignalModel(data_path, asset_list_path),
            CloudSignalView(),
        ),
        TKxSignalControl(
            TKxSignalModel(data_path, asset_list_path),
            TKxSignalView(),
        ),
        ChikouSignalControl(
            ChikouSignalModel(data_path, asset_list_path),
            ChikouSignalView(),
        ),
    )


def test_in_memory_controller_pipeline_matches_standalone_file_pipeline(
    tmp_path, monkeypatch
):
    in_memory_path = tmp_path / "in_memory"
    standalone_path = tmp_path / "standalone"
    in_memory_path.mkdir()
    standalone_path.mkdir()
    asset_list_path = tmp_path / "assets.csv"
    pd.DataFrame(
        {"symbol": ["TEST"], "name": ["Test Asset"]}
    ).to_csv(asset_list_path, index=False)

    data = _sample_ichimoku_data()
    for data_path in (in_memory_path, standalone_path):
        data.to_csv(data_path / "TEST_ichimokuTapy.csv", index=False)
        pd.DataFrame({"Close": [1]}).to_csv(
            data_path / "TEST.csv", index=False
        )

    in_memory_controllers = _signal_controllers(
        str(in_memory_path) + "/", str(asset_list_path)
    )
    read_csv = pd.read_csv
    csv_reads = []

    def tracking_read_csv(*args, **kwargs):
        csv_reads.append(args[0])
        return read_csv(*args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(pd, "read_csv", tracking_read_csv)
        for controller in in_memory_controllers:
            controller.process_dataframe("TEST", data)

    assert csv_reads == []

    standalone_controllers = _signal_controllers(
        str(standalone_path) + "/", str(asset_list_path)
    )
    for controller in standalone_controllers:
        controller.main()

    for suffix in ("cloudCount", "tkxCount", "chikouCount"):
        actual = pd.read_csv(in_memory_path / f"TEST_{suffix}.csv")
        expected = pd.read_csv(standalone_path / f"TEST_{suffix}.csv")
        pd.testing.assert_frame_equal(actual, expected)

    assert pd.read_csv(in_memory_path / "TEST_cloudCount.csv")[
        "Cloud Signal"
    ].tolist() == [1, -1, 0]
    assert pd.read_csv(in_memory_path / "TEST_tkxCount.csv")[
        "TKx Signal"
    ].tolist() == [1, -1, -1]
