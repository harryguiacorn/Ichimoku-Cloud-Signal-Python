from src.mvc.DataPandasMVC import Control, Model, View


def main(fetchDailyDate = True, fetchWeeklyData = False):
    if fetchDailyDate:
        _model = Model('data/dowjones30/d/', 'asset_list/DowJones30.csv',
                    'd', 365, True)
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model('data/dowjones30/w/', 'asset_list/DowJones30.csv',
                    'w', 52, True)
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()

if __name__ == "__main__":
    main()