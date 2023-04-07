from src.mvc.DataTKxSignalMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/dowjones30/1h/", "asset_list/DowJones30.csv", True
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model("data/dowjones30/d/", "asset_list/DowJones30.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model("data/dowjones30/w/", "asset_list/DowJones30.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model("data/dowjones30/m/", "asset_list/DowJones30.csv")
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
