import numpy as np
import pandas as pd
import pytest

from cloud_signal.mvc.core._csv_utils import (
    read_latest_signal_data,
    write_latest_row,
)
from cloud_signal.mvc.core.DataChikouSignalMVC import DataChikouSignal
from cloud_signal.mvc.core.DataCloudSignalMVC import DataCloudSignal
from cloud_signal.mvc.core.DataTKxSignalMVC import DataTKxSignal


@pytest.fixture(autouse=True)
def isolate_shared_cache(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "CLOUD_SIGNAL_CACHE_DIR", str(tmp_path / "shared-cache")
    )


def test_vectorized_cloud_counts_preserve_nan_and_zero_semantics(tmp_path):
    signal = DataCloudSignal("TEST", str(tmp_path) + "/")
    directions = pd.Series(
        [1, 1, np.nan, 1, 0, 0, -1, -1, np.nan, -1], dtype=float
    )

    assert np.allclose(
        signal.getCloudSignalCount(directions),
        [1, 2, np.nan, np.nan, 0, 0, 1, 2, np.nan, np.nan],
        equal_nan=True,
    )


def test_vectorized_tkx_counts_preserve_initial_and_nan_reset_semantics(
    tmp_path,
):
    signal = DataTKxSignal("TEST", str(tmp_path) + "/")
    directions = pd.Series(
        [1, 1, np.nan, 1, 1, 0, 0, np.nan, 0, -1, -1], dtype=float
    )

    assert signal.getTKxSignalCount(directions) == [
        0,
        1,
        0,
        1,
        2,
        0,
        0,
        0,
        0,
        1,
        2,
    ]


def test_vectorized_chikou_state_preserves_direction_through_neutral_rows(
    tmp_path,
):
    signal = DataChikouSignal("TEST", str(tmp_path) + "/")

    counts, states = signal.getChikouState(
        [1, 1, 0, np.nan, 0, -1, -1, 0, 1]
    )

    assert counts == [1, 2, 3, 4, 5, -1, -2, -3, 1]
    assert states == [
        "above chikou",
        "above chikou",
        "above chikou",
        "above chikou",
        "above chikou",
        "below chikou",
        "below chikou",
        "below chikou",
        "above chikou",
    ]


def test_vectorized_signal_counters_match_reference_loops(tmp_path):
    random = np.random.default_rng(42)
    values = random.choice([-1.0, 0.0, 1.0, 2.0, np.nan], size=500)
    cloud = DataCloudSignal("TEST", str(tmp_path) + "/")
    tkx = DataTKxSignal("TEST", str(tmp_path) + "/")
    chikou = DataChikouSignal("TEST", str(tmp_path) + "/")

    expected_cloud = []
    previous_cloud = None
    cloud_count = None
    expected_tkx = []
    previous_tkx = None
    tkx_count = None
    expected_chikou_counts = []
    expected_chikou_states = []
    chikou_direction = 0
    chikou_periods = 0

    for value in values:
        if np.isnan(value):
            cloud_count = np.nan
            tkx_count = 0
            chikou_value = 0
        else:
            if previous_cloud is None or value != previous_cloud:
                previous_cloud = value
                cloud_count = 0 if value == 0 else 1
            elif value == 0:
                cloud_count = 0
            else:
                cloud_count += 1

            if previous_tkx is None:
                previous_tkx = value
                tkx_count = 0
            elif value != previous_tkx:
                previous_tkx = value
                tkx_count = 0 if value == 0 else 1
            elif previous_tkx != 0:
                tkx_count += 1
            chikou_value = value

        expected_cloud.append(cloud_count)
        expected_tkx.append(tkx_count)
        if chikou_value in (1, -1) and chikou_value != chikou_direction:
            chikou_direction = int(chikou_value)
            chikou_periods = 1
        elif chikou_direction != 0:
            chikou_periods += 1
        else:
            chikou_periods = 0
        expected_chikou_counts.append(chikou_periods * chikou_direction)
        expected_chikou_states.append(
            chikou.getChikouStateLabel(chikou_direction)
        )

    assert np.allclose(
        cloud.getCloudSignalCount(pd.Series(values)),
        expected_cloud,
        equal_nan=True,
    )
    assert tkx.getTKxSignalCount(pd.Series(values)) == expected_tkx
    actual_chikou = chikou.getChikouState(pd.Series(values))
    assert actual_chikou == (
        expected_chikou_counts,
        expected_chikou_states,
    )


def test_unchanged_cloud_input_reuses_cached_signals_and_outputs(
    tmp_path, monkeypatch
):
    data = pd.DataFrame(
        {
            "Date": pd.date_range("2026-01-01", periods=3, freq="D"),
            "Close": [12.0, 8.0, 10.0],
            "senkou_span_a": [10.0, 9.0, 10.0],
            "senkou_span_b": [11.0, 10.0, 11.0],
        }
    )
    signal = DataCloudSignal("TEST", str(tmp_path) + "/")
    calls = []
    original = signal.getCloudDirection

    def tracking_direction(*args):
        calls.append(True)
        return original(*args)

    monkeypatch.setattr(signal, "getCloudDirection", tracking_direction)

    first = signal.process_dataframe(data)
    second = signal.process_dataframe(data)

    assert len(calls) == 1
    pd.testing.assert_frame_equal(first, second)


def test_overlapping_markets_share_cached_signals(tmp_path, monkeypatch):
    spx_dir = tmp_path / "spx500"
    russell_dir = tmp_path / "russell1000"
    spx_dir.mkdir()
    russell_dir.mkdir()
    data = pd.DataFrame(
        {
            "Date": pd.date_range("2026-01-01", periods=3, freq="D"),
            "Close": [12.0, 8.0, 10.0],
            "senkou_span_a": [10.0, 9.0, 10.0],
            "senkou_span_b": [11.0, 10.0, 11.0],
        }
    )
    first = DataCloudSignal("AAPL", str(spx_dir) + "/")
    second = DataCloudSignal("AAPL", str(russell_dir) + "/")
    calculations = []
    original = first.getCloudDirection

    def tracking_direction(*args):
        calculations.append(True)
        return original(*args)

    monkeypatch.setattr(first, "getCloudDirection", tracking_direction)
    monkeypatch.setattr(
        second, "getCloudDirection", tracking_direction
    )

    first.process_dataframe(data)
    second.process_dataframe(data)

    assert len(calculations) == 1
    assert (spx_dir / "AAPL_cloudCount.csv").is_file()
    assert (russell_dir / "AAPL_cloudCount.csv").is_file()


def test_aggregator_uses_consolidated_latest_signal_store(
    tmp_path, monkeypatch
):
    source_path = tmp_path / "TEST_cloudCount.csv"
    latest = pd.DataFrame(
        {
            "Date": ["2026-10-30"],
            "Close": [123.45],
            "Cloud Signal": [1],
            "Cloud Signal Count": [4],
        }
    )
    write_latest_row(latest, str(source_path))

    def unexpected_csv_read(*args, **kwargs):
        raise AssertionError("Aggregator should read the consolidated store")

    monkeypatch.setattr(pd, "read_csv", unexpected_csv_read)

    result = read_latest_signal_data(
        ["TEST"], str(tmp_path), "_cloudCount", "cloud"
    )

    assert result["TEST"].iloc[0].to_dict() == {
        "Date": "2026-10-30",
        "Close": 123.45,
        "Cloud Signal": 1,
        "Cloud Signal Count": 4,
    }


def test_aggregator_migrates_existing_sidecar_into_store(tmp_path):
    (tmp_path / "TEST_tkxCount_latest.csv").write_text(
        "Date,TKx Signal,TKx Signal Count\n2026-10-30,-1,-3\n",
        encoding="utf-8",
    )

    result = read_latest_signal_data(
        ["TEST"], str(tmp_path), "_tkxCount", "tkx"
    )
    (tmp_path / "TEST_tkxCount_latest.csv").unlink()

    restored = read_latest_signal_data(
        ["TEST"], str(tmp_path), "_tkxCount", "tkx"
    )

    assert result["TEST"].iloc[0]["TKx Signal Count"] == -3
    assert restored["TEST"].iloc[0]["TKx Signal Count"] == -3
