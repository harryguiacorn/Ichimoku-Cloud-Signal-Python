from src.mvc.core.DataChikouSignalMultiTimeframeMerger import (
    Control,
    Model,
    View,
)


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
        f"{asset_name} Chikou Multi Timeframe Scan",
    )
    Control(model, View()).main()
