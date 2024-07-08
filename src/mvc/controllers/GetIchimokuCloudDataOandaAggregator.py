from src.mvc.core.DataCloudSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetch4HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    if fetch1HData:
        _model = Model(
            "data/oanda/1h/",
            "asset_list/Oanda.csv",
            "output/cloud/",
            "Oanda-cloud-1H",
            "1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetch4HData:
        _model = Model(
            "data/oanda/4h/",
            "asset_list/Oanda.csv",
            "output/cloud/",
            "Oanda-cloud-4H",
            "4H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/oanda/d/",
            "asset_list/Oanda.csv",
            "output/cloud/",
            "Oanda-cloud-D",
            "1D",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/oanda/w/",
            "asset_list/Oanda.csv",
            "output/cloud/",
            "Oanda-cloud-W",
            "1W",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/oanda/m/",
            "asset_list/Oanda.csv",
            "output/cloud/",
            "Oanda-cloud-M",
            "1M",
            True,
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
