from DataKijunSignalMVC import Control, Model, View

_model = Model('data/spx500/d/', 'asset_list/SPX500.csv')
_control = Control(_model, View())
_control.main()    

_model = Model('data/spx500/w/', 'asset_list/SPX500.csv')
_control = Control(_model, View())
_control.main()

