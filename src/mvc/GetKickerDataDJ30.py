from DataKickerSignalMVC import Control, Model, View

_model = Model('data/dowjones30/d/', 'asset_list/DowJones30.csv')
_control = Control(_model, View())
_control.main()    

_model = Model('data/dowjones30/w/', 'asset_list/DowJones30.csv')
_control = Control(_model, View())
_control.main()

