from DataKijunSignalAggregatorMVC import Control, Model, View

_model = Model('data/futurescurrency/d/', 'asset_list/FuturesCurrency.csv', 'output/', 
               'Futures-D')
_control = Control(_model, View())
_control.main()

_model = Model('data/futurescurrency/w/', 'asset_list/FuturesCurrency.csv', 'output/', 
               'Futures-W')
_control = Control(_model, View())
_control.main()
