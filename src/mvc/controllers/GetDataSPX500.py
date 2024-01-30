from src.mvc.core.DataPandasMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=False,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    # period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    # interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    if fetch1HData:
        _model = Model(
            "data/spx500/1h/", "asset_list/SPX500.csv", "1h", "2y", True
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/spx500/d/", "asset_list/SPX500.csv", "1d", "max", True
        )
        _control = Control(_model, View())
        _control.main()

    if fetchWeeklyData:
        _model = Model(
            "data/spx500/w/", "asset_list/SPX500.csv", "1wk", "max", True
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()

    if fetchMonthlyData:
        _model = Model(
            "data/spx500/m/", "asset_list/SPX500.csv", "1mo", "max", True
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()


if __name__ == "__main__":
    main()
