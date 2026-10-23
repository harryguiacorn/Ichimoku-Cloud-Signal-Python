from cloud_signal.runners.market_registry import (
    get_market_config,
    list_market_names,
)
from cloud_signal.runners.run_market import _runtime_for_timeframes


def test_market_registry_contains_all_expected_runners():
    names = set(list_market_names())
    required = {
        "DJ30",
        "FTSE100",
        "FTSE250",
        "Futures",
        "HSI",
        "Nas100",
        "Oanda",
        "SPX500",
        "SPDR_ETFs",
        "Kraken",
        "CurrencyFutures",
        "Russell1000",
        "Bitfinex",
    }
    assert required.issubset(names)


def test_get_market_config_returns_named_market_data():
    config = get_market_config("FTSE250")
    assert config["name"] == "FTSE250"
    assert config["asset_list"] == "asset_list/FTSE250.csv"
    assert config["timeframes"]
    assert config["output_dir"]


def test_get_market_config_includes_runtime_runner_flags():
    config = get_market_config("FTSE250")
    runtime = config["runtime"]
    assert runtime["fetch_symbols_latest_FTSE250"] is True
    assert runtime["fetch_FTSE250_1H"] is True
    assert runtime["fetch_FTSE250_D"] is True
    assert runtime["run_Multi_TimeFrame_Merger_FTSE250"] is True


def test_selected_timeframe_disables_unselected_work_and_merge():
    config = get_market_config("SPX500")

    runtime, selected = _runtime_for_timeframes(config, ["1h", "d"])

    assert selected == {"1h", "d"}
    assert runtime["fetch_SPX500_1H"] is True
    assert runtime["fetch_SPX500_D"] is True
    assert runtime["fetch_SPX500_W"] is False
    assert runtime["fetch_SPX500_M"] is False
    assert runtime["run_Multi_TimeFrame_Merger_SPX500"] is False


def test_selected_timeframe_rejects_unknown_values():
    config = get_market_config("SPX500")

    try:
        _runtime_for_timeframes(config, ["quarterly"])
    except ValueError as error:
        assert "quarterly" in str(error)
    else:
        raise AssertionError("Unknown timeframe should be rejected")


def test_partial_timeframe_selection_requires_merge_flag():
    config = get_market_config("SPX500")
    config["runtime"].pop("run_Multi_TimeFrame_Merger_SPX500")

    try:
        _runtime_for_timeframes(config, ["1h"])
    except ValueError as error:
        assert "required for partial runs" in str(error)
    else:
        raise AssertionError("Missing merger flag should be rejected")
