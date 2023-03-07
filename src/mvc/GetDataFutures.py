from src.mvc.DataPandasMVC import Control, Model, View

def main(fetchDailyDate = True, fetchWeeklyData = False):
    if fetchDailyDate:
        _model = Model('data/futures/d/', 'asset_list/Futures.csv',
                    '1d', '3mo', True)
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model('data/futures/w/', 'asset_list/Futures.csv',
                    '1wk', '1y', True)   
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()

if __name__ == "__main__":
    main()