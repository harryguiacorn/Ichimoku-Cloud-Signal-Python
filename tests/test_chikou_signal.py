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

    assert counts == [0, 1, 2, 3, -1, -2, -3]
    assert states == [
        "neutral chikou",
        "above chikou",
        "above chikou",
        "above chikou",
        "below chikou",
        "below chikou",
        "below chikou",
    ]


def test_chikou_bearish_direction_has_negative_count():
    model = DataChikouSignal("TEST", "")

    counts, states = model.getChikouState(pd.Series([-1]))

    assert counts == [-1]
    assert states == ["below chikou"]


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
    html = (output_path / "merged.csv.html").read_text(encoding="utf-8")
    assert "1D Chikou Direction" not in html
    assert "1D Chikou Count" in html
    assert "1D Chikou State" in html
    assert "Chikou Score Sum" in html


def test_chikou_score_sum_uses_count_not_direction_or_state(tmp_path):
    first_path = tmp_path / "first.csv"
    second_path = tmp_path / "second.csv"
    output_path = tmp_path / "merged.csv"
    first_columns = [
        "Symbol",
        "Name",
        "1H Chikou Direction",
        "1H Chikou Count",
        "1H Chikou State",
    ]
    second_columns = [
        "Symbol",
        "Name",
        "1D Chikou Direction",
        "1D Chikou Count",
        "1D Chikou State",
    ]
    pd.DataFrame(
        [["TEST", "Test Asset", 1, 99, "below chikou"]], columns=first_columns
    ).to_csv(first_path, index=False)
    pd.DataFrame(
        [["TEST", "Test Asset", -1, 88, "above chikou"]],
        columns=second_columns,
    ).to_csv(second_path, index=False)

    MergerControl(
        MergerModel(
            [str(first_path), str(second_path)],
            str(output_path),
            [
                ["1H Chikou Direction", "1H Chikou Count"],
                ["1D Chikou Direction", "1D Chikou Count"],
            ],
            ["Chikou Score Sum"],
        ),
        MergerView(),
    ).main()

    result = pd.read_csv(output_path)
    assert result.loc[0, "Chikou Score Sum"] == 187
