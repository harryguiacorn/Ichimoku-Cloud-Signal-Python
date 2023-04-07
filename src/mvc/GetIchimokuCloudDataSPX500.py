from src.mvc.DataCloudSignalMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model("data/spx500/1h/", "asset_list/SPX500.csv", True)
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model("data/spx500/d/", "asset_list/SPX500.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model("data/spx500/w/", "asset_list/SPX500.csv")
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
