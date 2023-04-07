from src.mvc.DataKickerSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=True,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/ftse100/1h/",
            "asset_list/FTSE100.csv",
            "output/",
            "FTSE100-kicker-1H",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/ftse100/d/",
            "asset_list/FTSE100.csv",
            "output/",
            "FTSE100-kicker-D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/ftse100/w/",
            "asset_list/FTSE100.csv",
            "output/",
            "FTSE100-kicker-W",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/ftse100/m/",
            "asset_list/FTSE100.csv",
            "output/",
            "FTSE100-kicker-M",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
