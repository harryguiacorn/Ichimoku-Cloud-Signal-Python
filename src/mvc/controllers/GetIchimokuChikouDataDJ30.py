from src.mvc.core.DataChikouSignalMVC import (
    Control,
    DataChikouSignal,
    Model,
    View,
)


def main(
    fetch1HData=False,
    fetchDailyData=True,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    timeframes = [
        (fetch1HData, "data/dowjones30/1h/", True),
        (fetchDailyData, "data/dowjones30/d/", False),
        (fetchWeeklyData, "data/dowjones30/w/", False),
        (fetchMonthlyData, "data/dowjones30/m/", False),
    ]
    for enabled, path, datetime_format in timeframes:
        if enabled:
            model = Model(path, "asset_list/DowJones30.csv", datetime_format)
            for symbol in model.readAssetList():
                DataChikouSignal(symbol, path, datetime_format).main()
