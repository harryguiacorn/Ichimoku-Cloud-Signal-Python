from DataKijunSignalMVC import Control, Model, View

_model = Model('data/ftse100/d/', 'asset_list/FTSE100.csv')
_control = Control(_model, View())
_control.main()    

_model = Model('data/ftse100/w/', 'asset_list/FTSE100.csv')
_control = Control(_model, View())
_control.main()

