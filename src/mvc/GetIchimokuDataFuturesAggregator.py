
from DataKijunSignalAggregatorMVC import Control, Model, View

_model = Model('data/futures/d/', 'asset_list/Futures.csv',
               'Futures-D')
_control = Control(_model, View())
_control.main()

_model = Model('data/futures/w/', 'asset_list/Futures.csv',
               'Futures-W')
_control = Control(_model, View())
_control.main()
