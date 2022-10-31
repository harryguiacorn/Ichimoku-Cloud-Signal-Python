from DataPandasMVC import Control, Model, View

_model = Model('data/futurescurrency/d/', 'asset_list/FuturesCurrency.csv',
               'd', 365, True)
_control = Control(_model, View())
_control.main()

_model = Model('data/futurescurrency/w/', 'asset_list/FuturesCurrency.csv',
               'w', 52, True)
_control = Control(_model, View())
_control.main()
_control.showAssetList()
