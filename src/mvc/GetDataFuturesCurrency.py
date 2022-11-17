from src.mvc.DataPandasMVC import Control, Model, View

def main(fetchDailyDate = True, fetchWeeklyData = False):
    if fetchDailyDate:
        _model = Model('data/futurescurrency/d/', 'asset_list/FuturesCurrency.csv',
                    'd', 365, True)
        _control = Control(_model, View())
        _control.main()

    if fetchWeeklyData:
        _model = Model('data/futurescurrency/w/', 'asset_list/FuturesCurrency.csv',
                    'w', 52, True)
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()

if __name__ == "__main__":
    main()