from src.mvc.DataKijunSignalAggregatorMVC import Control, Model, View


def main(fetch1HData=False, fetchDailyData=True, fetchWeeklyData=False):
    if fetch1HData:
        _model = Model(
            "data/futures/d/",
            "asset_list/Futures.csv",
            "output/",
            "Futures-kijun-1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/futures/d/", "asset_list/Futures.csv", "output/", "Futures-kijun-D"
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/futures/w/", "asset_list/Futures.csv", "output/", "Futures-kijun-W"
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
