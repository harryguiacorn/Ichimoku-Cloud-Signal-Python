from src.mvc.core.DataKijunSignalMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/futurescurrency/1h/", "asset_list/FuturesCurrency.csv", True
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/futurescurrency/d/", "asset_list/FuturesCurrency.csv"
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/futurescurrency/w/", "asset_list/FuturesCurrency.csv"
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/futurescurrency/m/", "asset_list/FuturesCurrency.csv"
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
