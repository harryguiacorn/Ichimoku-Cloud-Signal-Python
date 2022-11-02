
from DataKijunSignalAggregatorMVC import Control, Model, View

_model = Model('data/nasdaq100/d/', 'asset_list/Nasdaq100.csv', 'output/', 
               'Nasdaq100-D')
_control = Control(_model, View())
_control.main()

_model = Model('data/nasdaq100/w/', 'asset_list/Nasdaq100.csv', 'output/', 
               'Nasdaq100-W')
_control = Control(_model, View())
_control.main()
