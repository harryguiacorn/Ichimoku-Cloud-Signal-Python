from src.mvc.DataKickerSignalAggregatorMVC import Control, Model, View


def main(fetchDailyData=True, fetchWeeklyData=False):
    if fetchDailyData:
        _model = Model(
            "data/futurescurrency/d/",
            "asset_list/FuturesCurrency.csv",
            "output/",
            "FuturesCurrency-D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/futurescurrency/w/",
            "asset_list/FuturesCurrency.csv",
            "output/",
            "FuturesCurrency-W",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
