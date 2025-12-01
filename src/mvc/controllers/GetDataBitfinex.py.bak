from src.mvc.core.bitfinex.DataPandasBitfinexMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetch4HData=False,
    fetchDailyData=False,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    # Time frame available values
    # Available values: "1m", "5m", "15m", "30m", "1h", "3h", "6h", "12h", "1D", "1W", "14D", "1M".

    if fetch1HData:
        _model = Model(
            "data/bitfinex/1h/",
            "asset_list/Bitfinex.csv",
            "1h",
            "10000",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetch4HData:
        # print("fetch 4h")
        _model = Model(
            "data/bitfinex/4h/",
            "asset_list/Bitfinex.csv",
            "4h",
            "10000",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/bitfinex/d/",
            "asset_list/Bitfinex.csv",
            "1D",
            "10000",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/bitfinex/w/",
            "asset_list/Bitfinex.csv",
            "1W",
            "10000",
            True,
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()
    if fetchMonthlyData:
        _model = Model(
            "data/bitfinex/m/",
            "asset_list/Bitfinex.csv",
            "1M",
            "10000",
            True,
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()


if __name__ == "__main__":
    main()
