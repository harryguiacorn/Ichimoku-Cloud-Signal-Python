from DataKijunSignalAggregatorMVC import Control, Model, View

_model = Model('data/dowjones30/d/', 'asset_list/DowJones30.csv', 'output/', 
               'Dow Jones 30-D')
_control = Control(_model, View())
_control.main()

_model = Model('data/dowjones30/w/', 'asset_list/DowJones30.csv', 'output/', 
               'Dow Jones 30-W')
_control = Control(_model, View())
_control.main()

