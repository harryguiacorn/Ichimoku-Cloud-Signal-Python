# from DataKickerSignalMVC import Control, Model, View
from src.mvc.DataKickerSignalMVC import Control, Model, View

def main():
    _model = Model('data/futures/d/', 'asset_list/Futures.csv')
    _control = Control(_model, View())
    _control.main()    

    _model = Model('data/futures/w/', 'asset_list/Futures.csv')
    _control = Control(_model, View())
    _control.main()

if __name__ == "__main__":
    main()