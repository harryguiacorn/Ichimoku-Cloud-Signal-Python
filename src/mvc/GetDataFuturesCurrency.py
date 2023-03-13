from src.mvc.DataPandasMVC import Control, Model, View


def main(fetchDailyData=True, fetchWeeklyData=False):
    if fetchDailyData:
        _model = Model(
            "data/futurescurrency/d/",
            "asset_list/FuturesCurrency.csv",
            "1d",
            "3mo",
            True,
        )
        _control = Control(_model, View())
        _control.main()

    if fetchWeeklyData:
        _model = Model(
            "data/futurescurrency/w/",
            "asset_list/FuturesCurrency.csv",
            "1wk",
            "1y",
            True,
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()


if __name__ == "__main__":
    main()
