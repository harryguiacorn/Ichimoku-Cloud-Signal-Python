from src.mvc.core.DataCloudSignalMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model("data/hsi/1h/", "asset_list/HSI.csv", True)
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model("data/hsi/d/", "asset_list/HSI.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model("data/hsi/w/", "asset_list/HSI.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model("data/hsi/m/", "asset_list/HSI.csv")
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
