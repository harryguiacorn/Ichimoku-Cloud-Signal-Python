from src.mvc.DataPandasMVC import Control, Model, View

def main():
    _model = Model('data/futures/d/', 'asset_list/Futures.csv',
                'd', 365, True)
    _control = Control(_model, View())
    _control.main()

    _model = Model('data/futures/w/', 'asset_list/Futures.csv',
                'w', 52, True)
    _control = Control(_model, View())
    _control.main()
    _control.showAssetList()

if __name__ == "__main__":
    main()