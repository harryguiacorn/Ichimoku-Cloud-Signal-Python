from src.mvc.core.kraken.DataPandasKrakenMVC import Control, Model, View
import logging
logger = logging.getLogger(__name__)


def main(
    fetch1HData=False,
    fetch4HData=False,
    fetchDailyData=False,
    fetchWeeklyData=False,
    fetchMonthlyData=False,
):
    # Asset pair to get data for

    # Example: XBTUSD
    # interval
    # integer
    # Possible values: [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]

    # Default value: 1

    # Time frame interval in minutes

    # Example: 60
    # since
    # integer
    # Return up to 720 OHLC data points since given timestamp

    # Example: 1548111600

    if fetch1HData:
        _model = Model(
            "data/kraken/1h/",
            "asset_list/Kraken.csv",
            "60",
            "720",  # 720
            True,
        )
        _control = Control(_model, View())
        _control.main()

    # return

    if fetch4HData:
        # print("fetch 4h")
        _model = Model(
            "data/kraken/4h/",
            "asset_list/Kraken.csv",
            "240",
            "720",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchDailyData:
        _model = Model(
            "data/kraken/d/",
            "asset_list/Kraken.csv",
            "1440",
            "720",
            True,
        )
        _control = Control(_model, View())
        _control.main()
    if fetchWeeklyData:
        _model = Model(
            "data/kraken/w/",
            "asset_list/Kraken.csv",
            "10080",
            "720",
            True,
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()
    if fetchMonthlyData:
        _model = Model(
            "data/kraken/m/",
            "asset_list/Kraken.csv",
            "21600",
            "720",
            True,
        )
        _control = Control(_model, View())
        _control.main()
        _control.showAssetList()


if __name__ == "__main__":
    main()
