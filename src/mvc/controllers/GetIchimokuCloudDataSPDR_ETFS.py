from src.mvc.core.DataCloudSignalMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model("data/spdr_etfs/1h/", "asset_list/SPDR_ETFS.csv", True)
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model("data/spdr_etfs/d/", "asset_list/SPDR_ETFS.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model("data/spdr_etfs/w/", "asset_list/SPDR_ETFS.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model("data/spdr_etfs/m/", "asset_list/SPDR_ETFS.csv")
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
