from DataPandasMVC import Control, Model, View

_model = Model('data/ftse250/d/', 'asset_list/FTSE250.csv',
               'd', 365, True)
_control = Control(_model, View())
_control.main()

_model = Model('data/ftse250/w/', 'asset_list/FTSE250.csv',
               'w', 52, True)
_control = Control(_model, View())
_control.main()
_control.showAssetList()

