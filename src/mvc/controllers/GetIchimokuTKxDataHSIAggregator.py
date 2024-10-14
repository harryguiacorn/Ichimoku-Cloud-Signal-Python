from src.mvc.core.DataTKxSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/hsi/1h/",
            "asset_list/HSI.csv",
            "output/tkx/",
            "HSI-tkx-1H",
            "1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/hsi/d/",
            "asset_list/HSI.csv",
            "output/tkx/",
            "HSI-tkx-D",
            "1D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/hsi/w/",
            "asset_list/HSI.csv",
            "output/tkx/",
            "HSI-tkx-W",
            "1W",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/hsi/m/",
            "asset_list/HSI.csv",
            "output/tkx/",
            "HSI-tkx-M",
            "1M",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
