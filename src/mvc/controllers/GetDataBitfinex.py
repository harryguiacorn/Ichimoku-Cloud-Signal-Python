from src.mvc.core.bitfinex.DataPandasBitfinexMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetch4HData=False,
    fetchDailyData=False,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/bitfinex/1h/",
            "asset_list/Bitfinex.csv",
            "H1",
            "300",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetch4HData:
        # print("fetch 4h")
        _model = Model(
            "data/bitfinex/4h/",
            "asset_list/Bitfinex.csv",
            "H4",
            "10",  # "300",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/bitfinex/d/",
            "asset_list/Bitfinex.csv",
            "D",
            "300",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/bitfinex/w/",
            "asset_list/Bitfinex.csv",
            "W",
            "300",
            True,
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()
    if fetchMonthlyData:
        _model = Model(
            "data/bitfinex/m/",
            "asset_list/Bitfinex.csv",
            "M",
            "300",
            True,
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()


if __name__ == "__main__":
    main()
