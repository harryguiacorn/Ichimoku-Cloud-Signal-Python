from src.mvc.DataKickerSignalAggregatorMVC import Control, Model, View

def main():
    _model = Model('data/dowjones30/d/', 'asset_list/DowJones30.csv', 'output/', 
                'Dow Jones 30-D')
    _control = Control(_model, View())
    _control.main()

    _model = Model('data/dowjones30/w/', 'asset_list/DowJones30.csv', 'output/', 
                'Dow Jones 30-W')
    _control = Control(_model, View())
    _control.main()

if __name__ == "__main__":
    main()