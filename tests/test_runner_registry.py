from cloud_signal.runners.market_registry import get_market_config, list_market_names


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
