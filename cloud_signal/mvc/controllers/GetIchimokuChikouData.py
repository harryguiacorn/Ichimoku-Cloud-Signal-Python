import os

from cloud_signal.mvc.core.DataChikouSignalMVC import DataChikouSignal, Model


def main(asset_list_path, timeframes):
    """Generate per-symbol Chikou files for enabled timeframes.

    Each timeframe is (enabled, data_path, datetime_format).
    """
    for enabled, data_path, datetime_format in timeframes:
        if not enabled or not os.path.isdir(data_path):
            continue
        model = Model(data_path, asset_list_path, datetime_format)
        for symbol in model.readAssetList():
            DataChikouSignal(symbol, data_path, datetime_format).main()
