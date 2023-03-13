from src.mvc.DataKickerSignalAggregatorMVC import Control, Model, View


def main(fetchDailyData=True, fetchWeeklyData=False):
    if fetchDailyData:
        _model = Model(
            "data/ftse100/d/", "asset_list/FTSE100.csv", "output/", "FTSE100-D"
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/ftse100/w/", "asset_list/FTSE100.csv", "output/", "FTSE100-W"
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
