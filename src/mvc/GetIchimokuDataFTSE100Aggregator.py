
from DataKijunSignalAggregatorMVC import Control, Model, View

_model = Model('data/ftse100/d/', 'asset_list/FTSE100.csv', 'output/', 
               'FTSE100-D')
_control = Control(_model, View())
_control.main()

_model = Model('data/ftse100/w/', 'asset_list/FTSE100.csv', 'output/', 
               'FTSE100-W')
_control = Control(_model, View())
_control.main()
