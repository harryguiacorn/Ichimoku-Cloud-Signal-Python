from src.mvc.core.DataTKxSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/spx500/1h/",
            "asset_list/SPX500.csv",
            "output/tkx/",
            "SPX500-tkx-1H",
            "1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/spx500/d/",
            "asset_list/SPX500.csv",
            "output/tkx/",
            "SPX500-tkx-D",
            "1D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/spx500/w/",
            "asset_list/SPX500.csv",
            "output/tkx/",
            "SPX500-tkx-W",
            "1W",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/spx500/m/",
            "asset_list/SPX500.csv",
            "output/tkx/",
            "SPX500-tkx-M",
            "1M",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
