from src.mvc.DataKijunSignalMVC import Control, Model, View


def main(fetchDailyData=True, fetchWeeklyData=False):
    if fetchDailyData:
        _model = Model("data/ftse250/d/", "asset_list/FTSE250.csv")
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model("data/ftse250/w/", "asset_list/FTSE250.csv")
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
