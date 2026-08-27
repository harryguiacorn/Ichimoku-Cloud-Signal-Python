from cloud_signal.mvc.core.DataChikouSignalAggregatorMVC import Control, Model, View


def main(asset_list_path, timeframes):
    """Aggregate per-symbol Chikou files for enabled timeframes.

    Each timeframe is (enabled, data_path, datetime_format, output_name,
    column_prefix). The datetime format is unused during aggregation.
    """
    for (
        enabled,
        data_path,
        _datetime_format,
        output_name,
        column_prefix,
    ) in timeframes:
        if not enabled:
            continue
        model = Model(
            data_path,
            asset_list_path,
            "output/chikou/",
            output_name,
            column_prefix,
        )
        Control(model, View()).main()
