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
            "data/kraken/1h/",
            "asset_list/Kraken.csv",
            "output/cloud/",
            "Kraken-cloud-1H",
            "1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetch4HData:
        _model = Model(
            "data/kraken/4h/",
            "asset_list/Kraken.csv",
            "output/cloud/",
            "Kraken-cloud-4H",
            "4H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/kraken/d/",
            "asset_list/Kraken.csv",
            "output/cloud/",
            "Kraken-cloud-D",
            "1D",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/kraken/w/",
            "asset_list/Kraken.csv",
            "output/cloud/",
            "Kraken-cloud-W",
            "1W",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchMonthlyData:
        _model = Model(
            "data/kraken/m/",
            "asset_list/Kraken.csv",
            "output/cloud/",
            "Kraken-cloud-M",
            "1M",
            True,
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()
