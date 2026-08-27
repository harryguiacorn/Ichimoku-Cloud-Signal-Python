from cloud_signal.mvc.core.DataChikouSignalAggregatorMVC import Control, Model, View


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    timeframes = [
        (fetch1HData, "data/dowjones30/1h/", "DowJones30-chikou-1H", "1H"),
        (fetchDailyData, "data/dowjones30/d/", "DowJones30-chikou-D", "1D"),
        (fetchWeeklyData, "data/dowjones30/w/", "DowJones30-chikou-W", "1W"),
        (fetchMonthlyData, "data/dowjones30/m/", "DowJones30-chikou-M", "1M"),
    ]
    for enabled, path, filename, prefix in timeframes:
        if enabled:
            model = Model(
                path,
                "asset_list/DowJones30.csv",
                "output/chikou/",
                filename,
                prefix,
            )
            Control(model, View()).main()
