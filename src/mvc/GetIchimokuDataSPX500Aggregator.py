from DataKijunSignalAggregatorMVC import Control, Model, View

_model = Model('data/spx500/d/', 'asset_list/SPX500.csv', 'output/', 
               'SPX 500-D')
_control = Control(_model, View())
_control.main()

_model = Model('data/spx500/w/', 'asset_list/SPX500.csv', 'output/', 
               'SPX 500-W')
_control = Control(_model, View())
_control.main()
