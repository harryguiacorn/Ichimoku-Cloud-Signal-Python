# from DataKickerSignalMVC import Control, Model, View
from src.mvc.DataKickerSignalMVC import Control, Model, View

def main():
    _model = Model('data/dowjones30/d/', 'asset_list/DowJones30.csv')
    _control = Control(_model, View())
    _control.main()    

    _model = Model('data/dowjones30/w/', 'asset_list/DowJones30.csv')
    _control = Control(_model, View())
    _control.main()

if __name__ == "__main__":
    main()