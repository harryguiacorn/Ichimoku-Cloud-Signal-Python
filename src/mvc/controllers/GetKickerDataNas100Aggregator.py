from src.mvc.core.DataKickerSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=True,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/nasdaq100/1h/",
            "asset_list/Nasdaq100.csv",
            "output/kicker/",
            "Nasdaq100-kicker-1H",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/nasdaq100/d/",
            "asset_list/Nasdaq100.csv",
            "output/kicker/",
            "Nasdaq100-kicker-D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/nasdaq100/w/",
            "asset_list/Nasdaq100.csv",
            "output/kicker/",
            "Nasdaq100-kicker-W",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/nasdaq100/m/",
            "asset_list/Nasdaq100.csv",
            "output/kicker/",
            "Nasdaq100-kicker-M",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
