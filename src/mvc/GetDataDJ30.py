from DataPandasMVC import Control, Model, View

_model = Model('data/dowjones30/d/', 'asset_list/DowJones30.csv',
               'd', 365, True)
_control = Control(_model, View())
_control.main()

_model = Model('data/dowjones30/w/', 'asset_list/DowJones30.csv',
               'w', 52, True)
_control = Control(_model, View())
_control.main()
_control.showAssetList()

