from src.mvc.core.DataKijunSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/dowjones30/1h/",
            "asset_list/DowJones30.csv",
            "output/kijun/",
            "DowJones30-kijun-1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/dowjones30/d/",
            "asset_list/DowJones30.csv",
            "output/kijun/",
            "DowJones30-kijun-D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/dowjones30/w/",
            "asset_list/DowJones30.csv",
            "output/kijun/",
            "DowJones30-kijun-W",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/dowjones30/m/",
            "asset_list/DowJones30.csv",
            "output/kijun/",
            "DowJones30-kijun-M",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
