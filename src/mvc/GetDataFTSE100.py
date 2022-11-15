from src.mvc.DataPandasMVC import Control, Model, View

def main():
    _model = Model('data/ftse100/d/', 'asset_list/FTSE100.csv',
                'd', 365, True)
    _control = Control(_model, View())
    _control.main()

    _model = Model('data/ftse100/w/', 'asset_list/FTSE100.csv',
                'w', 52, True)
    _control = Control(_model, View())
    _control.main()
    _control.showAssetList()

if __name__ == "__main__":
    main()