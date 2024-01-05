from src.mvc.core.DataTKxSignalMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetch4HData=False,
    fetchDailyData=False,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model("data/bitfinex/1h/", "asset_list/bitfinex.csv", True)
        _control = Control(_model, View())
        _control.main()
    if fetch4HData:
        _model = Model("data/bitfinex/4h/", "asset_list/bitfinex.csv", True)
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model("data/bitfinex/d/", "asset_list/bitfinex.csv", True)
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model("data/bitfinex/w/", "asset_list/bitfinex.csv", True)
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model("data/bitfinex/m/", "asset_list/bitfinex.csv", True)
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
