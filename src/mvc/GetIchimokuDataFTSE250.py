from DataKijunSignalMVC import Control, Model, View

_model = Model('data/ftse250/d/', 'asset_list/FTSE250.csv')
_control = Control(_model, View())
_control.main()    

_model = Model('data/ftse250/w/', 'asset_list/FTSE250.csv')
_control = Control(_model, View())
_control.main()

