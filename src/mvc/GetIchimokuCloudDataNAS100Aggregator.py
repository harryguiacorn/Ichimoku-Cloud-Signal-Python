from src.mvc.DataCloudSignalAggregatorMVC import Control, Model, View


def main(fetch1HData=False, fetchDailyData=True, fetchWeeklyData=False):
    if fetch1HData:
        _model = Model(
            "data/nasdaq100/1h/",
            "asset_list/Nasdaq100.csv",
            "output/",
            "Nasdaq100-cloud-1H",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/nasdaq100/d/",
            "asset_list/Nasdaq100.csv",
            "output/",
            "Nasdaq100-cloud-D",
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/nasdaq100/w/",
            "asset_list/Nasdaq100.csv",
            "output/",
            "Nasdaq100-cloud-W",
        )
        _control = Control(_model, View())
        _control.main()


if __name__ == "__main__":
    main()