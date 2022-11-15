from src.mvc.DataPandasMVC import Control, Model, View

def main():
    _model = Model('data/spx500/d/', 'asset_list/SPX500.csv',
                'd', 365, True)
    _control = Control(_model, View())
    _control.main()

    _model = Model('data/spx500/w/', 'asset_list/SPX500.csv',
                'w', 52, True)
    _control = Control(_model, View())
    _control.main()
    _control.showAssetList()

if __name__ == "__main__":
    main()