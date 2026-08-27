from cloud_signal.mvc.core.DataChikouSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)

MARKET_NAMES = {
    "SPX500": "S&P 500",
    "Nasdaq100": "Nasdaq 100",
    "DowJones30": "Dow Jones 30",
    "Russell1000": "Russell 1000",
    "Oanda": "Oanda",
    "Kraken": "Kraken Cryptocurrency",
    "FTSE100": "FTSE 100",
    "FTSE250": "FTSE 250",
    "Futures": "Futures",
    "FuturesCurrency": "Futures Currency",
    "HSI": "Hang Seng Index",
}


def main(asset_name, timeframes, run_merger=True):
    if not run_merger:
        return

    input_paths = []
    direction_count_names = []
    for (
        _enabled,
        _data_path,
        _datetime_format,
        output_name,
        column_prefix,
    ) in timeframes:
        input_paths.append(f"output/chikou/{output_name}.csv")
        direction_count_names.append(
            [
                f"{column_prefix} Chikou Direction",
                f"{column_prefix} Chikou Count",
            ]
        )

    model = Model(
        input_paths,
        f"output/chikou/{asset_name}-chikou-merged.csv",
        direction_count_names,
        ["Chikou Score Sum"],
        f"{MARKET_NAMES.get(asset_name, asset_name)} Chikou Scan",
    )
    Control(model, View()).main()
