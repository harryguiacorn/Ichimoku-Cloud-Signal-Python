from src.mvc.core.DataTKxSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/futurescurrency/1h/",
            "asset_list/FuturesCurrency.csv",
            "output/tkx/",
            "FuturesCurrency-tkx-1H",
            "1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/futurescurrency/d/",
            "asset_list/FuturesCurrency.csv",
            "output/tkx/",
            "FuturesCurrency-tkx-D",
            "1D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/futurescurrency/w/",
            "asset_list/FuturesCurrency.csv",
            "output/tkx/",
            "FuturesCurrency-tkx-W",
            "1W",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/futurescurrency/m/",
            "asset_list/FuturesCurrency.csv",
            "output/tkx/",
            "FuturesCurrency-tkx-M",
            "1M",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
