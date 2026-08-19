import pandas as pd

from src.mvc.core.DataChikouSignalAggregatorMVC import (
    Control as AggregatorControl,
    Model as AggregatorModel,
    View as AggregatorView,
)
from src.mvc.core.DataChikouSignalMultiTimeframeMerger import (
    Control as MergerControl,
    Model as MergerModel,
    View as MergerView,
)
from src.mvc.core.DataChikouSignalMVC import DataChikouSignal


def test_chikou_uses_historical_high_low_and_neutral_freezes_state():
    model = DataChikouSignal("TEST", "")
    close = pd.Series([10, 10, 10, 10, 10, 10, 10, 10])
    high = pd.Series([9, 11, 9, 9, 9, 9, 9, 9])
    low = pd.Series([1, 1, 1, 1, 1, 1, 1, 1])

    signals = model.getChikouSignal(close, high, low, kijun_period=2)
    counts, states = model.getChikouState(signals)

    assert signals == [0, 0, 1, 0, 1, 1, 1, 1]
    assert counts == [0, 0, 1, 2, 3, 4, 5, 6]
    assert states[3] == "above chikou"


def test_chikou_opposite_confirmation_resets_streak():
    model = DataChikouSignal("TEST", "")
    signals = pd.Series([0, 1, 0, 1, -1, 0, -1])

    counts, states = model.getChikouState(signals)

    assert counts == [0, 1, 2, 3, 1, 2, 3]
    assert states == [
        "neutral chikou",
        "above chikou",
        "above chikou",
        "above chikou",
        "below chikou",
        "below chikou",
        "below chikou",
    ]


def test_chikou_aggregator_and_merger_write_csv_and_html(tmp_path):
    data_path = tmp_path / "data"
    output_path = tmp_path / "output"
    data_path.mkdir()
    asset_list = tmp_path / "assets.csv"
    asset_list.write_text("symbol,name\nTEST,Test Asset\n", encoding="utf-8")
    (data_path / "TEST_chikouCount.csv").write_text(
        "Date,Chikou Signal,Chikou Signal Count,Chikou State\n"
        "2026-08-18,1,4,above chikou\n",
        encoding="utf-8",
    )

    AggregatorControl(
        AggregatorModel(
            str(data_path),
            str(asset_list),
            str(output_path),
            "Test-chikou-D",
            "1D",
        ),
        AggregatorView(),
    ).main()

    timeframe_csv = output_path / "Test-chikou-D.csv"
    assert timeframe_csv.exists()
    assert (output_path / "Test-chikou-D.csv.html").exists()
    assert list(pd.read_csv(timeframe_csv).columns) == [
        "Date",
        "Symbol",
        "Name",
        "1D Chikou Direction",
        "1D Chikou Count",
        "1D Chikou State",
    ]

    merged_csv = output_path / "merged.csv"
    MergerControl(
        MergerModel(
            [str(timeframe_csv)],
            str(merged_csv),
            [["1D Chikou Direction", "1D Chikou Count"]],
            ["Chikou Score Sum"],
        ),
        MergerView(),
    ).main()

    assert merged_csv.exists()
    assert (output_path / "merged.csv.html").exists()
